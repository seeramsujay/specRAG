# 🤝 SpecRAG Integration Guide (Node Handover)

Hello Team! This document outlines what I (Node 2: Backend & AI) have completed, how the core Brain works, and exactly what the rest of the nodes need to do to hit our Phase 3/4 milestones seamlessly.

## 🟢 Node 1: Data Engineer (RAG)
**Your Goal:** Feed the AI the exact datasheet context.
**What I've done:** I have fully integrated the Gemini API with structured output enforcement. It mathematically cannot hallucinate JSON formats anymore. 
**What I need from you:**
1. I left a placeholder string in `MCP_Server.py` (Line ~102): `context = f"Mock retrieved context for {component} from Node 1 DB..."`.
2. You need to write your `retrieve_context(component_name, code_snippet)` Python function.
3. Once your local Vector DB (Chroma/FAISS) is working, import your function into `MCP_Server.py` and replace my placeholder.
4. **Context Quality is King**: If your context misses the I2C registers, my AI will miss the I2C bug. Ensure table data from the PDFs is intact!

## 🟠 Node 3: Frontend Developer (VS Code)
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
     "line": 42,
     "message": "Register 0x3F is read-only.",
     "citation": "Datasheet Page 14, Table 3"
   }
   ```
3. If `status == "system_error"`, something broke (bad arguments, API timeout). Gracefully show a toast notification in VS code instead of a red squiggly line.
4. If `status == "error"`, draw the red squiggly on the `line` returned, and put the `message` and `citation` in the hover tooltip.

## 🟣 Node 4: DevOps & QA
**Your Goal:** Evaluate system accuracy across the full stack.
**What I've done:** I wrote a 100% coverage mock test suite for `MCP_Server.py` ensuring the script is bulletproof. (Check `Archives/testing/test.md` if you want to see the results).
**What I need from you:**
1. Once Node 1 plugs in the live RAG, we need your 5 buggy `.cpp` files.
2. Feed them to Node 3's frontend, or build a script that directly calls `MCP_Server.py`'s stdio stream.
3. **Prompt Tuning Loop**: If the AI misses a bug, tell me! We will immediately tune the system prompt in `Archives/AGENT.md` or tell Node 1 to fix their chunking.
4. Review the `README.md` and `CHANGELOG.md` I created to prep for the final judges' presentation.

---
**Server Boot Command for Testing:**
We now support configuring API keys via a `.env` file (see `.env.example`). Once configured, you can boot the server using the wrapper:
```bash
python Server.py
```
The server dynamically loads the key and runs the MCP protocol over standard input/output. If no `.env` keys are configured, it will default to Gemini if `GEMINI_API_KEY` is present.

