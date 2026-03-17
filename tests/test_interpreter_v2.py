import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_interpreter():
    code = """
    SBARGOLD# Test Interpreter
    x SBARGOLD= 10
    SBARGOLD! "Start Loop"
    
    sum SBARGOLD= 0
    i SBARGOLD= 1
    
    SBARGOLD~ 5 SBARGOLD{
        sum SBARGOLD+ sum i
        i SBARGOLD+ i 1
    SBARGOLD}
    
    SBARGOLD! "Sum is:"
    SBARGOLD! sum
    
    SBARGOLD> square n SBARGOLD{
        res SBARGOLD* n n
        SBARGOLD< res
    SBARGOLD}
    
    sq SBARGOLD$ square 5
    SBARGOLD! "Square of 5 is:"
    SBARGOLD! sq
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
    
    print("\nInterpreter Test PASSED if you see Sum 15 and Square 25")

if __name__ == "__main__":
    test_interpreter()
