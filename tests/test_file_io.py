import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_file_io():
    code = """
    SBARGOLD# Test File I/O
    filename SBARGOLD= "test_output.txt"
    content SBARGOLD= "Hello from SBARGOLD File I/O!"
    
    SBARGOLD! "Writing to file..."
    SBARGOLD>> filename content
    
    SBARGOLD! "Reading from file..."
    read_content SBARGOLD<< filename
    
    SBARGOLD! "File Content:"
    SBARGOLD! read_content
    """
    
    print("--- Code ---")
    print(code)
    
    print("\n--- Output ---")
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(program)
        print("\nFile I/O Test PASSED if you see the file content printed.")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
    finally:
        # Cleanup
        if os.path.exists("test_output.txt"):
            os.remove("test_output.txt")

if __name__ == "__main__":
    test_file_io()
