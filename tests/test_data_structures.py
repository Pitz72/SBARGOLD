import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter

def test_data_structures():
    code = """
    SBARGOLD# Test Data Structures
    
    SBARGOLD! "Creating Dictionary..."
    user SBARGOLD[:] "name" "Mario" "age" 30 "city" "Rome"
    
    SBARGOLD! "Accessing Properties..."
    name SBARGOLD. user "name"
    age SBARGOLD. user "age"
    
    SBARGOLD! "Name:"
    SBARGOLD! name
    SBARGOLD! "Age:"
    SBARGOLD! age
    
    SBARGOLD! "Array Access via Property:"
    list SBARGOLD[] 10 20 30
    item SBARGOLD. list 1
    SBARGOLD! item
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
    
    print("\nData Structures Test PASSED if you see Mario, 30, and 20")

if __name__ == "__main__":
    test_data_structures()
