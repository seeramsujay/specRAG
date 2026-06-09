import * as vscode from 'vscode';
import { McpClient, ValidationResponse } from './mcpClient';

let mcpClient: McpClient | null = null;
let diagnosticCollection: vscode.DiagnosticCollection;
let statusBarItem: vscode.StatusBarItem;
const diagnosticCitationMap = new Map<string, string>(); // Keyed by `${uri.toString()}:${line}`

export function activate(context: vscode.ExtensionContext) {
    console.log('SpecRAG extension is now active!');

    // Initialize MCP client
    mcpClient = new McpClient();
    context.subscriptions.push(mcpClient);

    // Create diagnostic collection
    diagnosticCollection = vscode.languages.createDiagnosticCollection('specrag');
    context.subscriptions.push(diagnosticCollection);

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = '$(cpu) SpecRAG: Ready';
    statusBarItem.tooltip = 'Click to run SpecRAG manual validation on current file';
    statusBarItem.command = 'specrag.validate';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('specrag.validate', async () => {
            const activeEditor = vscode.window.activeTextEditor;
            if (activeEditor) {
                mcpClient?.showChannel();
                await runValidation(activeEditor.document, true);
            } else {
                vscode.window.showInformationMessage('No active editor found to validate.');
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('specrag.clearDiagnostics', () => {
            diagnosticCollection.clear();
            diagnosticCitationMap.clear();
            updateStatusBar('Ready', 'info');
            vscode.window.showInformationMessage('SpecRAG diagnostics cleared.');
        })
    );

    // Event handler: On document save
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(async (document) => {
            const config = vscode.workspace.getConfiguration('specrag');
            const trigger = config.get<string>('validationTrigger', 'onSave');
            if (trigger === 'onSave' && isSupportedLanguage(document)) {
                await runValidation(document, false);
            }
        })
    );

    // Event handler: On document change (debounced)
    let debounceTimer: NodeJS.Timeout | undefined;
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument((event) => {
            const config = vscode.workspace.getConfiguration('specrag');
            const trigger = config.get<string>('validationTrigger', 'onSave');
            if (trigger === 'onType' && isSupportedLanguage(event.document)) {
                if (debounceTimer) {
                    clearTimeout(debounceTimer);
                }
                const delay = config.get<number>('debouncingDelay', 1500);
                debounceTimer = setTimeout(async () => {
                    await runValidation(event.document, false);
                }, delay);
            }
        })
    );

    // Clean up diagnostics when a document is closed
    context.subscriptions.push(
        vscode.workspace.onDidCloseTextDocument((document) => {
            diagnosticCollection.delete(document.uri);
            // Clean citation map keys for this document
            const uriStr = document.uri.toString();
            for (const key of diagnosticCitationMap.keys()) {
                if (key.startsWith(uriStr)) {
                    diagnosticCitationMap.delete(key);
                }
            }
        })
    );

    // Register custom Hover Provider for citations
    context.subscriptions.push(
        vscode.languages.registerHoverProvider(
            [
                { scheme: 'file', language: 'cpp' },
                { scheme: 'file', language: 'c' },
                { scheme: 'file', language: 'arduino' }
            ],
            {
                provideHover(document, position) {
                    const lineDiagnostics = diagnosticCollection.get(document.uri) || [];
                    for (const diag of lineDiagnostics) {
                        if (diag.range.contains(position)) {
                            if (diag.code === 'specrag') {
                                const mapKey = `${document.uri.toString()}:${diag.range.start.line}`;
                                const citation = diagnosticCitationMap.get(mapKey);
                                if (citation) {
                                    const markdown = new vscode.MarkdownString();
                                    markdown.appendMarkdown(`### 🦾 SpecRAG Hardware Auditor\n\n`);
                                    markdown.appendMarkdown(`⚠️ **Violation:** ${diag.message}\n\n`);
                                    markdown.appendMarkdown(`📚 **Datasheet Citation:** _${citation}_\n`);
                                    markdown.isTrusted = true;
                                    return new vscode.Hover(markdown, diag.range);
                                }
                            }
                        }
                    }
                    return null;
                }
            }
        )
    );

    // Register custom Code Action Provider for Quick Fixes
    context.subscriptions.push(
        vscode.languages.registerCodeActionsProvider(
            [
                { scheme: 'file', language: 'cpp' },
                { scheme: 'file', language: 'c' },
                { scheme: 'file', language: 'arduino' }
            ],
            new SpecRagCodeActionProvider(),
            {
                providedCodeActionKinds: [vscode.CodeActionKind.QuickFix]
            }
        )
    );
}

export function deactivate() {
    if (mcpClient) {
        mcpClient.dispose();
    }
}

function isSupportedLanguage(document: vscode.TextDocument): boolean {
    const lang = document.languageId;
    return lang === 'cpp' || lang === 'c' || lang === 'arduino';
}

function updateStatusBar(status: 'Ready' | 'Auditing...' | 'Success' | 'Error', type: 'info' | 'warn' | 'success' = 'info') {
    if (status === 'Auditing...') {
        statusBarItem.text = '$(sync~spin) SpecRAG: Auditing...';
        statusBarItem.color = new vscode.ThemeColor('statusBarItem.warningForeground');
    } else if (status === 'Success') {
        statusBarItem.text = '$(pass) SpecRAG: Success';
        statusBarItem.color = new vscode.ThemeColor('statusBarItem.prominentForeground');
    } else if (status === 'Error') {
        statusBarItem.text = '$(error) SpecRAG: Violations Found';
        statusBarItem.color = new vscode.ThemeColor('statusBarItem.errorForeground');
    } else {
        statusBarItem.text = '$(cpu) SpecRAG: Ready';
        statusBarItem.color = undefined;
    }
}

function extractComponentName(text: string): string {
    // Look for lines like: // @component MPU6050 or /* @component MPU6050 */
    const commentRegex = /\/\/\s*@component\s+([A-Za-z0-9_-]+)/;
    const blockCommentRegex = /\/\*\s*@component\s+([A-Za-z0-9_-]+)/;
    
    let match = text.match(commentRegex);
    if (match && match[1]) {
        return match[1].trim();
    }
    
    match = text.match(blockCommentRegex);
    if (match && match[1]) {
        return match[1].trim();
    }
    
    const config = vscode.workspace.getConfiguration('specrag');
    return config.get<string>('defaultComponent', 'MPU6050');
}

async function runValidation(document: vscode.TextDocument, isManual: boolean) {
    if (!mcpClient) {
        return;
    }

    const text = document.getText();
    const componentName = extractComponentName(text);
    
    updateStatusBar('Auditing...');
    mcpClient.log(`Starting validation for '${document.fileName}' with component '${componentName}'`);

    const config = vscode.workspace.getConfiguration('specrag');
    const useMock = config.get<boolean>('useMock', false);

    const result: ValidationResponse = await mcpClient.validateHardwareCode(text, componentName, useMock);

    // Clear old diagnostics for this document
    diagnosticCollection.delete(document.uri);
    const uriStr = document.uri.toString();
    for (const key of diagnosticCitationMap.keys()) {
        if (key.startsWith(uriStr)) {
            diagnosticCitationMap.delete(key);
        }
    }

    if (result.status === 'success') {
        updateStatusBar('Success', 'success');
        if (isManual) {
            vscode.window.showInformationMessage(`SpecRAG Audit: Successfully validated code against ${componentName} constraints!`);
        }
    } else if (result.status === 'error') {
        updateStatusBar('Error', 'warn');
        
        let line = result.line !== null ? result.line : 1;
        // Adjust for 0-based indexing in VS Code
        let lineIndex = line - 1;
        if (lineIndex < 0) {
            lineIndex = 0;
        } else if (lineIndex >= document.lineCount) {
            lineIndex = document.lineCount - 1;
        }

        const lineObj = document.lineAt(lineIndex);
        const range = new vscode.Range(
            lineIndex,
            lineObj.firstNonWhitespaceCharacterIndex,
            lineIndex,
            lineObj.text.length
        );

        let severity = vscode.DiagnosticSeverity.Error;
        if (result.severity === 'medium') {
            severity = vscode.DiagnosticSeverity.Warning;
        } else if (result.severity === 'low') {
            severity = vscode.DiagnosticSeverity.Information;
        }

        const diagMessage = `${result.message} [Citation: ${result.citation}]`;
        const diagnostic = new vscode.Diagnostic(range, diagMessage, severity);
        diagnostic.code = 'specrag';
        diagnostic.source = 'SpecRAG Auditor';

        diagnosticCollection.set(document.uri, [diagnostic]);
        
        // Cache the citation for the custom hover provider
        const mapKey = `${document.uri.toString()}:${lineIndex}`;
        diagnosticCitationMap.set(mapKey, result.citation);

        if (isManual) {
            vscode.window.showWarningMessage(`SpecRAG Audit: Code violation found on line ${line}!`);
        }
    } else {
        // System Error
        updateStatusBar('Ready', 'info');
        mcpClient.log(`System Error returned from backend: ${result.message}`);
        vscode.window.showWarningMessage(`SpecRAG System Error: ${result.message}`);
    }
}

class SpecRagCodeActionProvider implements vscode.CodeActionProvider {
    provideCodeActions(
        document: vscode.TextDocument,
        range: vscode.Range | vscode.Selection,
        context: vscode.CodeActionContext
    ): vscode.CodeAction[] {
        const actions: vscode.CodeAction[] = [];
        for (const diagnostic of context.diagnostics) {
            if (diagnostic.code === 'specrag') {
                // Quick Fix 1: Comment out the offending line
                const commentAction = new vscode.CodeAction(
                    'Comment out hardware call (SpecRAG)',
                    vscode.CodeActionKind.QuickFix
                );
                commentAction.diagnostics = [diagnostic];
                commentAction.edit = new vscode.WorkspaceEdit();
                
                const lineIndex = diagnostic.range.start.line;
                const lineObj = document.lineAt(lineIndex);
                commentAction.edit.insert(
                    document.uri,
                    new vscode.Position(lineIndex, lineObj.firstNonWhitespaceCharacterIndex),
                    '// '
                );
                actions.push(commentAction);

                // Quick Fix 2: Add a FIXME annotation above
                const fixAnnotAction = new vscode.CodeAction(
                    'Add FIXME annotation (SpecRAG)',
                    vscode.CodeActionKind.QuickFix
                );
                fixAnnotAction.diagnostics = [diagnostic];
                fixAnnotAction.edit = new vscode.WorkspaceEdit();
                
                // Construct clean message without citation suffix
                const cleanMsg = diagnostic.message.replace(/\s*\[Citation:.*\]$/, '');
                fixAnnotAction.edit.insert(
                    document.uri,
                    new vscode.Position(lineIndex, 0),
                    `// FIXME: SpecRAG detected violation - ${cleanMsg}\n`
                );
                actions.push(fixAnnotAction);
            }
        }
        return actions;
    }
}
