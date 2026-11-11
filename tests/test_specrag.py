import re
from pathlib import Path
from clean_markdown import sanitize_to_markdown

def test_sanitize_to_markdown():
    raw_html = "<h1>Register Description</h1><p>Test <b>text</b></p><script>alert(1)</script>"
    md = sanitize_to_markdown(raw_html)
    assert "# Register Description" in md
    assert "Test **text**" in md
    assert "alert" not in md

def test_sanitize_empty():
    assert sanitize_to_markdown("") == ""

def test_hardware_patterns():
    from ast_parser import HW_FUNCTIONS, HW_OBJECTS, REG_PATTERN
    assert "pinMode" in HW_FUNCTIONS
    assert "digitalWrite" in HW_FUNCTIONS
    assert "Serial" in HW_OBJECTS
    assert REG_PATTERN.match("PORTA") is not None
    assert REG_PATTERN.match("DDRB") is not None
    assert REG_PATTERN.match("GPIO_ENABLE") is not None
    assert REG_PATTERN.match("INVALID_REG_XYZ") is None

def test_requirements_file():
    req_file = Path("requirements.txt")
    assert req_file.exists()
    content = req_file.read_text()
    assert len(content) > 0
