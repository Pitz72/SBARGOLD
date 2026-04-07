from typing import List, Optional, Any

class ASTNode:
    """Nodo base per l'Abstract Syntax Tree (AST) di Sbargold."""
    def __init__(self, line: int = 0, col: int = 0):
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class Program(ASTNode):
    """Nodo radice che contiene l'intera sequenza di istruzioni del programma."""
    def __init__(self, statements: List[ASTNode]):
        super().__init__()
        self.statements = statements
    
    def __repr__(self):
        return f"Program(stmts={len(self.statements)})"

class Statement(ASTNode):
    """Nodo base per le istruzioni (non ritornano valori)."""
    pass

class Expression(ASTNode):
    """Nodo base per le espressioni (ritornano valori)."""
    pass

# --- Expressions ---

class Number(Expression):
    """Rappresenta un valore numerico (Intero o Float)."""
    def __init__(self, value: float, is_float: bool = False, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.value = value
        self.is_float = is_float
    
    def __repr__(self):
        return f"Number({self.value})"

class String(Expression):
    """Rappresenta una stringa letterale."""
    def __init__(self, value: str, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.value = value
    
    def __repr__(self):
        return f"String('{self.value}')"

class Identifier(Expression):
    """Rappresenta un nome di variabile o funzione."""
    def __init__(self, name: str, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"

class BinOp(Expression):
    """Rappresenta un'operazione binaria (Matematica o Confronto)."""
    def __init__(self, left: Expression, op: str, right: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"

class UnaryOp(Expression):
    """Rappresenta un'operazione unaria (es. NOT logico)."""
    def __init__(self, op: str, right: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f"UnaryOp({self.op} {self.right})"

class FunctionCall(Expression):
    """Rappresenta l'invocazione di una funzione."""
    def __init__(self, name: str, args: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"Call({self.name}, args={len(self.args)})"

class StringConcat(Expression):
    """Rappresenta la concatenazione di due stringhe (SBARGOLD&)."""
    def __init__(self, left: Expression, right: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Concat({self.left}, {self.right})"

class StringOp(Expression):
    """Rappresenta un'operazione su stringa (SBARGOLD^)."""
    def __init__(self, op: str, target: Expression, args: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.op = op
        self.target = target
        self.args = args
    
    def __repr__(self):
        return f"StrOp({self.op}, on={self.target})"

class FileRead(Expression):
    """Rappresenta la lettura di un file (SBARGOLD<<)."""
    def __init__(self, path: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.path = path
    
    def __repr__(self):
        return f"FileRead({self.path})"

class PropAccess(Expression):
    """Rappresenta l'accesso a una proprietà di un dizionario o array (SBARGOLD.)."""
    def __init__(self, target: Expression, key: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.target = target
        self.key = key
    
    def __repr__(self):
        return f"Access({self.target}.{self.key})"

# --- Statements ---

class ArrayLiteral(Expression):
    """Rappresenta un array letterale (SBARGOLD[] 1 2 3)."""
    def __init__(self, elements: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.elements = elements
    
    def __repr__(self):
        return f"ArrayLiteral(size={len(self.elements)})"

class DictDeclStatement(Statement):
    """Definizione di un dizionario (SBARGOLD[:])."""
    def __init__(self, name: str, keys: List[Expression], values: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.name = name
        self.keys = keys
        self.values = values
    
    def __repr__(self):
        return f"DictDecl({self.name}, pairs={len(self.keys)})"

class ImportStatement(Statement):
    """Importazione di un modulo esterno (SBARGOLD|)."""
    def __init__(self, module_path: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.module_path = module_path
    
    def __repr__(self):
        return f"Import({self.module_path})"

class FileWriteStatement(Statement):
    """Scrittura su un file (SBARGOLD>>)."""
    def __init__(self, path: Expression, content: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.path = path
        self.content = content
    
    def __repr__(self):
        return f"FileWrite(to={self.path})"

class PrintStatement(Statement):
    """Stampa di uno o più valori (SBARGOLD!)."""
    def __init__(self, expressions: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.expressions = expressions
    
    def __repr__(self):
        return f"Print(exprs={len(self.expressions)})"

class InputStatement(Statement):
    """Richiesta input utente (SBARGOLD?)."""
    def __init__(self, variable: str, prompt: Optional[str] = None, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.variable = variable
        self.prompt = prompt
    
    def __repr__(self):
        return f"Input({self.variable}, prompt='{self.prompt}')"

class AssignStatement(Statement):
    """Assegnazione di un valore (SBARGOLD=). Il target può essere una variabile o una proprietà."""
    def __init__(self, target: Expression, expression: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.target = target
        self.expression = expression
    
    def __repr__(self):
        return f"Assign({self.target} = {self.expression})"

class IfStatement(Statement):
    """Struttura condizionale (SBARGOLD@). Supporta rami opzionali ELIF e ELSE."""
    def __init__(self, condition: Expression, body: List[Statement], elif_branches: List[tuple] = None, else_body: List[Statement] = None, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.condition = condition
        self.body = body
        self.elif_branches = elif_branches if elif_branches else [] # List of (condition, body)
        self.else_body = else_body
    
    def __repr__(self):
        return f"If({self.condition}, branches={len(self.elif_branches)}, has_else={self.else_body is not None})"

class WhileStatement(Statement):
    """Struttura di iterazione condizionale (SBARGOLD~~)."""
    def __init__(self, condition: Expression, body: List[Statement], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"While({self.condition}, body={len(self.body)})"

class LoopStatement(Statement):
    """Struttura di iterazione (SBARGOLD~)."""
    def __init__(self, count_expr: Optional[Expression], iterator_var: Optional[str], iterable_expr: Optional[Expression], body: List[Statement], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.count_expr = count_expr
        self.iterator_var = iterator_var
        self.iterable_expr = iterable_expr
        self.body = body
    
    def __repr__(self):
        if self.count_expr:
            return f"LoopCount({self.count_expr})"
        return f"LoopForeach({self.iterator_var} in {self.iterable_expr})"

class FunctionDefStatement(Statement):
    """Definizione di una funzione (SBARGOLD>)."""
    def __init__(self, name: str, params: List[str], body: List[Statement], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.name = name
        self.params = params
        self.body = body
    
    def __repr__(self):
        return f"FuncDef({self.name}, params={self.params})"

class ReturnStatement(Statement):
    """Ritorno di un valore da una funzione (SBARGOLD<)."""
    def __init__(self, expression: Expression, line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.expression = expression
    
    def __repr__(self):
        return f"Return({self.expression})"

class ArrayDeclStatement(Statement):
    """Definizione di un array (SBARGOLD[])."""
    def __init__(self, name: str, elements: List[Expression], line: int = 0, col: int = 0):
        super().__init__(line, col)
        self.name = name
        self.elements = elements
    
    def __repr__(self):
        return f"ArrayDecl({self.name}, size={len(self.elements)})"
