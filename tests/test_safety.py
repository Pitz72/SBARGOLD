import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter
from sbargold_core import errors

def test_return_safety():
    print("Testing Return outside function (should fail)...")
    code = "SBARGOLD< 123"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    try:
        parser.parse()
        print("[FAIL] Return safety test failed: SyntaxError NOT raised")
        return False
    except errors.SyntaxError as e:
        print(f"[OK] Return safety test PASSED: {e}")
        return True

def test_recursion_sync():
    print("Testing Recursion Sync (should handle 900+ calls)...")
    # A simple recursive function that will hit our 1000 limit
    code = """
    SBARGOLD> RECURSE n SBARGOLD{
        SBARGOLD@ n > 0 SBARGOLD{
            next SBARGOLD= n - 1
            SBARGOLD$ RECURSE next
        SBARGOLD}
    SBARGOLD}
    SBARGOLD$ RECURSE 800
    SBARGOLD! "Recursion handled 800 deep"
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter()
    try:
        interpreter.interpret(program)
        print("[OK] Recursion sync test PASSED")
        return True
    except errors.RuntimeError as e:
        print(f"[FAIL] Recursion sync test failed: {e}")
        return False
    except RecursionError as e:
        print(f"[FAIL] Recursion sync test failed: Python RecursionError hit! {e}")
        return False

if __name__ == "__main__":
    r1 = test_return_safety()
    r2 = test_recursion_sync()
    if r1 and r2:
        sys.exit(0)
    else:
        sys.exit(1)
