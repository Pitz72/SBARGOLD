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
        # FIX: Synchronize Python recursion limit with SBARGOLD's limit
        sys.setrecursionlimit(self.MAX_CALL_DEPTH + 500)
        
        self.op_count = 0  # Contatore operazioni reali (loop, aritmetica, I/O)
        self.MAX_OPERATIONS = 100000  # Limite operazioni effettive
        
        # Module protection
        self.import_stack: Set[str] = set()

    def _check_operation_limit(self, node: ast.ASTNode, count: int = 1):
        """SECURITY FIX: Controlla il limite operazioni reali, non solo statement.
        
        Questo previene DoS da loop semplici che eseguono milioni di operazioni
        Python senza incrementare instruction_count.
        """
        self.op_count += count
        if self.op_count > self.MAX_OPERATIONS:
            raise errors.RuntimeError(
                f"Security Error: Execution exceeded maximum allowed operations ({self.MAX_OPERATIONS}). "
                "Possible infinite loop or resource exhaustion attack.", 
                node.line, node.col
            )

    def _safe_path(self, user_path: str, node: ast.ASTNode) -> str:
        """Verifica che il path richiesto non tenti di uscire dalla base_path (Sandbox).
        
        SECURITY FIX: Usa os.path.realpath per risolvere symlink e normalizzare
        il path prima del confronto. Previene bypass con ../, symlink traversal,
        e path normalization attacks.
        """
        # Costruisci il path assoluto dal base_path
        joined_path = os.path.join(self.base_path, user_path)
        
        # Risolvi symlink e normalizza il path (../, ./, //)
        real_requested = os.path.realpath(joined_path)
        real_base = os.path.realpath(self.base_path)
        
        # Aggiungi separatore per prevenire match parziali (es: /project vs /project2)
        if not real_requested.startswith(real_base + os.sep) and real_requested != real_base:
            raise errors.RuntimeError(
                f"Security Error: Access to path '{user_path}' (resolved: '{real_requested}') outside of sandbox ('{real_base}') is denied.", 
                node.line, node.col
            )
        return real_requested

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

    def _debug_step(self, stmt, input_func=None, output_func=None):
        """Gestisce lo stepping interattivo per il debugging.
        
        FIX #12: Refactor per testabilità - permette injection di input/output functions.
        In produzione: input_func=input, output_func=print
        Nei test: input_func=lambda: mock_input.pop(0), output_func=lambda s: outputs.append(s)
        """
        _input = input_func if input_func else input
        _output = output_func if output_func else print
        
        _output(f"\n[DEBUG] File: {self.current_file} | Line: {stmt.line} | Col: {stmt.col}")
        _output(f"Istruzione: {stmt}")
        
        # FIX #12: Rimuovi dipendenza da isatty() - usa SBG_TEST_MODE per auto-skip
        if os.environ.get('SBG_TEST_MODE') == '1':
            return

        while True:
            try:
                cmd = _input("DEBUG (n:next, v:vars, q:quit) > ").lower().strip()
            except EOFError:
                break
            if cmd == 'n' or cmd == '':
                break
            elif cmd == 'v':
                _output("--- Variabili Locali ---")
                for k, v in self.environment.values.items():
                    _output(f"  {k} = {v}")
                _output("------------------------")
            elif cmd == 'q':
                _output("Debugging terminato.")
                sys.exit(0)
            else:
                _output("Comando non riconosciuto.")

    def _execute(self, stmt: ast.Statement):
        """Esegue una singola istruzione AST."""
        # SECURITY FIX: Usa _check_operation_limit invece del contatore statement grezzo
        self._check_operation_limit(stmt, 1)
            
        try:
            if isinstance(stmt, ast.PrintStatement):
                self._check_operation_limit(stmt, 1)  # I/O costosa
                values = [str(self._evaluate(expr)) for expr in stmt.expressions]
                print(" ".join(values))
            elif isinstance(stmt, ast.InputStatement):
                self._check_operation_limit(stmt, 1)  # I/O costosa
                prompt = stmt.prompt if stmt.prompt else ""
                val = input(prompt + " " if prompt else "")
                # FIX #9: Type coercion robusta - prova int, poi float, altrimenti stringa
                # Rimuove leading zeros per evitare confusione octal (007 → 7)
                # Gestisce numeri decimali multipli come error (3.14.15 → stringa)
                val_stripped = val.strip()
                if not val_stripped:
                    # Input vuoto → stringa vuota
                    typed_val = ""
                else:
                    # Prova int (rimuovendo leading zeros se numero puro)
                    try:
                        # Verifica sia un numero intero puro (solo cifre e segno opzionale)
                        if (val_stripped.lstrip('-').isdigit()):
                            typed_val = int(val_stripped)
                        else:
                            raise ValueError("Not a pure integer")
                    except ValueError:
                        # Prova float (una sola virgola/punto, numeri)
                        try:
                            # Conta separatori decimali
                            dot_count = val_stripped.count('.')
                            comma_count = val_stripped.count(',')
                            if dot_count + comma_count == 1 and val_stripped.replace('.','').replace(',','').lstrip('-').isdigit():
                                # Normalizza a punto per Python float
                                normalized = val_stripped.replace(',', '.')
                                typed_val = float(normalized)
                            elif dot_count == 0 and comma_count == 0:
                                # Non è numero → stringa
                                typed_val = val_stripped
                            else:
                                # Troppi separatori → stringa
                                typed_val = val_stripped
                        except ValueError:
                            # Fallback a stringa
                            typed_val = val_stripped
                self.environment.assign(stmt.variable, typed_val, stmt)
            elif isinstance(stmt, ast.AssignStatement):
                self._check_operation_limit(stmt, 1)  # Operazione di assegnazione
                value = self._evaluate(stmt.expression)
                
                # Gestione L-Value: dove scriviamo il valore?
                target = stmt.target
                if isinstance(target, ast.Identifier):
                    # Assegnazione semplice a variabile
                    self.environment.assign(target.name, value, stmt)
                elif isinstance(target, ast.PropAccess):
                    # Mutazione di un oggetto esistente (Dizionario o Array)
                    obj = self._evaluate(target.target)
                    key = self._evaluate(target.key)
                    
                    if isinstance(obj, dict):
                        obj[key] = value
                    elif isinstance(obj, list):
                        try:
                            idx = int(float(key))
                            if idx < 0 or idx >= len(obj):
                                raise errors.RuntimeError(f"Array mutation index out of bounds: {idx}", stmt.line, stmt.col)
                            obj[idx] = value
                        except (ValueError, TypeError):
                            raise errors.RuntimeError(f"Array index must be numeric, got {type(key).__name__}", stmt.line, stmt.col)
                    else:
                        raise errors.RuntimeError(f"Cannot mutate non-collection type {type(obj).__name__}", stmt.line, stmt.col)
                else:
                    raise errors.RuntimeError(f"Invalid assignment target: {type(target).__name__}", stmt.line, stmt.col)

            elif isinstance(stmt, ast.IfStatement):
                self._check_operation_limit(stmt, 1)  # Valutazione condizione iniziale
                executed = False
                if self._is_truthy(self._evaluate(stmt.condition)):
                    self._execute_block(stmt.body, Environment(self.environment))
                    executed = True
                else:
                    # Controlla rami ELIF
                    for cond, body in stmt.elif_branches:
                        self._check_operation_limit(stmt, 1)
                        if self._is_truthy(self._evaluate(cond)):
                            self._execute_block(body, Environment(self.environment))
                            executed = True
                            break
                
                # Se nessuno sopra è stato eseguito, esegui ELSE se presente
                if not executed and stmt.else_body:
                    self._check_operation_limit(stmt, 1)
                    self._execute_block(stmt.else_body, Environment(self.environment))

            elif isinstance(stmt, ast.WhileStatement):
                self._check_operation_limit(stmt, 1)
                while self._is_truthy(self._evaluate(stmt.condition)):
                    # Ogni iterazione è un'operazione che consuma budget
                    self._check_operation_limit(stmt, 1)
                    self._execute_block(stmt.body, Environment(self.environment))

            elif isinstance(stmt, ast.LoopStatement):
                self._check_operation_limit(stmt, 1)  # Setup loop
                if stmt.count_expr:
                    count_val = self._evaluate(stmt.count_expr)
                    try:
                        count = int(count_val)
                    except (ValueError, TypeError):
                        raise errors.RuntimeError(f"Loop count must be an integer, got {type(count_val).__name__}", stmt.line, stmt.col)
                    # SECURITY FIX: Conta ogni iterazione come operazione separata
                    for i in range(count):
                        self._check_operation_limit(stmt, 1)  # Ogni iterazione conta
                        self._execute_block(stmt.body, Environment(self.environment))
                elif stmt.iterator_var:
                    iterable = self._evaluate(stmt.iterable_expr)
                    if not isinstance(iterable, list):
                        raise errors.RuntimeError("Loop iterable must be an array", stmt.line, stmt.col)
                    # SECURITY FIX: Conta ogni iterazione come operazione separata
                    for item in iterable:
                        self._check_operation_limit(stmt, 1)  # Ogni iterazione conta
                        loop_env = Environment(self.environment)
                        loop_env.define(stmt.iterator_var, item)
                        self._execute_block(stmt.body, loop_env)
            elif isinstance(stmt, ast.FunctionDefStatement):
                self._check_operation_limit(stmt, 1)
                # FIX #7: Warning quando una funzione sovrascrive un'altra esistente
                if stmt.name in self.functions:
                    import warnings
                    warnings.warn(
                        f"Function '{stmt.name}' redefined at line {stmt.line}, column {stmt.col}. "
                        f"Previous definition at line {self.functions[stmt.name].declaration.line} will be replaced.",
                        RuntimeWarning,
                        stacklevel=2
                    )
                function = SbargoldFunction(stmt, self.environment)
                self.functions[stmt.name] = function
            elif isinstance(stmt, ast.FileWriteStatement):
                self._check_operation_limit(stmt, 5)  # I/O costosa: valutazione + scrittura
                path = str(self._evaluate(stmt.path))
                content = str(self._evaluate(stmt.content))
                full_path = self._safe_path(path, stmt)
                try:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                except Exception as e:
                    raise errors.RuntimeError(f"File Write Error: {e}", stmt.line, stmt.col)
            elif isinstance(stmt, ast.DictDeclStatement):
                self._check_operation_limit(stmt, len(stmt.keys) * 2)  # Ogni key-value è costoso
                keys = [self._evaluate(k) for k in stmt.keys]
                values = [self._evaluate(v) for v in stmt.values]
                dictionary = dict(zip(keys, values))
                self.environment.define(stmt.name, dictionary)
            elif isinstance(stmt, ast.ImportStatement):
                self._check_operation_limit(stmt, 50)  # Import è molto costoso (parsing + esecuzione)
                self._handle_import(stmt)
            elif isinstance(stmt, ast.ReturnStatement):
                self._check_operation_limit(stmt, 1)
                value = self._evaluate(stmt.expression)
                raise ReturnValue(value)
            elif isinstance(stmt, ast.ArrayDeclStatement):
                self._check_operation_limit(stmt, len(stmt.elements))  # Ogni elemento conta
                elements = [self._evaluate(e) for e in stmt.elements]
                self.environment.define(stmt.name, elements)
        except errors.SbargoldError:
            raise
        except Exception as e:
            # SECURITY FIX: Preserva l'eccezione originale con traceback per debugging
            # Non wrappare SbargoldError già gestite, solo eccezioni Python interne
            import traceback
            original_tb = traceback.format_exc()
            raise errors.RuntimeError(
                f"Internal Execution Error: {e}\n--- Original Traceback ---\n{original_tb}", 
                stmt.line, stmt.col
            ) from e

    def _handle_import(self, stmt: ast.ImportStatement):
        """Gestisce l'importazione di moduli con protezione contro loop circolari.
        
        SECURITY FIX: Elimina il check os.path.exists() che crea race condition (TOCTOU).
        Ora si tenta direttamente l'apertura e si cattura FileNotFoundError.
        """
        module_rel_path = str(self._evaluate(stmt.module_path))
        full_path = self._safe_path(module_rel_path, stmt)
        
        if full_path in self.import_stack:
            raise errors.RuntimeError(f"Import Error: Circular import detected for '{module_rel_path}'", stmt.line, stmt.col)
        
        self.import_stack.add(full_path)
        try:
            # SECURITY: Nessun pre-check esists() - apertura atomica con gestione errore
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    code = f.read()
            except FileNotFoundError:
                raise errors.RuntimeError(f"Import Error: File '{module_rel_path}' not found", stmt.line, stmt.col)
            except PermissionError:
                raise errors.RuntimeError(f"Import Error: Permission denied for '{module_rel_path}'", stmt.line, stmt.col)
            
            from .lexer import Lexer
            from .parser import Parser
            
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()
            
            # Sub-interpreter for module execution
            sub_interpreter = Interpreter(base_path=os.path.dirname(full_path))
            
            sub_interpreter.import_stack = self.import_stack # Share stack for circular detection
            sub_interpreter.current_file = module_rel_path
            sub_interpreter.interpret(program, debug=self.debug_mode)
            
            # NAMESPACING: Harvest module results into parent namespace
            # Example: module 'utils' -> functions become 'utils:func_name'
            module_name = os.path.splitext(os.path.basename(full_path))[0]
            
            # Copy all functions defined in module to parent with prefix
            for name, func in sub_interpreter.functions.items():
                self.functions[f"{module_name}:{name}"] = func
            
            # Copy all global variables defined in module to parent with prefix
            for name, val in sub_interpreter.globals.values.items():
                self.globals.define(f"{module_name}:{name}", val)
            
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
            if expr.op == 'AND':
                left_val = self._evaluate(expr.left)
                if not self._is_truthy(left_val): return False
                return bool(self._is_truthy(self._evaluate(expr.right)))
            if expr.op == 'OR':
                left_val = self._evaluate(expr.left)
                if self._is_truthy(left_val): return True
                return bool(self._is_truthy(self._evaluate(expr.right)))
                
            left = self._evaluate(expr.left)
            right = self._evaluate(expr.right)
            return self._evaluate_binary(left, expr.op, right, expr)
        if isinstance(expr, ast.UnaryOp):
            right = self._evaluate(expr.right)
            if expr.op == 'NOT':
                return not self._is_truthy(right)
            raise errors.RuntimeError(f"Unknown unary operator '{expr.op}'", expr.line, expr.col)
        if isinstance(expr, ast.FunctionCall):
            return self._call_function(expr)
        if isinstance(expr, ast.StringConcat):
            left = str(self._evaluate(expr.left))
            right = str(self._evaluate(expr.right))
            return left + right
        if isinstance(expr, ast.ArrayLiteral):
            self._check_operation_limit(expr, len(expr.elements))
            return [self._evaluate(e) for e in expr.elements]
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
            self._check_operation_limit(expr, 1)  # FIX: conta operazione accesso
            target = self._evaluate(expr.target)
            key = self._evaluate(expr.key)
            if isinstance(target, dict):
                return target.get(key)
            elif isinstance(target, list):
                try:
                    # FIX #10: Validazione indice array - deve essere intero puro
                    key_val = float(key)
                    if not key_val.is_integer():
                        raise errors.RuntimeError(
                            f"Array index must be an integer, got {key} (float index not allowed)", 
                            expr.line, expr.col
                        )
                    idx = int(key_val)
                    if idx < 0 or idx >= len(target):
                        raise errors.RuntimeError(
                            f"Array index out of bounds: {idx} (array length: {len(target)})", 
                            expr.line, expr.col
                        )
                    return target[idx]
                except (ValueError, TypeError):
                    raise errors.RuntimeError(f"Array index must be a numeric value, got '{key}' ({type(key).__name__})", expr.line, expr.col)
                except IndexError:
                    raise errors.RuntimeError(f"Array index out of bounds: {int(float(key))} (array length: {len(target)})", expr.line, expr.col)
            raise errors.RuntimeError(f"Property access target must be a dictionary or array, got {type(target).__name__}", expr.line, expr.col)
        return None

    def _evaluate_string_op(self, expr: ast.StringOp):
        """Esegue operazioni specializzate sulle stringhe.
        
        FIX #11: Tutte le operazioni stringa sono case-insensitive.
        LEN, len, Len sono equivalenti.
        """
        self._check_operation_limit(expr, 1)  # FIX: conta operazione
        op = self._evaluate(expr.op)
        target = self._evaluate(expr.target)
        target = str(target) if not isinstance(target, str) else target
        
        if not isinstance(op, str):
            raise errors.RuntimeError("String operation name must be a string", expr.line, expr.col)
        
        # FIX #11: Normalizza a uppercase per case-insensitive matching
        # Documentato: LEN, len, Len, LeN sono tutti validi
        op = op.upper()
        if op == "LEN": return len(target)
        if op == "UPPER": return target.upper()
        if op == "LOWER": return target.lower()
        if op == "SPLIT":
            sep = self._evaluate(expr.args[0]) if expr.args else " "
            return target.split(str(sep))
        
        # FIX #11: Suggerimento operazioni valide in errore
        valid_ops = "LEN, UPPER, LOWER, SPLIT"
        raise errors.RuntimeError(
            f"Unknown string operation '{op}'. Valid operations (case-insensitive): {valid_ops}", 
            expr.line, expr.col
        )

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
