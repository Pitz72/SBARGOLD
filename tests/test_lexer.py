import sys
import os

# Add parent directory to path to import sbargold_core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer

def test_lexer():
    code = """
    SBARGOLD# Test Code
    x SBARGOLD= 10
    SBARGOLD! "Hello"
    SBARGOLD~ 5 SBARGOLD{
        x SBARGOLD+ x 1
    SBARGOLD}
    """
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("Tokens found:")
    for t in tokens:
        print(t)
        
    # Basic assertions
    assert any(t.type == 'CMD_ASSIGN' for t in tokens)
    assert any(t.type == 'CMD_PRINT' for t in tokens)
    assert any(t.type == 'CMD_LOOP' for t in tokens)
    assert any(t.type == 'BLOCK_START' for t in tokens)
    assert any(t.type == 'BLOCK_END' for t in tokens)
    assert any(t.type == 'INTEGER' and t.value == '10' for t in tokens)
    assert any(t.type == 'STRING' and t.value == 'Hello' for t in tokens)
    
    print("\nLexer Test PASSED!")

if __name__ == "__main__":
    test_lexer()
