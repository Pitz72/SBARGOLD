import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter
from sbargold_core import errors

def test_namespaces():
    print("Testing Namespace Isolation and Prefixes...")
    
    # Create a temporary module file
    module_code = """
    SBARGOLD> GREET name SBARGOLD{
        SBARGOLD! "Hello from module, " SBARGOLD& "val:" name
    SBARGOLD}
    SBARGOLD# This should NOT overwrite the parent 'data' var
    data SBARGOLD= 999
    """
    with open("tests/tmp_mod.sbg", "w") as f:
        f.write(module_code)
        
    main_code = """
    SBARGOLD# Define a variable with same name as in module
    data SBARGOLD= 123
    
    SBARGOLD! "Parent data before import: " SBARGOLD& "val:" data
    
    SBARGOLD| "tests/tmp_mod.sbg"
    
    SBARGOLD! "Parent data after import: " SBARGOLD& "val:" data
    SBARGOLD! "Module data via prefix: " SBARGOLD& "val:" tmp_mod:data
    
    SBARGOLD! "Calling module function via prefix..."
    SBARGOLD$ tmp_mod:GREET "World"
    """
    
    lexer = Lexer(main_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    
    print("\n--- Output ---")
    interpreter.interpret(program)
    
    # Assertions check
    # Parent data should still be 123
    assert interpreter.globals.get("data", None) == 123
    # Module data should be 999 with prefix
    assert interpreter.globals.get("tmp_mod:data", None) == 999
    
    print("\n[OK] Namespace Test PASSED")
    
    # Cleanup
    os.remove("tests/tmp_mod.sbg")

if __name__ == "__main__":
    try:
        test_namespaces()
    except Exception as e:
        print(f"[FAIL] Test Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
