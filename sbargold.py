#!/usr/bin/env python3
"""
Sbargold Programming Language Interpreter
Un linguaggio esoterico basato su un solo comando: SBARGOLD
"""

import sys
from sbargold_core.lexer import Lexer
from sbargold_core.parser import Parser
from sbargold_core.interpreter import Interpreter
from sbargold_core import errors

def run(code: str):
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        program = parser.parse()
        
        interpreter = Interpreter()
        interpreter.interpret(program)
        
    except errors.SbargoldError as e:
        print(e)
    except Exception as e:
        print(f"INTERNAL ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    if len(sys.argv) < 2:
        print("Uso: python sbargold.py <file.sbg>")
        print("     python sbargold.py -c '<codice>'")
        print("     python sbargold.py -d <file.sbg> (Debug Mode)")
        sys.exit(1)
    
    debug = False
    if sys.argv[1] == '-d':
        debug = True
        filename = sys.argv[2]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            interpreter = Interpreter()
            interpreter.interpret(program, debug=True)
            
        except Exception as e:
            print(f"SBARGOLD ERROR: {e}")
            sys.exit(1)
        return

    if sys.argv[1] == '-c':
        code = sys.argv[2]
        run(code)
    else:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
            run(code)
        except FileNotFoundError:
            print(f"SBARGOLD ERROR: File '{filename}' non trovato!")
            sys.exit(1)
        except Exception as e:
            print(f"SBARGOLD ERROR: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
