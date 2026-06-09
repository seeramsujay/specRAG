# Changelog

All notable changes to the **SpecRAG** project will be documented in this file.
## [Unreleased] - 2026-06-10

### Added
- **Node 2 Logic Filter**: Implemented `ast_parser.py` and integrated it into `MCP_Server.py`. The MCP server now uses Abstract Syntax Tree (AST) parsing to filter out irrelevant code before querying the LLM, significantly improving accuracy and token efficiency.
- **RAG Integration**: Integrated `rag.py` for smart datasheet retrieval.
- **Static Analysis**: Added support for `mypy`, `pylint`, and `flake8` for robust code quality checking.
## [Unreleased] - 2026-04-07

### Added
- **Gemini API Integration**: Implemented live `google-generativeai` support in `MCP_Server.py`.
- **Structured JSON Outputs**: Integrated Pydantic `HardwareValidationResult` schema to mathematically guarantee LLM JSON responses match Node 3's required contract.
- **Project Workflows**: Created `Future_Steps.md`, `task.md`, and this `CHANGELOG.md` to track Hackathon milestones.
- **Professional Documentation**: Added a comprehensive, Hacker News-worthy `README.md` complete with an architecture diagram and VS Code mockup.
- **Robust Test Suite**: Established `Archives/testing/test_runner.py` for fully mocked, multi-scenario error testing of the MCP server.

### Changed
- **Token Efficiency**: Refactored `AGENT.md` and `ROADMAP.md` into highly condensed markup formats to minimize LLM token usage context drops.
- **MCP Server Safety**: 
  - Substituted all `print` calls with `logging` routed to `sys.stderr`, preventing JSON-RPC corruption via `stdout`.
  - Fortified `validate_hardware_code` against null pointers and missing argument payloads.
- **Environment Stack**: Updated `requirements.txt` to properly branch `mcp`, `pydantic` and vector/RAG stack dependencies (`chromadb`, `pypdf`, `numpy`).

### Fixed
- **Path Resolution Bug**: Corrected a crash in `MCP_Server.py` where `get_agent_system_prompt()` assumed it was executed from the same flat directory as `agent.md`. Now correctly resolves to `Archives/AGENT.md` with fallback heuristics.
