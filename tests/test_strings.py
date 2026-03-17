import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_strings():
    code = """
    SBARGOLD# Test String Ops
    str1 SBARGOLD= "Hello"
    str2 SBARGOLD= "World"
    
    full SBARGOLD& str1 str2
    SBARGOLD! full
    
    upper SBARGOLD^ "UPPER" full
    SBARGOLD! upper
    
    len SBARGOLD^ "LEN" full
    SBARGOLD! len
    
    SBARGOLD! "Split Test:"
    parts SBARGOLD^ "SPLIT" "A-B-C" "-"
    SBARGOLD~ item in parts SBARGOLD{
        SBARGOLD! item
    SBARGOLD}
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
    
    print("\nString Test PASSED if you see HelloWorld, HELLOWORLD, 10, and A B C")

if __name__ == "__main__":
    test_strings()
