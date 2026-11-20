# specRAG: Architectural Review & Firmware Intelligence Roadmap (future.md)

---

## 1. Architectural Code Review & Current State Analysis

SpecRAG pioneers real-time hardware datasheet validation directly inside modern developer IDEs. By coupling a vector-based semantic retrieval engine over PDF component specifications with a **Model Context Protocol (MCP)** server, SpecRAG intercepts embedded C/C++ and Arduino source code as it is written, flagging electrical discrepancies (e.g., driving 5V logic directly into 3.3V GPIO, clock frequency violations, missing pull-up resistor requirements) before physical PCBs are energized.

### Architectural Strengths
- **MCP Decoupling:** Decouples the AI diagnostic backend from the VS Code client, allowing the LLM reasoning and dense vector embeddings to run remotely or across distributed compute nodes.
- **Pydantic Structured Output Enforcement:** Enforces deterministic JSON output guarantees via Gemini 1.5 Flash structured schemas (`HardwareValidationResult`), preventing freeform chat hallucination from breaking editor diagnostics.
- **Multi-Provider Fallback:** Built-in modular LLM providers supporting Gemini, OpenAI, and Azure OpenAI alongside offline mock test runners.

### Key Technical Limitations & Code Smell
1. **Unstructured PDF Table Ingestion:** Datasheet tables (such as pin multiplexing registers and electrical characteristics) often get fragmented by naive chunking algorithms, losing column alignment and condition thresholds (e.g., $V_{IH}$ minimum at $V_{DD}=3.0\text{V}$).
2. **Synchronous File-Save Bottlenecks:** Triggering full RAG lookups synchronously on file save can introduce latency ($>1.5\text{s}$) in the developer typing loop.
3. **Lack of Pin-State Context Graph:** The auditor currently operates on isolated snippets rather than building an aggregated circuit state graph tracking netlists, pin assignments, and power rails across the entire firmware project.

---

## 2. Strategic Engineering Roadmap

```mermaid
flowchart TD
    subgraph Phase 1: High-Fidelity Datasheet Ingestion
        P1A[Multimodal Vision OCR for Tables] --> P1B[Parametric Pinout Knowledge Graph]
        P1B --> P1C[Hierarchical Chunking with Register Maps]
    end

    subgraph Phase 2: Asynchronous IDE Language Server (LSP)
        P2A[LSP Diagnostic Background Worker] --> P2B[Incremental Abstract Syntax Tree (AST) Parser]
        P2B --> P2C[Sub-100ms In-Memory Vector Cache]
    end

    subgraph Phase 3: Hardware In-The-Loop Simulation
        P3A[Wokwi / QEMU Virtual Testbed Bridge] --> P3B[Automated Register Map Generation svd2rust]
        P3B --> P3C[Automated Peripheral Configuration Assertions]
    end

    subgraph Phase 4: Offline Airgapped Edge Execution
        P4A[Quantized On-Device SLM: Llama 3 / Qwen] --> P4B[Local Vector DB via Chroma/sqlite-vec]
        P4B --> P4C[Zero-Telemetry Aerospace & Defense Mode]
    end

    Phase 1 --> Phase 2
    Phase 2 --> Phase 3
    Phase 3 --> Phase 4
```

---

## 3. Detailed Milestone Execution Plan

### Milestone 1: Multimodal Datasheet Parsing & Parametric Graph
- [ ] **Multimodal Table Extractor:** Integrate vision-language models to extract complex electrical characteristic tables, timing diagrams, and pin multiplexing matrices without column degradation.
- [ ] **Parametric Component Graph:** Store extracted parameters (min/max supply voltage, sink/source current limits, default pull-ups, alternate pin functions) in a structured graph database (Neo4j / SQLite) rather than pure unstructured vector chunks.
- [ ] **Automated SVD Ingestion:** Ingest standard ARM CMSIS-SVD (System View Description) XML files to auto-ground register definitions and bitfields.

### Milestone 2: Background LSP Diagnostics & Incremental AST Analysis
- [ ] **Tree-Sitter C/C++ AST Hook:** Replace crude regex/text-matching with Tree-Sitter AST inspection to track GPIO register manipulation (`PORTB |= (1 << PB5)`) and baud rate calculations dynamically.
- [ ] **Debounced Background Evaluation:** Implement debounced background queries with local in-memory LRU caching to push squiggly warnings into VS Code within $<150\text{ms}$.
- [ ] **Code Action Quick-Fixes:** Provide IDE quick-actions (e.g., "Insert 4.7kΩ pull-up note", "Clamp ADC input scaling factor") directly in the VS Code editor context menu.

### Milestone 3: Hardware In-The-Loop (HIL) & SVD Code Generation
- [ ] **Zero-Shot Peripheral Driver Synthesis:** Automatically generate typed Rust `svd2rust` or C++ header register maps from datasheet PDFs.
- [ ] **Wokwi Simulation Integration:** Automatically validate firmware against virtual Wokwi breadboard circuits, simulating I2C ACK responses and signal rise times before flashing.

### Milestone 4: Air-Gapped Local Inference for Defense & Aerospace
- [ ] **Quantized Local SLM Ingestion:** Enable offline inference with GGUF-quantized models (e.g. Qwen 2.5 Coder 7B) running locally via `llama-cpp-python`.
- [ ] **Zero-Network Airgap Profile:** Ensure 100% offline verification with zero outbound network telemetry for high-security embedded defense environments.
