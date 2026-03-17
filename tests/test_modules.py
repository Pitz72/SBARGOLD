import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_modules():
    # Ensure module file exists (created by previous step)
    
    code = """
    SBARGOLD# Test Modules
    SBARGOLD! "Importing module..."
    SBARGOLD| "tests/my_module.sbg"
    
    SBARGOLD! "Calling module function..."
    SBARGOLD$ greet "Tester"
    
    SBARGOLD! "Accessing module variable..."
    SBARGOLD! module_var
    """
    
    print("--- Code ---")
    print(code)
    
    print("\n--- Output ---")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(program)
    
    print("\nModules Test PASSED if you see Module Loaded, Hello from Module, and 42")

if __name__ == "__main__":
    test_modules()
