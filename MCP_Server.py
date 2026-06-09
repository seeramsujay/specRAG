import asyncio
import json
import os
import sys
import logging
import inspect
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Optional
from pydantic import BaseModel, Field
import google.generativeai as genai
from openai import AzureOpenAI, OpenAI

# Configure logging to go to stderr (crucial for MCP to not corrupt stdout)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)

# Load environment variables (e.g., GEMINI_API_KEY, AZURE_OPENAI_API_KEY)
load_dotenv()

# Initialize the MCP Server
app = Server("specrag-backend")

# Define JSON Schema via Pydantic for LLM structured output mapping
class HardwareValidationResult(BaseModel):
    status: str = Field(description="'error' or 'success'")
    severity: Optional[str] = Field(None, description="Error severity: 'high', 'medium', 'low', or null if success")
    line: Optional[int] = Field(None, description="Exact line number of bug, or null if success")
    message: str = Field(description="A one-sentence explanation of the hardware violation")
    citation: str = Field(description="Specific section, table, or page proving the error. Empty if success.")

# Dynamically import Node 1/2's retrieve_context function if present
retrieve_context = None
try:
    from rag import retrieve_context
    logger.info("Successfully imported retrieve_context from rag.py")
except ImportError:
    # Use dynamic import to prevent static analysis linter errors for missing modules
    import importlib
    try:
        retrieve_module = importlib.import_module("retrieve")
        retrieve_context = getattr(retrieve_module, "retrieve_context", None)
        logger.info("Successfully imported retrieve_context from retrieve.py")
    except ImportError:
        logger.info("No retrieve_context function found in rag.py or retrieve.py. Using mock retriever.")

def get_llm_client():
    """
    Checks environment configuration and returns the appropriate client.
    Returns:
        tuple: (client_type, client_instance, model_name)
        client_type can be 'azure_openai', 'openai', or 'gemini'.
    """
    azure_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    
    if azure_key and azure_endpoint:
        client = AzureOpenAI(
            api_key=azure_key,
            azure_endpoint=azure_endpoint,
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")
        )
        model = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
        return "azure_openai", client, model

    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        client = OpenAI(api_key=openai_key)
        model = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o")
        return "openai", client, model

    # Fallback to Gemini
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        genai.configure(api_key=gemini_key)
    model = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    return "gemini", None, model

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Exposes available tools to the MCP client.
    """
    return [
        Tool(
            name="validate_hardware_code_mock",
            description="Phase 1 Mock: Validates C/C++ hardware code against datasheet rules.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_snippet": {"type": "string", "description": "The C/C++ code to validate"},
                    "component": {"type": "string", "description": "Target component (e.g., 'MPU6050')"}
                },
                "required": ["code_snippet", "component"]
            }
        ),
        Tool(
            name="validate_hardware_code",
            description="Phase 2 Real: Validates C/C++ hardware code using LLM and RAG context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_snippet": {"type": "string", "description": "The C/C++ code to validate"},
                    "component": {"type": "string", "description": "Target component (e.g., 'MPU6050')"}
                },
                "required": ["code_snippet", "component"]
            }
        )
    ]

def evaluate_logic_mock(filtered_code: str, vector_context: str) -> dict:
    """
    Phase 1 Mock: Ignores the input entirely and just spits out a perfectly
    formatted JSON error, allowing the backend server to test its routing logic.
    """
    return {
        "status": "error",
        "severity": "high",
        "line": 42,
        "message": "Register 0x3F is read-only.",
        "citation": "Datasheet Page 14, Table 3: Register Map"
    }

def evaluate_logic(filtered_code: str, vector_context: str) -> dict:
    """
    Phase 2 Real: Validates filtered C++ hardware code against retrieved vector context
    using the configured LLM client. Returns a dictionary matching the HardwareValidationResult schema.
    """
    try:
        system_prompt = get_agent_system_prompt()
        user_prompt = f"Context:\n{vector_context}\n\nCode:\n{filtered_code}"
        
        client_type, client, model_name = get_llm_client()
        logger.info(f"Evaluating logic using LLM provider '{client_type}' with model '{model_name}'...")
        
        if client_type in ("azure_openai", "openai"):
            response = client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=HardwareValidationResult,
                temperature=0.1
            )
            result_json = response.choices[0].message.content
            return json.loads(result_json)
        elif client_type == "gemini":
            # Direct dictionary schema avoids "Unknown field for Schema: default" in older SDK versions
            gemini_schema = {
                "type": "OBJECT",
                "properties": {
                    "status": {
                        "type": "STRING",
                        "description": "'error' or 'success'"
                    },
                    "severity": {
                        "type": "STRING",
                        "description": "Error severity: 'high', 'medium', 'low', or null if success"
                    },
                    "line": {
                        "type": "INTEGER",
                        "description": "Exact line number of bug, or null if success"
                    },
                    "message": {
                        "type": "STRING",
                        "description": "A one-sentence explanation of the hardware violation"
                    },
                    "citation": {
                        "type": "STRING",
                        "description": "Specific section, table, or page proving the error. Empty if success."
                    }
                },
                "required": ["status", "message", "citation"]
            }
            model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
            response = model.generate_content(
                user_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=gemini_schema,
                    temperature=0.1
                )
            )
            return json.loads(response.text)
        else:
            raise ValueError("No LLM provider configuration found. Set GEMINI_API_KEY or AZURE_OPENAI_API_KEY in .env.")
            
    except Exception as e:
        logger.error(f"Logic evaluation failed: {str(e)}")
        return {
            "status": "system_error",
            "severity": "high",
            "line": None,
            "message": f"Logic evaluation failed: {str(e)}",
            "citation": ""
        }

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handles tool execution requests from the MCP client.
    """
    if name == "validate_hardware_code_mock":
        # ---------------------------------------------------------
        # PHASE 1: THE CONTRACT (MOCK ENDPOINT)
        # ---------------------------------------------------------
        code = arguments.get("code_snippet", "") if arguments else ""
        component = arguments.get("component", "") if arguments else ""
        mock_response = evaluate_logic_mock(code, f"Mock retrieved context for {component}...")
        return [TextContent(type="text", text=json.dumps(mock_response))]

    elif name == "validate_hardware_code":
        # ---------------------------------------------------------
        # PHASE 2/3: THE REAL IMPLEMENTATION
        # ---------------------------------------------------------
        if not arguments:
            return [TextContent(type="text", text=json.dumps({
                "status": "system_error",
                "severity": "high",
                "line": None,
                "message": "Missing arguments.",
                "citation": ""
            }))]
            
        code = arguments.get("code_snippet")
        component = arguments.get("component")
        
        if not code or not component:
            return [TextContent(type="text", text=json.dumps({
                "status": "system_error",
                "severity": "high",
                "line": None,
                "message": "Missing code_snippet or component parameter.",
                "citation": ""
            }))]
        
        try:
            # 1. Filter the incoming code snippet via AST
            logger.info("Filtering C++ code snippet via AST parsing...")
            try:
                from ast_parser import filter_hardware_logic
                filtered_code = filter_hardware_logic(code)
            except Exception as ast_err:
                logger.warning(f"AST parsing/filtering failed: {ast_err}. Using original code snippet.")
                filtered_code = code

            # 2. Retrieve context (either via Node 1/2 function or fallback mock) using the filtered code
            if retrieve_context is not None:
                try:
                    logger.info(f"Querying RAG database for component '{component}'...")
                    sig = inspect.signature(retrieve_context)
                    if "component_name" in sig.parameters:
                        context = retrieve_context(component_name=component, code_snippet=filtered_code)
                    else:
                        context = retrieve_context(component, filtered_code)
                except Exception as rag_err:
                    logger.warning(f"RAG retrieval failed: {rag_err}. Falling back to mock context.")
                    context = f"Mock retrieved context for {component} from Node 1 DB..."
            else:
                context = f"Mock retrieved context for {component} from Node 1 DB..."
            
            # 3. Run the evaluation using the filtered code
            result = evaluate_logic(filtered_code=filtered_code, vector_context=context)
            return [TextContent(type="text", text=json.dumps(result))]
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            error_payload = {
                "status": "system_error",
                "severity": "high",
                "line": None,
                "message": f"Analysis failed: {str(e)}",
                "citation": ""
            }
            return [TextContent(type="text", text=json.dumps(error_payload))]
            
    else:
        raise ValueError(f"Unknown tool: {name}")

def get_agent_system_prompt() -> str:
    """Returns the strict system prompt for the hardware validator agent."""
    file_path = os.path.join(os.path.dirname(__file__), "Archives", "AGENT.md")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning(f"Strategy prompt {file_path} not found. Using fallback.")
        return "You are a hardware code validator. Analyze code against context and return strictly compliant JSON."

async def main():
    """Runs the MCP server over standard input/output."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import sys
    print("SpecRAG MCP Server booting up...", file=sys.stderr)
    asyncio.run(main())