Node 1: RAG Data Engineering & Vector Architecture
Objective: Serve as the definitive "Ground Truth" engine by converting raw hardware datasheets into a highly accurate, semantically searchable vector database.

Core Architecture Tasks:

Data Ingestion & Sanitization: Finalize and maintain the ingest.py and clean_markdown.py scripts. Ensure the automated pipeline reliably strips out HTML artifacts, block diagram text, and revision histories to prevent context window pollution.

Semantic Chunking: Implement LangChain’s MarkdownHeaderTextSplitter to intelligently divide the cleaned Markdown. Ensure technical tables remain firmly attached to their hierarchical headers so critical context is never lost during retrieval.

Embedding & Indexing: Route the chunked datasheet data through an embedding model (e.g., Azure OpenAI text-embedding-3-small) and index it into a Vector Database (Azure AI Search or ChromaDB).

Retrieval Algorithm: Engineer a hybrid search algorithm (combining keyword and vector search) to reliably retrieve the exact hardware constraints when queried for specific components and pins.

Deliverable / API Contract: A standalone Python retrieval function: retrieve_context(component_name: str, query: str) -> str.

Asynchronous Unblocker: Create a dummy version of this script that returns hardcoded text (e.g., "Absolute Maximum VIN is 3.3V") so the backend and AI nodes can test their systems immediately.

Node 2: AST Parsing & Backend Infrastructure
Objective: Act as the central router and data filter, ensuring the AI is only fed relevant hardware logic rather than thousands of lines of useless boilerplate code.

Core Architecture Tasks:

Infrastructure Setup: Deploy the central API server (FastAPI or a Model Context Protocol server) to listen for incoming requests from the VS Code client. Manage API keys, routing, and error handling.

AST Implementation: Integrate a parsing library like Tree-sitter to convert incoming C++ code into an Abstract Syntax Tree.

Logic Filtering: Target Arduino and ESP32 C++ syntax to programmatically extract only the hardware-relevant lines (e.g., #define, pinMode(), analogRead(), digitalWrite()).

Data Routing: Receive the parsed C++ code, call Node 1's retrieval function for the required datasheet specs, and package both into a unified payload for Node 3.

Deliverable / API Contract: A live, local REST endpoint (e.g., POST /api/check-code) that accepts raw C++ files and returns the final JSON error report.

Asynchronous Unblocker: Deploy a mock server on Day 1 that accepts incoming network traffic and simply returns a static, hardcoded JSON string so the frontend developer can build the UI without waiting for the real logic.

Node 3: AI Engineering & Reasoning
Objective: Constrain the Large Language Model mathematically so it acts as a deterministic, zero-hallucination hardware auditor rather than a conversational chatbot.

Core Architecture Tasks:

Prompt Engineering: Design the core system prompt architecture that fuses Node 2's filtered C++ code with Node 1's retrieved Markdown tables, instructing the LLM on exactly how to cross-reference the data.

Structured Output Enforcement: Utilize a validation library (like Pydantic or LangChain Output Parsers) to force the LLM to strictly output a predefined JSON schema containing the error severity, line number, and datasheet citation. Chatty text must be strictly prohibited.

Few-Shot Training: Build prompt examples demonstrating specific constraint violations—such as incorrectly implementing a bidirectional 3.3V to 5V logic level shifter in a Wokwi simulation—to calibrate the AI's reasoning capabilities.

Evaluation Suite: Create an automated testing script loaded with intentional hardware code errors to continuously benchmark the model's accuracy and prove a 0% hallucination rate.

Deliverable / API Contract: A Python function evaluate_logic(filtered_code: str, vector_context: str) -> dict that strictly outputs the agreed-upon JSON schema.

Asynchronous Unblocker: Provide a dummy script that ignores the input entirely and just spits out a perfectly formatted JSON error, allowing the backend server to test its routing logic.

Node 4: IDE Client & Developer UX
Objective: Build the developer-facing interface that seamlessly intercepts code saves and renders hardware constraints directly into the IDE environment.

Core Architecture Tasks:

Extension Architecture: Develop the TypeScript VS Code extension utilizing the Language Server Protocol (LSP) and the VS Code Diagnostics API.

Event Handling & Debouncing: Write the logic to capture the active editor text. Implement debouncing so the extension only pings the backend server after the developer stops typing for a set duration, preventing API spam.

Diagnostic Rendering: Parse the incoming JSON from the backend and map it to the active text editor to draw red "squiggly" lines under the exact line of violating code.

Hover & Code Actions: Build Hover Providers to display the actual datasheet citation when the user hovers over the error. Implement a "Quick Fix" lightbulb action to suggest code corrections directly in the editor.

Deliverable / API Contract: The packaged .vsix VS Code extension that handles all HTTP requests and UI rendering autonomously.

Asynchronous Unblocker: Create a dummy JSON file locally that perfectly mimics the backend response schema, allowing complete UI and Diagnostic API development entirely offline.
