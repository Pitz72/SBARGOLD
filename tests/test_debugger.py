import sys
import os
import io
from contextlib import redirect_stdout

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_debugger():
    code = """
    SBARGOLD# Test Debugger
    x SBARGOLD= 10
    SBARGOLD! "Debug Test"
    """
    
    print("--- Code ---")
    print(code)
    
    print("\n--- Output (Debug Mode) ---")
    
    # Capture stdout to verify debug output
    f = io.StringIO()
    with redirect_stdout(f):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter()
        # Enable debug mode
        interpreter.interpret(program, debug=True)
    
    output = f.getvalue()
    print(output)
    
    if "[DEBUG] Executing:" in output:
        print("\nDebugger Test PASSED!")
    else:
        print("\nDebugger Test FAILED: Debug output not found.")

if __name__ == "__main__":
    test_debugger()
