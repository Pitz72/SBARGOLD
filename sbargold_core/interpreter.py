import os
import sys
from typing import Any, Dict, List, Optional, Set
from . import ast
from . import errors

class Environment:
    """Gestisce lo scope delle variabili (Globali, Locali, Closures)."""
    def __init__(self, parent=None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        """Definisce una nuova variabile nello scope corrente."""
        self.values[name] = value

    def get(self, name: str, node: ast.ASTNode) -> Any:
        """Recupera il valore di una variabile risalendo la catena degli scope."""
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name, node)
        raise errors.RuntimeError(f"Undefined variable '{name}'", node.line, node.col)

    def assign(self, name: str, value: Any, node: ast.ASTNode):
        """Assegna un nuovo valore a una variabile esistente o la definisce se non trovata."""
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value, node)
            return
        self.define(name, value)

class SbargoldFunction:
    """Rappresenta una funzione con il suo scope di chiusura (Closure)."""
    def __init__(self, declaration: ast.FunctionDefStatement, closure: Environment):
        self.declaration = declaration
        self.closure = closure

class Interpreter:
    """Esecutore principale del codice Sbargold basato su AST."""
    
    def __init__(self, base_path: str = "."):
        self.globals = Environment()
        self.environment = self.globals
        self.functions: Dict[str, SbargoldFunction] = {}
        self.debug_mode = False
        self.base_path = os.path.abspath(base_path)
        self.current_file = "main"
        
        # Security & Resource Limits
        self.call_depth = 0
        self.MAX_CALL_DEPTH = 1000
        self.instruction_count = 0
        self.MAX_INSTRUCTIONS = 5000000
        
        # Module protection
        self.import_stack: Set[str] = set()

    def _safe_path(self, user_path: str, node: ast.ASTNode) -> str:
        """Verifica che il path richiesto non tenti di uscire dalla base_path (Sandbox)."""
        requested_path = os.path.abspath(os.path.join(self.base_path, user_path))
        if not requested_path.startswith(self.base_path):
            raise errors.RuntimeError(f"Security Error: Access to path '{user_path}' outside of sandbox is denied.", node.line, node.col)
        return requested_path

    def interpret(self, program: ast.Program, debug=False):
        """Avvia l'interpretazione del programma AST fornito."""
        self.debug_mode = debug
        try:
            for stmt in program.statements:
                if self.debug_mode:
                    self._debug_step(stmt)
                self._execute(stmt)
        except errors.SbargoldError as e:
            print(e)
        except ReturnValue:
            pass 

    def _debug_step(self, stmt):
        """Gestisce lo stepping interattivo per il debugging."""
        print(f"\n[DEBUG] File: {self.current_file} | Line: {stmt.line} | Col: {stmt.col}")
        print(f"Istruzione: {stmt}")
        
        if not sys.stdin.isatty() or os.environ.get('SBG_TEST_MODE') == '1':
            return

        while True:
            try:
                cmd = input("DEBUG (n:next, v:vars, q:quit) > ").lower().strip()
            except EOFError:
                break
            if cmd == 'n' or cmd == '':
                break
            elif cmd == 'v':
                print("--- Variabili Locali ---")
                for k, v in self.environment.values.items():
                    print(f"  {k} = {v}")
                print("------------------------")
            elif cmd == 'q':
                print("Debugging terminato.")
                sys.exit(0)
            else:
                print("Comando non riconosciuto.")

    def _execute(self, stmt: ast.Statement):
        """Esegue una singola istruzione AST."""
        self.instruction_count += 1
        if self.instruction_count > self.MAX_INSTRUCTIONS:
            raise errors.RuntimeError("Security Error: Execution exceeded maximum allowed instructions (Possible infinite loop).", stmt.line, stmt.col)
            
        try:
            if isinstance(stmt, ast.PrintStatement):
                value = self._evaluate(stmt.expression)
                print(value)
            elif isinstance(stmt, ast.InputStatement):
                prompt = stmt.prompt if stmt.prompt else ""
                val = input(prompt + " " if prompt else "")
                try:
                    if '.' in val:
                        val = float(val)
                    else:
                        val = int(val)
                except ValueError:
                    pass
                self.environment.assign(stmt.variable, val, stmt)
            elif isinstance(stmt, ast.AssignStatement):
                value = self._evaluate(stmt.expression)
                self.environment.assign(stmt.variable, value, stmt)
            elif isinstance(stmt, ast.IfStatement):
                if self._is_truthy(self._evaluate(stmt.condition)):
                    self._execute_block(stmt.body, Environment(self.environment))
            elif isinstance(stmt, ast.LoopStatement):
                if stmt.count_expr:
                    count_val = self._evaluate(stmt.count_expr)
                    try:
                        count = int(count_val)
                    except (ValueError, TypeError):
                        raise errors.RuntimeError(f"Loop count must be an integer, got {type(count_val).__name__}", stmt.line, stmt.col)
                    for _ in range(count):
                        self._execute_block(stmt.body, Environment(self.environment))
                elif stmt.iterator_var:
                    iterable = self._evaluate(stmt.iterable_expr)
                    if not isinstance(iterable, list):
                        raise errors.RuntimeError("Loop iterable must be an array", stmt.line, stmt.col)
                    for item in iterable:
                        loop_env = Environment(self.environment)
                        loop_env.define(stmt.iterator_var, item)
                        self._execute_block(stmt.body, loop_env)
            elif isinstance(stmt, ast.FunctionDefStatement):
                function = SbargoldFunction(stmt, self.environment)
                self.functions[stmt.name] = function
            elif isinstance(stmt, ast.FileWriteStatement):
                path = str(self._evaluate(stmt.path))
                content = str(self._evaluate(stmt.content))
                full_path = self._safe_path(path, stmt)
                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    raise errors.RuntimeError(f"File Write Error: {e}", stmt.line, stmt.col)
            elif isinstance(stmt, ast.DictDeclStatement):
                keys = [self._evaluate(k) for k in stmt.keys]
                values = [self._evaluate(v) for v in stmt.values]
                dictionary = dict(zip(keys, values))
                self.environment.define(stmt.name, dictionary)
            elif isinstance(stmt, ast.ImportStatement):
                self._handle_import(stmt)
            elif isinstance(stmt, ast.ReturnStatement):
                value = self._evaluate(stmt.expression)
                raise ReturnValue(value)
            elif isinstance(stmt, ast.ArrayDeclStatement):
                elements = [self._evaluate(e) for e in stmt.elements]
                self.environment.define(stmt.name, elements)
        except errors.SbargoldError:
            raise
        except Exception as e:
            raise errors.RuntimeError(f"Internal Execution Error: {e}", stmt.line, stmt.col)

    def _handle_import(self, stmt: ast.ImportStatement):
        """Gestisce l'importazione di moduli con protezione contro loop circolari."""
        module_rel_path = str(self._evaluate(stmt.module_path))
        full_path = self._safe_path(module_rel_path, stmt)
        
        if full_path in self.import_stack:
            raise errors.RuntimeError(f"Import Error: Circular import detected for '{module_rel_path}'", stmt.line, stmt.col)
        
        if not os.path.exists(full_path):
             raise errors.RuntimeError(f"Import Error: File '{module_rel_path}' non trovato", stmt.line, stmt.col)
        
        self.import_stack.add(full_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            from .lexer import Lexer
            from .parser import Parser
            
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            
            # Sub-interpreter for module execution
            sub_interpreter = Interpreter(base_path=os.path.dirname(full_path))
            sub_interpreter.globals = self.globals 
            sub_interpreter.functions = self.functions 
            sub_interpreter.import_stack = self.import_stack # Share stack
            sub_interpreter.current_file = module_rel_path
            sub_interpreter.interpret(program, debug=self.debug_mode)
            
        except errors.SbargoldError:
            raise
        except Exception as e:
            raise errors.RuntimeError(f"Import Error: {e}", stmt.line, stmt.col)
        finally:
            self.import_stack.remove(full_path)

    def _execute_block(self, statements: List[ast.Statement], env: Environment):
        """Esegue un blocco di istruzioni in un nuovo ambiente."""
        previous = self.environment
        try:
            self.environment = env
            for stmt in statements:
                if self.debug_mode:
                    self._debug_step(stmt)
                self._execute(stmt)
        finally:
            self.environment = previous

    def _evaluate(self, expr: ast.Expression) -> Any:
        """Valuta un'espressione AST e ne ritorna il valore."""
        if isinstance(expr, ast.Number):
            return expr.value
        if isinstance(expr, ast.String):
            return expr.value
        if isinstance(expr, ast.Identifier):
            return self.environment.get(expr.name, expr)
        if isinstance(expr, ast.BinOp):
            left = self._evaluate(expr.left)
            right = self._evaluate(expr.right)
            return self._evaluate_binary(left, expr.op, right, expr)
        if isinstance(expr, ast.FunctionCall):
            return self._call_function(expr)
        if isinstance(expr, ast.StringConcat):
            left = str(self._evaluate(expr.left))
            right = str(self._evaluate(expr.right))
            return left + right
        if isinstance(expr, ast.StringOp):
            return self._evaluate_string_op(expr)
        if isinstance(expr, ast.FileRead):
            path = str(self._evaluate(expr.path))
            full_path = self._safe_path(path, expr)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                raise errors.RuntimeError(f"File Read Error: {e}", expr.line, expr.col)
        if isinstance(expr, ast.PropAccess):
            target = self._evaluate(expr.target)
            key = self._evaluate(expr.key)
            if isinstance(target, dict):
                return target.get(key)
            elif isinstance(target, list):
                try:
                    return target[int(key)]
                except (ValueError, IndexError):
                    raise errors.RuntimeError(f"Array index error: {key}", expr.line, expr.col)
            raise errors.RuntimeError("Property access target must be a dictionary or array", expr.line, expr.col)
        return None

    def _evaluate_string_op(self, expr: ast.StringOp):
        """Esegue operazioni specializzate sulle stringhe."""
        op = self._evaluate(expr.op)
        target = self._evaluate(expr.target)
        target = str(target) if not isinstance(target, str) else target
        
        if not isinstance(op, str):
            raise errors.RuntimeError("String operation name must be a string", expr.line, expr.col)
            
        op = op.upper()
        if op == "LEN": return len(target)
        if op == "UPPER": return target.upper()
        if op == "LOWER": return target.lower()
        if op == "SPLIT":
            sep = self._evaluate(expr.args[0]) if expr.args else " "
            return target.split(str(sep))
        
        raise errors.RuntimeError(f"Unknown string operation '{op}'", expr.line, expr.col)

    def _evaluate_binary(self, left, op, right, node: ast.ASTNode):
        """Valuta operatori aritmetici e di confronto."""
        try:
            if op == '+': return left + right
            if op == '-': return left - right
            if op == '*': return left * right
            if op == '/': 
                if right == 0: raise errors.RuntimeError("Division by zero", node.line, node.col)
                return left / right
            if op == '==': return left == right
            if op == '!=': return left != right
            if op == '<': return left < right
            if op == '>': return left > right
            if op == '<=': return left <= right
            if op == '>=': return left >= right
        except TypeError as e:
            raise errors.RuntimeError(f"Type error in binary operation: {e}", node.line, node.col)
        return None

    def _call_function(self, expr: ast.FunctionCall):
        """Gestisce la chiamata di una funzione con supporto alle Closures."""
        self.call_depth += 1
        if self.call_depth > self.MAX_CALL_DEPTH:
            raise errors.RuntimeError("Security Error: Maximum recursion depth exceeded", expr.line, expr.col)
            
        if expr.name not in self.functions:
            self.call_depth -= 1
            raise errors.RuntimeError(f"Undefined function '{expr.name}'", expr.line, expr.col)
        
        function = self.functions[expr.name]
        func_def = function.declaration
        
        if len(expr.args) != len(func_def.params):
            self.call_depth -= 1
            raise errors.RuntimeError(f"Function '{expr.name}' expects {len(func_def.params)} arguments, got {len(expr.args)}", expr.line, expr.col)
        
        func_env = Environment(function.closure)
        for i, param in enumerate(func_def.params):
            func_env.define(param, self._evaluate(expr.args[i]))
            
        try:
            self._execute_block(func_def.body, func_env)
        except ReturnValue as r:
            return r.value
        finally:
            self.call_depth -= 1
            
        return None

    def _is_truthy(self, value):
        """Determina se un valore è considerato 'Vero' in Sbargold."""
        if value is None: return False
        if isinstance(value, bool): return value
        if isinstance(value, (int, float)): return value != 0
        if isinstance(value, (str, list, dict)): return len(value) > 0
        return True

class ReturnValue(Exception):
    """Eccezione interna per gestire il ritorno di valori dalle funzioni."""
    def __init__(self, value):
        self.value = value
