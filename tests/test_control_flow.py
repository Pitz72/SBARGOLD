import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_control_flow():
    code = """
    SBARGOLD# Test IF/ELIF/ELSE
    x SBARGOLD= 15
    
    SBARGOLD! "--- IF/ELIF/ELSE Test ---"
    SBARGOLD@ x < 10 SBARGOLD{
        SBARGOLD! "x is small"
    SBARGOLD}
    SBARGOLD@? x < 20 SBARGOLD{
        SBARGOLD! "x is medium"
    SBARGOLD}
    SBARGOLD@! SBARGOLD{
        SBARGOLD! "x is large"
    SBARGOLD}

    SBARGOLD# Test WHILE
    SBARGOLD! "--- WHILE Test ---"
    count SBARGOLD= 0
    SBARGOLD~~ count < 5 SBARGOLD{
        count SBARGOLD+ count 1
        SBARGOLD! count
    SBARGOLD}
    
    SBARGOLD! "Done."
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)

if __name__ == "__main__":
    try:
        test_control_flow()
        print("[OK] Control Flow test PASSED")
    except Exception as e:
        print(f"[FAIL] Control Flow test FAILED: {e}")
        sys.exit(1)
