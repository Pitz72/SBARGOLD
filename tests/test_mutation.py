import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_mutation():
    code = """
    SBARGOLD# Test Mutation (L-Values)
    
    SBARGOLD! "--- Simple Var Mutation ---"
    x SBARGOLD= 10
    x SBARGOLD= 20
    SBARGOLD! x
    
    SBARGOLD! "--- Dictionary Mutation ---"
    user SBARGOLD[:] "name" "Mario" "age" 30
    SBARGOLD! user.name
    
    user.name SBARGOLD= "Luigi"
    user.age SBARGOLD= 31
    SBARGOLD! user.name
    SBARGOLD! user.age
    
    SBARGOLD! "--- Array Mutation ---"
    list SBARGOLD[] 100 200 300
    list.1 SBARGOLD= 999
    SBARGOLD! list.1
    
    SBARGOLD! "--- Mixed Mutation ---"
    data SBARGOLD[:] "items" (SBARGOLD[] 1 2 3)
    SBARGOLD! data.items.0
    data.items.0 SBARGOLD= 500
    SBARGOLD! data.items.0
    
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
        test_mutation()
        print("[OK] Mutation test PASSED")
    except Exception as e:
        print(f"[FAIL] Mutation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
