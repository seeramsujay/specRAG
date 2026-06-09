# 📄 Node 3: AI Engineering & Reasoning Handout

This handout outlines the architecture, constraints, benchmark test scenarios, and integration details established for the Node 3 deliverables.

---

## 🎯 Phase Overview
The objective of Node 3 is to constrain the LLM mathematically to function as a deterministic, zero-hallucination hardware validator. To achieve this, we have:
1. **Restored the Agent Persona (`Archives/AGENT.md`)** to define strict inspection rules.
2. **Re-established the Evaluation Suite (`Archives/testing/test_runner.py`)** with an automated, dry-run hardware bug benchmark.
3. **Simulated Hardware Violations in `MCP_Server.py`** to run tests without live API costs.

---

## 🤖 1. System Persona Instruction File (`Archives/AGENT.md`)
The instruction file has been restored to configure the agent with a strict hardware auditor role. It details the following domains:

*   **Register-Map Inspection Rules**: Ensuring writes target valid/accessible registers, enforcing read-only constraints, and validating bitmask ranges.
*   **Pin Configuration & Logic-Level Schemas**: Verifying pin modes (`INPUT`/`OUTPUT`) match the hardware configurations and flagging logic-level voltage mismatches (e.g., direct 3.3V vs 5V connections without level shifters).
*   **I2C Write/Read Constraints**: Checking I2C addresses (e.g., `0x68` vs `0x69` for `MPU6050`), enforcing proper write transactions (always bounded by `beginTransmission` and `endTransmission`), and verifying read configurations.
*   **Response Schema**: Forcing raw JSON output (no markdown wrappers) matching the schema:
    ```json
    {
      "status": "error" | "success",
      "severity": "high" | "medium" | "low" | null,
      "line": <int | null>,
      "message": "<string: 1-sentence-explanation>",
      "citation": "<string: datasheet section, page number, table, or register name>"
    }
    ```
*   **Citation Mandate**: Precise citation of datasheet sections, pages, or register names is strictly mandated for any identified bug (`high`, `medium`, or `low` severity).

---

## 🧪 2. Evaluation Suite & Benchmark (`Archives/testing/test_runner.py`)
We have implemented 4 new test cases under `Archives/testing/test_runner.py` representing a predefined benchmark of hardware bug scenarios. The mock validation logic in `MCP_Server.py` (`evaluate_logic_mock`) dynamically matches the code snippet and parses line numbers:

### Predefined Scenarios

1.  **Incorrect Register Write (High Severity)**
    *   *Bug*: Writing `0x00` to register `0x75` (`WHO_AM_I`), which is read-only.
    *   *Code Snippet*:
        ```cpp
        void setup() {
          Wire.beginTransmission(0x68);
          Wire.write(0x75);
          Wire.write(0x00);
          Wire.endTransmission();
        }
        ```
    *   *Result*: `status: "error"`, `severity: "high"`, `line: 4`, `citation: "Datasheet Section 10.4, Register 0x75 (WHO_AM_I) description"`.

2.  **Missing I2C Start (Medium Severity)**
    *   *Bug*: Calling `Wire.write()` without a preceding `Wire.beginTransmission()`.
    *   *Code Snippet*:
        ```cpp
        void init_sensor() {
          Wire.write(0x2D);
          Wire.write(0x08);
        }
        ```
    *   *Result*: `status: "error"`, `severity: "medium"`, `line: 2`, `citation: "Arduino Wire Library Reference: beginTransmission is required before write."`.

3.  **Pin Mode Mismatch (Low Severity)**
    *   *Bug*: Performing a `digitalWrite` on a pin configured as `INPUT`.
    *   *Code Snippet*:
        ```cpp
        void setup() {
          pinMode(3, INPUT);
        }
        void loop() {
          digitalWrite(3, HIGH);
        }
        ```
    *   *Result*: `status: "error"`, `severity: "low"`, `line: 5`, `citation: "Arduino Reference: pinMode must be set to OUTPUT for digitalWrite."`.

4.  **Valid Configuration (Success Case)**
    *   *Behavior*: Correct pin setup and write operations.
    *   *Code Snippet*:
        ```cpp
        void setup() {
          pinMode(3, OUTPUT);
        }
        void loop() {
          digitalWrite(3, HIGH);
        }
        ```
    *   *Result*: `status: "success"`, `severity: null`, `line: null`, `citation: ""`.

---

## ⚡ 3. Running the Tests
To execute the suite (19 tests covering tool registration, input validation, client parsing, and the new benchmark scenarios):

```bash
python3 Archives/testing/test_runner.py
```

### Output
```text
Ran 19 tests in 1.157s

OK
```

---

## 🤝 4. Integration Guidelines for Other Nodes

*   **Node 2 (AST & Backend)**: Route filtered C++ code directly into the MCP Server tools. Use `validate_hardware_code_mock` for dry runs or `validate_hardware_code` for production.
*   **Node 1 (RAG Data)**: Ensure I2C addresses, register numbers, and pin limits are correctly indexed in ChromaDB so that `retrieve_context` retrieves the relevant tables.
*   **Node 4 (IDE Client)**: Hover diagnostic tooltip should extract the exact `line` for the diagnostic, displaying the `message` and the `citation` directly.
