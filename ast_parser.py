import logging
import re
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser, Node

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Tree-sitter C++ parser
try:
    CPP_LANGUAGE = Language(tscpp.language())
    parser = Parser(CPP_LANGUAGE)
    logger.info("Successfully initialized Tree-sitter C++ parser.")
except Exception as e:
    logger.error("Failed to initialize Tree-sitter C++ parser: %s", e)
    parser = None

# Set of standard Arduino/ESP32 hardware control functions
HW_FUNCTIONS = {
    "pinMode", "digitalWrite", "digitalRead", "analogWrite", "analogRead",
    "analogReference", "attachInterrupt", "detachInterrupt",
    "delay", "delayMicroseconds", "millis", "micros",
    "pulseIn", "pulseInLong", "shiftIn", "shiftOut", "tone", "noTone"
}

# Key objects representing hardware protocol or interface classes
HW_OBJECTS = {"Serial", "Wire", "SPI", "I2C", "TwoWire"}

# Regex matching common AVR/ESP32 hardware registers (typically all caps)
REG_PATTERN = re.compile(
    r"^(PORT[A-Z]|DDR[A-Z]|PIN[A-Z]|TCCR[0-9]|TCNT[0-9]|OCR[0-9]|TIMSK|"
    r"ADMUX|ADCSRA|ADCL|ADCH|SPCR|SPSR|SPDR|TWBR|TWSR|TWAR|TWDR|TWCR|"
    r"GPIO_[A-Z0-9_]+)$"
)

def get_node_text(node: Node, source: bytes) -> str:
    """Helper to extract text slice for a given AST node."""
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")

def is_hardware_call(node: Node, source: bytes) -> bool:
    """Checks if a call_expression is hardware-related."""
    if node.type != "call_expression":
        return False
    
    callee = node.child_by_field_name("function")
    if not callee:
        return False
    
    callee_text = get_node_text(callee, source)
    
    # 1. Direct function name check
    if callee_text in HW_FUNCTIONS:
        return True
    
    # 2. Object method check (e.g., Wire.begin, Serial.print)
    if callee.type == "field_expression":
        obj = callee.child_by_field_name("argument")
        if obj:
            obj_text = get_node_text(obj, source)
            if obj_text in HW_OBJECTS:
                return True
                
    return False

def is_register_access(node: Node, source: bytes) -> bool:
    """Checks if an expression involves direct register manipulation."""
    if node.type == "assignment_expression":
        left = node.child_by_field_name("left")
        if left:
            left_text = get_node_text(left, source)
            if REG_PATTERN.match(left_text):
                return True
    elif node.type == "identifier":
        ident_text = get_node_text(node, source)
        if REG_PATTERN.match(ident_text):
            return True
    return False

def collect_hardware_symbols_and_nodes(node: Node, source: bytes, hw_nodes: set, hw_symbols: set):
    """
    Pass 1: Recursively traverses the AST to collect hardware-relevant nodes
    and record all variable identifiers used in those hardware statements.
    """
    is_hw = False
    
    # Preprocessor includes and defines are always kept
    if node.type in ("preproc_include", "preproc_def"):
        is_hw = True
        if node.type == "preproc_def":
            name_node = node.child_by_field_name("name")
            if name_node:
                hw_symbols.add(get_node_text(name_node, source))
    
    # Identify calls like pinMode() or Wire.begin()
    elif is_hardware_call(node, source):
        is_hw = True
        # Track argument variables (e.g. ledPin in digitalWrite(ledPin, HIGH))
        arg_list = node.child_by_field_name("arguments")
        if arg_list:
            for arg in arg_list.children:
                if arg.type == "identifier":
                    hw_symbols.add(get_node_text(arg, source))
                    
    # Identify direct register manipulation (e.g. PORTB |= 0x01)
    elif is_register_access(node, source):
        is_hw = True
        right = node.child_by_field_name("right")
        if right:
            def collect_idents(n):
                if n.type == "identifier":
                    hw_symbols.add(get_node_text(n, source))
                for c in n.children:
                    collect_idents(c)
            collect_idents(right)
                    
    if is_hw:
        hw_nodes.add(node)
        
    for child in node.children:
        collect_hardware_symbols_and_nodes(child, source, hw_nodes, hw_symbols)

def identify_kept_nodes(node: Node, source: bytes, hw_nodes: set, hw_symbols: set, kept_nodes: set):
    """
    Pass 2: Marks which nodes should be kept.
    A node is kept if it is directly hardware-related, defines a variable
    referenced in a hardware call, or has a descendant that is kept.
    """
    is_hw_decl = False
    if node.type == "declaration":
        # Keep variable declarations if they initialize a hardware symbol (e.g. const int pin = 13)
        for child in node.children:
            if child.type == "init_declarator":
                var_name_node = child.child_by_field_name("declarator")
                if var_name_node:
                    var_name = get_node_text(var_name_node, source)
                    if var_name in hw_symbols:
                        is_hw_decl = True
                        
    # Process children first to bubble up relevance
    has_kept_descendant = False
    for child in node.children:
        identify_kept_nodes(child, source, hw_nodes, hw_symbols, kept_nodes)
        if child in kept_nodes:
            has_kept_descendant = True
            
    if node in hw_nodes or is_hw_decl or has_kept_descendant:
        kept_nodes.add(node)

def reconstruct_code(node: Node, source: bytes, kept_nodes: set, indent_level=0) -> str:
    """
    Pass 3: Reconstructs C++ code from kept nodes, preserving structure/indentation.
    """
    if node not in kept_nodes:
        return ""
        
    indent = "    " * indent_level
    
    # Statements printed as-is
    if node.type in ("preproc_include", "preproc_def", "expression_statement", "declaration", "assignment_expression"):
        text = get_node_text(node, source).strip()
        return f"{indent}{text}\n"
        
    # Function definitions (e.g. setup, loop)
    if node.type == "function_definition":
        type_node = node.child_by_field_name("type")
        decl_node = node.child_by_field_name("declarator")
        body_node = node.child_by_field_name("body")
        
        type_str = get_node_text(type_node, source) if type_node else ""
        decl_str = get_node_text(decl_node, source) if decl_node else ""
        func_sig = f"{type_str} {decl_str}".strip()
        
        body_str = ""
        if body_node and body_node in kept_nodes:
            body_str = reconstruct_code(body_node, source, kept_nodes, indent_level)
        else:
            body_str = f"{indent}{{\n{indent}}}\n"
            
        return f"{indent}{func_sig} {body_str.strip()}\n\n"
        
    # Blocks of statements
    if node.type == "compound_statement":
        lines = ["{"]
        for child in node.children:
            if child in kept_nodes and child.type not in ("{", "}"):
                child_code = reconstruct_code(child, source, kept_nodes, indent_level + 1)
                if child_code:
                    lines.append(child_code.rstrip("\n"))
        lines.append(indent + "}")
        return "\n".join(lines)
        
    # Conditionals (if statements)
    if node.type == "if_statement":
        cond_node = node.child_by_field_name("condition")
        cond_str = get_node_text(cond_node, source) if cond_node else ""
        consequence_node = node.child_by_field_name("consequence")
        alternative_node = node.child_by_field_name("alternative")
        
        consequence_str = ""
        if consequence_node and consequence_node in kept_nodes:
            if consequence_node.type == "compound_statement":
                consequence_str = reconstruct_code(consequence_node, source, kept_nodes, indent_level).strip()
            else:
                inner = reconstruct_code(consequence_node, source, kept_nodes, indent_level + 1)
                consequence_str = f"{{\n{inner}{indent}}}"
                
        alternative_str = ""
        if alternative_node and alternative_node in kept_nodes:
            if alternative_node.type == "compound_statement":
                alt_inner = reconstruct_code(alternative_node, source, kept_nodes, indent_level).strip()
            else:
                inner = reconstruct_code(alternative_node, source, kept_nodes, indent_level + 1)
                alt_inner = f"{{\n{inner}{indent}}}"
            alternative_str = "\n" + indent + "else " + alt_inner
            
        return f"{indent}if {cond_str} {consequence_str}{alternative_str}\n"

    # Loops (while, for)
    if node.type in ("while_statement", "for_statement"):
        body_node = node.child_by_field_name("body")
        header_end = body_node.start_byte if body_node else node.end_byte
        loop_header = source[node.start_byte:header_end].decode("utf-8").strip()
        
        body_str = "{}"
        if body_node and body_node in kept_nodes:
            if body_node.type == "compound_statement":
                body_str = reconstruct_code(body_node, source, kept_nodes, indent_level).strip()
            else:
                inner = reconstruct_code(body_node, source, kept_nodes, indent_level + 1)
                body_str = f"{{\n{inner}{indent}}}"
                
        return f"{indent}{loop_header} {body_str}\n"

    # Fallback default traversal
    result = []
    for child in node.children:
        if child in kept_nodes:
            child_str = reconstruct_code(child, source, kept_nodes, indent_level)
            if child_str:
                result.append(child_str)
    return "".join(result)

def filter_hardware_logic(code_snippet: str) -> str:
    """
    Parses a C++ code snippet and filters out all statements that are
    unrelated to hardware control/registers. Returns the reconstructed,
    clean C++ snippet. If parsing fails, returns the original snippet as fallback.
    """
    if not parser:
        logger.warning("Parser not initialized. Returning original code snippet.")
        return code_snippet
        
    if not code_snippet or not code_snippet.strip():
        return ""
        
    try:
        source_bytes = code_snippet.encode("utf-8")
        tree = parser.parse(source_bytes)
        
        hw_nodes = set()
        hw_symbols = set()
        collect_hardware_symbols_and_nodes(tree.root_node, source_bytes, hw_nodes, hw_symbols)
        
        # If no hardware operations were found, we provide a warning comment
        # so Node 3 can quickly report success/no errors.
        if not hw_nodes:
            return "// No hardware-relevant C++ code detected in this snippet.\n"
            
        kept_nodes = set()
        identify_kept_nodes(tree.root_node, source_bytes, hw_nodes, hw_symbols, kept_nodes)
        
        filtered_code = reconstruct_code(tree.root_node, source_bytes, kept_nodes).strip()
        return filtered_code
        
    except Exception as e:
        logger.error("Error occurred while parsing C++ code: %s. Falling back to original code.", e)
        return code_snippet
