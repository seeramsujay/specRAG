# SpecRAG VS Code Extension

**SpecRAG Hardware Auditor** is a VS Code extension designed to intercept code edits/saves and run real-time hardware validation audits against component datasheets using the SpecRAG MCP Server.

## 🚀 Features

- **Real-Time Validation**: Runs a RAG-powered LLM analysis on your active firmware file to detect datasheet constraint violations.
- **Visual Diagnostics**: Renders red "squiggly" lines (errors) and orange lines (warnings) under the exact line of code violating datasheet parameters.
- **Premium Hover Citations**: Hovering over a diagnostic line opens a rich Markdown popup detailing the violation and displaying the exact datasheet page, section, or table reference.
- **Quick Fix Code Actions**: Clicking the lightbulb on a violation provides quick actions, such as commenting out the offending code or inserting a `FIXME` comment.
- **Interactive Status Bar**: Shows the current audit state (`Ready`, `Auditing...`, `Success`, `Violations Found`) directly in the status bar. Clicking it manually triggers validation.

---

## 🛠️ Configuration & Setup

You can configure the extension in your VS Code settings under `specrag.*`:

| Setting | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `specrag.pythonPath` | `string` | `"python"` | Path to the Python interpreter (e.g., `python`, `python3`, or virtual environment binary). |
| `specrag.serverPath` | `string` | `""` | Absolute path to `Server.py`. If left empty, the extension automatically locates it in the workspace root. |
| `specrag.defaultComponent` | `string` | `"MPU6050"` | Fallback hardware component name if no `@component` annotation is found in the code. |
| `specrag.validationTrigger` | `enum` | `"onSave"` | Trigger event for validation: `onSave`, `onType` (debounced), or `manual`. |
| `specrag.debouncingDelay` | `integer` | `1500` | Delay (ms) before triggering validation after you stop typing (only when trigger is set to `onType`). |
| `specrag.useMock` | `boolean` | `false` | If true, runs validation against the mock server tool (`validate_hardware_code_mock`) for offline testing. |

---

## 📖 Declaring Target Hardware Components

To audit a file against a specific hardware datasheet, declare it using the `@component` inline annotation near the top of the file:

```cpp
// @component MPU6050
#include <Wire.h>

void setup() {
    Wire.begin();
    // SpecRAG will validate this file against the MPU6050 datasheet context
}
```

Supported comment formats:
- Single-line: `// @component MPU6050`
- Multi-line: `/* @component MPU6050 */`

If no annotation is found, SpecRAG falls back to your `specrag.defaultComponent` setting.

---

## 💻 Manual Commands

Use the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) to trigger manual tasks:
- `SpecRAG: Validate Current File` (Runs validation immediately and shows the server logs panel)
- `SpecRAG: Clear Diagnostics` (Clears all red squigglies and status indicators)
