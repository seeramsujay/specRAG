import os
import sys
import json
import subprocess
import unittest

# Ensure the workspace root is in python path so we can import MCP_Server
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, workspace_root)


class TestSpecRAGMCP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Determine path to the python executable and MCP_Server script
        cls.workspace_root = workspace_root
        cls.venv_python = os.path.join(cls.workspace_root, ".venv", "bin", "python")
        if not os.path.exists(cls.venv_python):
            cls.venv_python = sys.executable
        cls.server_script = os.path.join(cls.workspace_root, "MCP_Server.py")

        # Start server subprocess
        cls.process = subprocess.Popen(
            [cls.venv_python, cls.server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        cls.req_id = 1

        # Perform handshake
        cls.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        )
        cls.send_notification("notifications/initialized")

    @classmethod
    def tearDownClass(cls):
        if cls.process:
            cls.process.stdin.close()
            cls.process.stdout.close()
            cls.process.stderr.close()
            cls.process.terminate()
            cls.process.wait()

    @classmethod
    def send_request(cls, method, params=None):
        current_id = cls.req_id
        msg = {
            "jsonrpc": "2.0",
            "id": current_id,
            "method": method,
            "params": params or {},
        }
        cls.req_id += 1
        cls.process.stdin.write(json.dumps(msg) + "\n")
        cls.process.stdin.flush()

        # Read responses until we get the one with matching ID
        while True:
            line = cls.process.stdout.readline()
            if not line:
                return None
            try:
                resp = json.loads(line)
                if resp.get("id") == current_id:
                    return resp
            except json.JSONDecodeError:
                continue

    @classmethod
    def send_notification(cls, method, params=None):
        msg = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        cls.process.stdin.write(json.dumps(msg) + "\n")
        cls.process.stdin.flush()

    def test_01_mcp_server_boot(self):
        """Test 1: Verify MCP server successfully booted and process is running."""
        self.assertIsNotNone(self.process)
        self.assertIsNone(self.process.poll())

    def test_02_tool_validate_hardware_code_mock_exists(self):
        """Test 2: Verify mock validation tool is registered by the server."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        tool_names = [t.get("name") for t in tools]
        self.assertIn("validate_hardware_code_mock", tool_names)

    def test_03_tool_validate_hardware_code_exists(self):
        """Test 3: Verify real validation tool is registered by the server."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        tool_names = [t.get("name") for t in tools]
        self.assertIn("validate_hardware_code", tool_names)

    def test_04_schema_mock_code_snippet(self):
        """Test 4: Verify mock validation tool schema includes 'code_snippet'."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        mock_tool = next(
            t for t in tools if t.get("name") == "validate_hardware_code_mock"
        )
        properties = mock_tool.get("inputSchema", {}).get("properties", {})
        self.assertIn("code_snippet", properties)

    def test_05_schema_mock_component(self):
        """Test 5: Verify mock validation tool schema includes 'component'."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        mock_tool = next(
            t for t in tools if t.get("name") == "validate_hardware_code_mock"
        )
        properties = mock_tool.get("inputSchema", {}).get("properties", {})
        self.assertIn("component", properties)

    def test_06_schema_real_code_snippet(self):
        """Test 6: Verify real validation tool schema includes 'code_snippet'."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        real_tool = next(t for t in tools if t.get("name") == "validate_hardware_code")
        properties = real_tool.get("inputSchema", {}).get("properties", {})
        self.assertIn("code_snippet", properties)

    def test_07_schema_real_component(self):
        """Test 7: Verify real validation tool schema includes 'component'."""
        resp = self.send_request("tools/list")
        tools = resp.get("result", {}).get("tools", [])
        real_tool = next(t for t in tools if t.get("name") == "validate_hardware_code")
        properties = real_tool.get("inputSchema", {}).get("properties", {})
        self.assertIn("component", properties)

    def test_08_scenario_1_incorrect_register_write(self):
        """Test 8: Benchmark Scenario 1 (Incorrect Register Write - High Severity)."""
        code = """void setup() {
  Wire.beginTransmission(0x68);
  Wire.write(0x75);
  Wire.write(0x00);
  Wire.endTransmission();
}"""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": code, "component": "MPU6050"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "error")
        self.assertEqual(data.get("severity"), "high")
        self.assertEqual(data.get("line"), 4)
        self.assertIn("WHO_AM_I", data.get("citation"))

    def test_09_scenario_2_missing_i2c_start(self):
        """Test 9: Benchmark Scenario 2 (Missing I2C Start - Medium Severity)."""
        code = """void init_sensor() {
  Wire.write(0x2D);
  Wire.write(0x08);
}"""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": code, "component": "ADXL345"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "error")
        self.assertEqual(data.get("severity"), "medium")
        self.assertEqual(data.get("line"), 2)
        self.assertIn("beginTransmission", data.get("citation"))

    def test_10_scenario_3_pin_mode_mismatch(self):
        """Test 10: Benchmark Scenario 3 (Pin Mode Mismatch - Low Severity)."""
        code = """void setup() {
  pinMode(3, INPUT);
}
void loop() {
  digitalWrite(3, HIGH);
}"""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": code, "component": "Arduino"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "error")
        self.assertEqual(data.get("severity"), "low")
        self.assertEqual(data.get("line"), 5)
        self.assertIn("pinMode", data.get("citation"))

    def test_11_scenario_4_valid_configuration(self):
        """Test 11: Benchmark Scenario 4 (Valid Configuration - Success)."""
        code = """void setup() {
  pinMode(3, OUTPUT);
}
void loop() {
  digitalWrite(3, HIGH);
}"""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": code, "component": "Arduino"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "success")
        self.assertIsNone(data.get("severity"))
        self.assertIsNone(data.get("line"))

    def test_12_mock_default_fallback(self):
        """Test 12: Verify mock validation fallback logic when code does not match predefined scenarios."""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": "void loop() {}", "component": "Generic"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "error")
        self.assertEqual(data.get("severity"), "high")
        self.assertEqual(data.get("line"), 42)
        self.assertIn("Register 0x3F", data.get("message"))

    def test_13_mock_empty_code_snippet(self):
        """Test 13: Verify mock validation behaves correctly when snippet is empty."""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code_mock",
                "arguments": {"code_snippet": "", "component": "Generic"},
            },
        )
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        data = json.loads(content[0].get("text"))
        self.assertEqual(data.get("status"), "error")
        self.assertEqual(data.get("line"), 42)

    def test_14_real_missing_args(self):
        """Test 14: Verify real validation tool returns validation error when arguments are missing."""
        resp = self.send_request("tools/call", {"name": "validate_hardware_code"})
        self.assertTrue(resp.get("result", {}).get("isError", False))
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        self.assertIn("validation error", content[0].get("text"))

    def test_15_real_missing_code_snippet(self):
        """Test 15: Verify real validation tool returns validation error when 'code_snippet' is missing."""
        resp = self.send_request(
            "tools/call",
            {"name": "validate_hardware_code", "arguments": {"component": "MPU6050"}},
        )
        self.assertTrue(resp.get("result", {}).get("isError", False))
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        self.assertIn("validation error", content[0].get("text"))

    def test_16_real_missing_component(self):
        """Test 16: Verify real validation tool returns validation error when 'component' is missing."""
        resp = self.send_request(
            "tools/call",
            {
                "name": "validate_hardware_code",
                "arguments": {"code_snippet": "void loop() {}"},
            },
        )
        self.assertTrue(resp.get("result", {}).get("isError", False))
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        self.assertIn("validation error", content[0].get("text"))

    def test_17_call_unknown_tool(self):
        """Test 17: Verify JSON-RPC error response when calling an unknown tool."""
        resp = self.send_request(
            "tools/call",
            {
                "name": "invalid_tool_name",
                "arguments": {"code_snippet": "void loop() {}"},
            },
        )
        self.assertTrue(resp.get("result", {}).get("isError", False))
        content = resp.get("result", {}).get("content", [])
        self.assertEqual(len(content), 1)
        self.assertIn("Unknown tool", content[0].get("text"))

    def test_18_get_agent_system_prompt(self):
        """Test 18: Directly test get_agent_system_prompt returns the text of Archives/AGENT.md."""
        from MCP_Server import get_agent_system_prompt

        prompt = get_agent_system_prompt()
        self.assertIn("Hardware Auditor", prompt)
        self.assertIn("REGISTER-MAP INSPECTION RULES", prompt)

    def test_19_evaluate_logic_mock_direct(self):
        """Test 19: Directly test the evaluate_logic_mock helper logic."""
        from MCP_Server import evaluate_logic_mock

        code = """void setup() {
  Wire.beginTransmission(0x68);
  Wire.write(0x75);
  Wire.write(0x00);
  Wire.endTransmission();
}"""
        res = evaluate_logic_mock(code, "test context")
        self.assertEqual(res.get("status"), "error")
        self.assertEqual(res.get("severity"), "high")
        self.assertEqual(res.get("line"), 4)


if __name__ == "__main__":
    unittest.main()
