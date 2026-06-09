import * as child_process from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';

export interface ValidationResponse {
    status: 'error' | 'success' | 'system_error';
    severity: 'high' | 'medium' | 'low' | null;
    line: number | null;
    message: string;
    citation: string;
}

export class McpClient {
    private process: child_process.ChildProcess | null = null;
    private requestId = 1;
    private pendingRequests = new Map<number, { resolve: (val: any) => void; reject: (err: Error) => void }>();
    private outputChannel: vscode.OutputChannel;
    private stdoutBuffer = '';
    private isInitialized = false;
    private connectionState: 'DISCONNECTED' | 'CONNECTING' | 'CONNECTED' = 'DISCONNECTED';

    constructor() {
        this.outputChannel = vscode.window.createOutputChannel('SpecRAG Server Log');
    }

    public log(message: string) {
        this.outputChannel.appendLine(`[${new Date().toISOString()}] ${message}`);
    }

    public showChannel() {
        this.outputChannel.show(true);
    }

    private async ensureConnected(): Promise<void> {
        if (this.connectionState === 'CONNECTED' && this.process) {
            return;
        }

        if (this.connectionState === 'CONNECTING') {
            // Wait for existing connection attempt to resolve
            return new Promise((resolve, reject) => {
                const check = setInterval(() => {
                    if (this.connectionState === 'CONNECTED') {
                        clearInterval(check);
                        resolve();
                    } else if (this.connectionState === 'DISCONNECTED') {
                        clearInterval(check);
                        reject(new Error('Failed to connect to SpecRAG Server'));
                    }
                }, 100);
            });
        }

        this.connectionState = 'CONNECTING';
        this.isInitialized = false;
        this.stdoutBuffer = '';
        this.pendingRequests.clear();

        const config = vscode.workspace.getConfiguration('specrag');
        const pythonPath = config.get<string>('pythonPath', 'python');
        
        // Find Server.py path
        let serverPath = config.get<string>('serverPath', '');
        if (!serverPath) {
            const workspaceFolders = vscode.workspace.workspaceFolders;
            if (workspaceFolders && workspaceFolders.length > 0) {
                serverPath = path.join(workspaceFolders[0].uri.fsPath, 'Server.py');
            }
        }

        if (!serverPath) {
            this.connectionState = 'DISCONNECTED';
            throw new Error('Workspace folder is not open, and no Server.py path is configured.');
        }

        const cwd = path.dirname(serverPath);
        this.log(`Spawning MCP server at: ${serverPath}`);
        this.log(`Using Python interpreter: ${pythonPath}`);
        this.log(`Cwd: ${cwd}`);

        try {
            // Use -u to make Python output unbuffered (critical for stdio integration)
            this.process = child_process.spawn(pythonPath, ['-u', serverPath], {
                cwd,
                env: { ...process.env }
            });
        } catch (err: any) {
            this.connectionState = 'DISCONNECTED';
            this.log(`Failed to spawn Python process: ${err.message}`);
            throw new Error(`Failed to spawn Python process: ${err.message}`);
        }

        if (!this.process || !this.process.stdout || !this.process.stdin || !this.process.stderr) {
            this.connectionState = 'DISCONNECTED';
            throw new Error('Failed to set up standard input/output streams for SpecRAG server.');
        }

        // Handle stderr
        this.process.stderr.on('data', (data) => {
            const lines = data.toString().split('\n');
            for (const line of lines) {
                if (line.trim()) {
                    this.log(`[Server Stderr] ${line}`);
                }
            }
        });

        // Handle stdout
        this.process.stdout.on('data', (data) => {
            this.stdoutBuffer += data.toString();
            this.processStdoutBuffer();
        });

        // Handle close/exit
        this.process.on('close', (code) => {
            this.log(`Process exited with code: ${code}`);
            this.cleanup();
        });

        this.process.on('error', (err) => {
            this.log(`Process error: ${err.message}`);
            this.cleanup();
        });

        // Perform the MCP Handshake
        try {
            await this.performHandshake();
            this.connectionState = 'CONNECTED';
            this.log('MCP handshake completed successfully.');
        } catch (err: any) {
            this.cleanup();
            throw new Error(`MCP handshake failed: ${err.message}`);
        }
    }

    private cleanup() {
        this.connectionState = 'DISCONNECTED';
        this.isInitialized = false;
        if (this.process) {
            this.process.kill();
            this.process = null;
        }
        for (const [id, req] of this.pendingRequests.entries()) {
            req.reject(new Error('Process disconnected.'));
        }
        this.pendingRequests.clear();
    }

    public dispose() {
        this.cleanup();
        this.outputChannel.dispose();
    }

    private processStdoutBuffer() {
        let newlineIndex = this.stdoutBuffer.indexOf('\n');
        while (newlineIndex !== -1) {
            const messageStr = this.stdoutBuffer.substring(0, newlineIndex).trim();
            this.stdoutBuffer = this.stdoutBuffer.substring(newlineIndex + 1);
            
            if (messageStr) {
                try {
                    const message = JSON.parse(messageStr);
                    this.handleJsonRpcMessage(message);
                } catch (err) {
                    this.log(`JSON parse error on stdout: ${err} (Raw line: "${messageStr}")`);
                }
            }
            
            newlineIndex = this.stdoutBuffer.indexOf('\n');
        }
    }

    private handleJsonRpcMessage(message: any) {
        if (message.id !== undefined) {
            const id = Number(message.id);
            const pending = this.pendingRequests.get(id);
            if (pending) {
                this.pendingRequests.delete(id);
                if (message.error) {
                    pending.reject(new Error(message.error.message || 'Unknown RPC error'));
                } else {
                    pending.resolve(message.result);
                }
            }
        } else {
            // Notifications or other messages
            this.log(`Received notification/event: ${JSON.stringify(message)}`);
        }
    }

    private performHandshake(): Promise<void> {
        return new Promise((resolve, reject) => {
            const initId = this.requestId++;
            const initRequest = {
                jsonrpc: '2.0',
                id: initId,
                method: 'initialize',
                params: {
                    protocolVersion: '2024-11-05',
                    capabilities: {},
                    clientInfo: {
                        name: 'specrag-vscode',
                        version: '0.1.0'
                    }
                }
            };

            const timeout = setTimeout(() => {
                this.pendingRequests.delete(initId);
                reject(new Error('Timeout waiting for initialize response from server.'));
            }, 8000);

            this.pendingRequests.set(initId, {
                resolve: (result) => {
                    clearTimeout(timeout);
                    try {
                        this.sendNotification('notifications/initialized');
                        this.isInitialized = true;
                        resolve();
                    } catch (err) {
                        reject(err);
                    }
                },
                reject: (err) => {
                    clearTimeout(timeout);
                    reject(err);
                }
            });

            this.sendRaw(initRequest);
        });
    }

    private sendRaw(message: any) {
        if (!this.process || !this.process.stdin) {
            throw new Error('Process is not running.');
        }
        const jsonStr = JSON.stringify(message) + '\n';
        this.process.stdin.write(jsonStr);
    }

    private sendNotification(method: string, params?: any) {
        const notification = {
            jsonrpc: '2.0',
            method,
            ...(params ? { params } : {})
        };
        this.sendRaw(notification);
    }

    private async callTool(name: string, argumentsObj: any): Promise<any> {
        await this.ensureConnected();

        return new Promise((resolve, reject) => {
            const id = this.requestId++;
            const request = {
                jsonrpc: '2.0',
                id,
                method: 'tools/call',
                params: {
                    name,
                    arguments: argumentsObj
                }
            };

            // Set a 30 second timeout for LLM reasoning responses
            const timeout = setTimeout(() => {
                this.pendingRequests.delete(id);
                reject(new Error(`Timeout waiting for tool call response for '${name}'.`));
            }, 35000);

            this.pendingRequests.set(id, {
                resolve: (result) => {
                    clearTimeout(timeout);
                    resolve(result);
                },
                reject: (err) => {
                    clearTimeout(timeout);
                    reject(err);
                }
            });

            this.sendRaw(request);
        });
    }

    public async validateHardwareCode(codeSnippet: string, component: string, useMock = false): Promise<ValidationResponse> {
        const toolName = useMock ? 'validate_hardware_code_mock' : 'validate_hardware_code';
        try {
            this.log(`Calling validation tool '${toolName}' for component '${component}'...`);
            const result = await this.callTool(toolName, {
                code_snippet: codeSnippet,
                component: component
            });

            if (result && result.content && result.content.length > 0) {
                const text = result.content[0].text;
                const parsedResponse = JSON.parse(text) as ValidationResponse;
                return parsedResponse;
            }

            throw new Error('Invalid empty result payload from tool.');
        } catch (err: any) {
            this.log(`Validation failed: ${err.message}`);
            return {
                status: 'system_error',
                severity: 'high',
                line: null,
                message: `Validation failed: ${err.message}`,
                citation: ''
            };
        }
    }
}
