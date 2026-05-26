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
    line: Optional[int] = Field(None, description="Exact line number of bug, or null if success")
    message: str = Field(description="A one-sentence explanation of the hardware violation")
    citation: str = Field(description="Specific section, table, or page proving the error. Empty if success.")

# Dynamically import Node 1/2's retrieve_context function if present
retrieve_context = None
try:
    from rag import retrieve_context
    logger.info("Successfully imported retrieve_context from rag.py")
except ImportError:
    try:
        from retrieve import retrieve_context
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
    return "gemini", None, "gemini-1.5-flash"

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

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handles tool execution requests from the MCP client.
    """
    if name == "validate_hardware_code_mock":
        # ---------------------------------------------------------
        # PHASE 1: THE CONTRACT (MOCK ENDPOINT)
        # ---------------------------------------------------------
        mock_response = {
            "status": "error",
            "line": 42,
            "message": "Register 0x3F is read-only.",
            "citation": "Datasheet Page 14, Table 3: Register Map"
        }
        return [TextContent(type="text", text=json.dumps(mock_response))]

    elif name == "validate_hardware_code":
        # ---------------------------------------------------------
        # PHASE 2/3: THE REAL IMPLEMENTATION
        # ---------------------------------------------------------
        if not arguments:
            return [TextContent(type="text", text=json.dumps({"status": "system_error", "message": "Missing arguments."}))]
            
        code = arguments.get("code_snippet")
        component = arguments.get("component")
        
        if not code or not component:
            return [TextContent(type="text", text=json.dumps({"status": "system_error", "message": "Missing code_snippet or component parameter."}))]
        
        try:
            # 1. Retrieve context (either via Node 1/2 function or fallback mock)
            if retrieve_context is not None:
                try:
                    logger.info(f"Querying RAG database for component '{component}'...")
                    sig = inspect.signature(retrieve_context)
                    if "component_name" in sig.parameters:
                        context = retrieve_context(component_name=component, code_snippet=code)
                    else:
                        context = retrieve_context(component, code)
                except Exception as rag_err:
                    logger.warning(f"RAG retrieval failed: {rag_err}. Falling back to mock context.")
                    context = f"Mock retrieved context for {component} from Node 1 DB..."
            else:
                context = f"Mock retrieved context for {component} from Node 1 DB..."
            
            # 2. Construct LLM prompts
            system_prompt = get_agent_system_prompt()
            user_prompt = f"Context:\n{context}\n\nCode:\n{code}"
            
            # 3. Determine LLM provider and call the model
            client_type, client, model_name = get_llm_client()
            logger.info(f"Validating {component} code using LLM provider '{client_type}' with model '{model_name}'...")
            
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
                result_text = response.choices[0].message.content
            elif client_type == "gemini":
                model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
                response = model.generate_content(
                    user_prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=HardwareValidationResult,
                        temperature=0.1
                    )
                )
                result_text = response.text
            else:
                raise ValueError("No LLM provider configuration found. Set GEMINI_API_KEY or AZURE_OPENAI_API_KEY in .env.")
            
            return [TextContent(type="text", text=result_text)]
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            error_payload = {
                "status": "system_error",
                "message": f"Analysis failed: {str(e)}"
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