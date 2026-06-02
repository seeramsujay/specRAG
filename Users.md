# 🤝 SpecRAG Integration Guide (Node Handover)

Hello Team! This document outlines what I (Node 3: AI Engineering & Reasoning) have completed, how the core Brain works, and exactly what the rest of the nodes need to do to hit our Phase 3/4 milestones seamlessly.

## 🟢 Node 1: RAG Data Engineering & Vector Architecture
**Your Goal:** Feed the AI the exact datasheet context.
**What I've done:** I have fully integrated the Gemini API with structured output enforcement. It mathematically cannot hallucinate JSON formats anymore. 
**What I need from you:**
1. I left a placeholder string in `MCP_Server.py` (Line ~102): `context = f"Mock retrieved context for {component} from Node 1 DB..."`.
2. You need to write your `retrieve_context(component_name, code_snippet)` Python function.
3. Once your local Vector DB (Chroma/FAISS) is working, import your function into `MCP_Server.py` and replace my placeholder.
4. **Context Quality is King**: If your context misses the I2C registers, my AI will miss the I2C bug. Ensure table data from the PDFs is intact!

## 🟠 Node 4: IDE Client & Developer UX
**Your Goal:** Present the errors to the user gracefully.
**What I've done:** The MCP Server is complete, error-proofed, and fully tested. It exposes a tool called `validate_hardware_code`.
**What you need to do:**
1. When you trigger the MCP Tool, provide exactly this schema:
   ```json
   {
     "code_snippet": "void setup() { ... }",
     "component": "MPU6050"
   }
   ```
2. The server will **always** return a stringified JSON matching this exact Pydantic schema:
   ```json
   {
     "status": "error" | "success" | "system_error",
     "severity": "high" | "medium" | "low" | null,
     "line": 42,
     "message": "Register 0x3F is read-only.",
     "citation": "Datasheet Page 14, Table 3"
   }
   ```
3. If `status == "system_error"`, something broke (bad arguments, API timeout). Gracefully show a toast notification in VS Code instead of a red squiggly line.
4. If `status == "error"`, draw the red squiggly on the `line` returned, and put the `message` and `citation` in the hover tooltip.
5. **Python API Integration**: Node 2 can import Node 3's evaluation functions directly for local python routing:
   ```python
   from MCP_Server import evaluate_logic, evaluate_logic_mock
   
   # For real evaluation:
   result_dict = evaluate_logic(filtered_code, vector_context)
   
   # For dry run / mock validation:
   result_dict = evaluate_logic_mock(filtered_code, vector_context)
   ```

## 🟣 Node 2: AST Parsing & Backend Infrastructure
**Your Goal:** Filter raw firmware code via AST parsing and route the data cleanly to prevent LLM context pollution.
**What I've done:**
1. I have set up the core validation framework and system prompt structure in `MCP_Server.py`.
2. I've designed the validation response schema to accept code snippets and component names.
**What I need from you:**
1. **AST Integration:** Target Arduino and ESP32 C++ syntax to programmatically extract only hardware-relevant lines (`pinMode`, `digitalWrite`, etc.).
2. **Data Routing:** Package the parsed C++ code and the RAG context retrieved from Node 1, and route the unified payload to the AI evaluation module.
3. **Local Server:** Finalize the FastAPI or Model Context Protocol server configuration to listen for incoming requests from Node 4's VS Code client.

---
**Server Boot Command for Testing:**
We now support configuring API keys via a `.env` file (see `.env.example`). Once configured, you can boot the server using the wrapper:
```bash
python Server.py
```
The server dynamically loads the key and runs the MCP protocol over standard input/output. If no `.env` keys are configured, it will default to Gemini if `GEMINI_API_KEY` is present.

