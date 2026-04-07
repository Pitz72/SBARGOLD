import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter
import sbargold_core.errors as errors

def test_logic():
    code = """
    SBARGOLD# Test Logic AND, OR, NOT
    
    t SBARGOLD= 1
    f SBARGOLD= 0
    
    SBARGOLD! "--- AND Test ---"
    SBARGOLD@ t AND t SBARGOLD{ SBARGOLD! "t AND t: PASS" SBARGOLD}
    SBARGOLD@ t AND f SBARGOLD{ SBARGOLD! "t AND f: FAIL" SBARGOLD}
    SBARGOLD@ f AND t SBARGOLD{ SBARGOLD! "f AND t: FAIL" SBARGOLD}
    SBARGOLD@ f AND f SBARGOLD{ SBARGOLD! "f AND f: FAIL" SBARGOLD}

    SBARGOLD! "--- OR Test ---"
    SBARGOLD@ t OR t SBARGOLD{ SBARGOLD! "t OR t: PASS" SBARGOLD}
    SBARGOLD@ t OR f SBARGOLD{ SBARGOLD! "t OR f: PASS" SBARGOLD}
    SBARGOLD@ f OR t SBARGOLD{ SBARGOLD! "f OR t: PASS" SBARGOLD}
    SBARGOLD@ f OR f SBARGOLD{ SBARGOLD! "f OR f: FAIL" SBARGOLD}

    SBARGOLD! "--- NOT Test ---"
    SBARGOLD@ NOT f SBARGOLD{ SBARGOLD! "NOT f: PASS" SBARGOLD}
    SBARGOLD@ NOT t SBARGOLD{ SBARGOLD! "NOT t: FAIL" SBARGOLD}

    SBARGOLD! "--- Complex Test ---"
    x SBARGOLD= 10
    y SBARGOLD= 20
    SBARGOLD@ (x > 5) AND (NOT (y < 15)) SBARGOLD{
        SBARGOLD! "Complex Condition: PASS"
    SBARGOLD}
    """
    
    print(f"Testing logic conditions...")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    
    interpreter = Interpreter()
    interpreter.interpret(program)

if __name__ == "__main__":
    try:
        test_logic()
        print("[OK] Logic test PASSED")
    except Exception as e:
        print(f"[FAIL] Logic test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
