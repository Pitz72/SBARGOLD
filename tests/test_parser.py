import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser

def test_parser():
    code = """
    SBARGOLD# Test Parser
    x SBARGOLD= 10
    SBARGOLD! "Hello"
    SBARGOLD@ x > 5 SBARGOLD{
        SBARGOLD! "Big"
    SBARGOLD}
    """
    
    print("--- Code ---")
    print(code)
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    program = parser.parse()
    
    print("\n--- AST ---")
    print(program)
    
    # Assertions
    assert len(program.statements) == 3
    assert str(program.statements[0]).startswith("Assign(x = Number(10))")
    assert str(program.statements[1]).startswith("Print(exprs=1)")
    assert str(program.statements[2]).startswith("If(")
    
    print("\nParser Test PASSED!")

if __name__ == "__main__":
    test_parser()
