from typing import List, Optional
from .lexer import Token, Lexer
from . import ast
from . import errors

class Parser:
    """Parser per trasformare una lista di token in un Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> ast.Program:
        """Punto di ingresso per il parsing del programma."""
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'EOF':
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return ast.Program(statements)

    def _peek(self, offset: int = 0) -> Token:
        """Guarda il token corrente o i successivi senza consumarli."""
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return self.tokens[-1] # EOF

    def _consume(self, type: str = None) -> Token:
        """Consuma il token corrente verificandone il tipo."""
        token = self._peek()
        if type and token.type != type:
            raise errors.SyntaxError(f"Expected {type}, found {token.type}", token.line, token.column)
        self.pos += 1
        return token

    def _match(self, type: str) -> bool:
        """Verifica se il token corrente corrisponde al tipo e lo consuma in caso positivo."""
        if self._peek().type == type:
            self.pos += 1
            return True
        return False

    def _parse_statement(self) -> Optional[ast.Statement]:
        """Esegue il parsing di una singola istruzione."""
        token = self._peek()

        if token.type == 'CMD_PRINT':
            cmd_token = self._consume()
            expr = self._parse_expression()
            return ast.PrintStatement(expr, cmd_token.line, cmd_token.column)
        
        if token.type == 'CMD_IF':
            cmd_token = self._consume()
            condition = self._parse_expression()
            self._consume('BLOCK_START')
            body = self._parse_block()
            return ast.IfStatement(condition, body, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_LOOP':
            cmd_token = self._consume()
            # Foreach loop: SBARGOLD~ item in array
            if self._peek().type == 'IDENTIFIER' and self._peek(1).type == 'KEYWORD' and self._peek(1).value == 'in':
                iterator_var = self._consume('IDENTIFIER').value
                self._consume('KEYWORD') # in
                iterable_expr = self._parse_expression()
                self._consume('BLOCK_START')
                body = self._parse_block()
                return ast.LoopStatement(None, iterator_var, iterable_expr, body, cmd_token.line, cmd_token.column)
            else:
                # Count loop: SBARGOLD~ 10
                count_expr = self._parse_expression()
                self._consume('BLOCK_START')
                body = self._parse_block()
                return ast.LoopStatement(count_expr, None, None, body, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_FUNC_DEF':
            cmd_token = self._consume()
            name = self._consume('IDENTIFIER').value
            params = []
            while self._peek().type == 'IDENTIFIER':
                params.append(self._consume('IDENTIFIER').value)
            self._consume('BLOCK_START')
            body = self._parse_block()
            return ast.FunctionDefStatement(name, params, body, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_RETURN':
            cmd_token = self._consume()
            expr = self._parse_expression()
            return ast.ReturnStatement(expr, cmd_token.line, cmd_token.column)

        if token.type == 'IDENTIFIER':
            name_token = self._consume()
            
            # Input: var SBARGOLD? "prompt"
            if self._match('CMD_INPUT'):
                cmd_token = self.tokens[self.pos-1]
                prompt = None
                if self._peek().type == 'STRING':
                    prompt = self._consume('STRING').value
                return ast.InputStatement(name_token.value, prompt, cmd_token.line, cmd_token.column)

            # Array Declaration: name SBARGOLD[] ...
            if self._match('CMD_ARRAY'):
                cmd_token = self.tokens[self.pos-1]
                elements = []
                while self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                     elements.append(self._parse_expression())
                return ast.ArrayDeclStatement(name_token.value, elements, cmd_token.line, cmd_token.column)

            # Assignment: name SBARGOLD= expr
            if self._match('CMD_ASSIGN'):
                cmd_token = self.tokens[self.pos-1]
                expr = self._parse_expression()
                return ast.AssignStatement(name_token.value, expr, cmd_token.line, cmd_token.column)
            
            # Arithmetic assignment: result SBARGOLD+ a b
            if self._peek().type in ['CMD_ADD', 'CMD_SUB', 'CMD_MUL', 'CMD_DIV']:
                op_token = self._consume()
                op_map = {'CMD_ADD': '+', 'CMD_SUB': '-', 'CMD_MUL': '*', 'CMD_DIV': '/'}
                left = self._parse_expression()
                right = self._parse_expression()
                bin_op = ast.BinOp(left, op_map[op_token.type], right, op_token.line, op_token.column)
                return ast.AssignStatement(name_token.value, bin_op, op_token.line, op_token.column)
            
            # Function Call with return capture: result SBARGOLD$ func args
            if self._match('CMD_FUNC_CALL'):
                cmd_token = self.tokens[self.pos-1]
                func_name = self._consume('IDENTIFIER').value
                args = []
                while self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                     args.append(self._parse_expression())
                call_node = ast.FunctionCall(func_name, args, cmd_token.line, cmd_token.column)
                return ast.AssignStatement(name_token.value, call_node, cmd_token.line, cmd_token.column)

            # String Concatenation: result SBARGOLD& str1 str2
            if self._match('CMD_STR_CONCAT'):
                cmd_token = self.tokens[self.pos-1]
                left = self._parse_expression()
                right = self._parse_expression()
                concat_node = ast.StringConcat(left, right, cmd_token.line, cmd_token.column)
                return ast.AssignStatement(name_token.value, concat_node, cmd_token.line, cmd_token.column)

            # String Op: result SBARGOLD^ "UPPER" str
            if self._match('CMD_STR_OP'):
                cmd_token = self.tokens[self.pos-1]
                op_name = self._parse_expression()
                target = self._parse_expression()
                args = []
                while self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                     args.append(self._parse_expression())
                op_node = ast.StringOp(op_name, target, args, cmd_token.line, cmd_token.column)
                return ast.AssignStatement(name_token.value, op_node, cmd_token.line, cmd_token.column)

            # File Read: content SBARGOLD<< "file.txt"
            if self._match('CMD_FILE_READ'):
                cmd_token = self.tokens[self.pos-1]
                path = self._parse_expression()
                read_node = ast.FileRead(path, cmd_token.line, cmd_token.column)
                return ast.AssignStatement(name_token.value, read_node, cmd_token.line, cmd_token.column)

            # Property Access: result SBARGOLD. dict key
            if self._match('CMD_PROP_ACCESS'):
                cmd_token = self.tokens[self.pos-1]
                target = self._parse_expression()
                key = self._parse_expression()
                access_node = ast.PropAccess(target, key, cmd_token.line, cmd_token.column)
                return ast.AssignStatement(name_token.value, access_node, cmd_token.line, cmd_token.column)
            
            # Dictionary Definition: name SBARGOLD[:] key1 val1 ...
            if self._match('CMD_DICT_DEF'):
                cmd_token = self.tokens[self.pos-1]
                keys = []
                values = []
                while self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                     keys.append(self._parse_expression())
                     if self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                        values.append(self._parse_expression())
                     else:
                        raise errors.SyntaxError("Dictionary definition expects key-value pairs", cmd_token.line, cmd_token.column)
                return ast.DictDeclStatement(name_token.value, keys, values, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_IMPORT':
            cmd_token = self._consume()
            path = self._parse_expression()
            return ast.ImportStatement(path, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_FILE_WRITE':
            cmd_token = self._consume()
            path = self._parse_expression()
            content = self._parse_expression()
            return ast.FileWriteStatement(path, content, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_FUNC_CALL':
            cmd_token = self._consume()
            func_name = self._consume('IDENTIFIER').value
            args = []
            while self._peek().type not in ['EOF', 'BLOCK_END'] and not self._peek().type.startswith('CMD_'):
                    args.append(self._parse_expression())
            call_expr = ast.FunctionCall(func_name, args, cmd_token.line, cmd_token.column)
            return ast.PrintStatement(call_expr, cmd_token.line, cmd_token.column)

        self._consume() # Skip unknown
        return None

    def _parse_block(self) -> List[ast.Statement]:
        """Esegue il parsing di un blocco di istruzioni delimitate da SBARGOLD{ }."""
        statements = []
        while self._peek().type != 'BLOCK_END' and self._peek().type != 'EOF':
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        self._consume('BLOCK_END')
        return statements

    # --- Expression Parsing with Precedence (PEMDAS) ---

    def _parse_expression(self) -> ast.Expression:
        """Entry point per le espressioni."""
        return self._parse_comparison()

    def _parse_comparison(self) -> ast.Expression:
        """Livello 4: == != < > <= >="""
        left = self._parse_addition()
        
        while self._peek().type in ['OP_EQ', 'OP_NEQ', 'OP_LT', 'OP_GT', 'OP_LTE', 'OP_GTE']:
            op_token = self._consume()
            right = self._parse_addition()
            left = ast.BinOp(left, op_token.value, right, op_token.line, op_token.column)
            
        return left

    def _parse_addition(self) -> ast.Expression:
        """Livello 3: + -"""
        left = self._parse_multiplication()
        
        # Support arithmetic operators outside of SBARGOLD+ commands if needed, 
        # but Sbargold usually uses SBARGOLD+ commands. 
        # However, for expression evaluation (e.g. in IF condition), we support standard ops.
        while self._peek().type in ['OP_ADD', 'OP_SUB']: # Need to add these to lexer if we want infix
             # Current lexer only has CMD_ADD etc. Let's see if we have generic tokens.
             # Actually, the lexer only recognizes OP_EQ etc. 
             # We should probably add + - * / as generic tokens in Lexer for infix support.
             pass
        
        # For now, Sbargold expressions are mostly terms or single binary ops from CMD_.
        # Let's keep it simple or expand Lexer. 
        return left

    def _parse_multiplication(self) -> ast.Expression:
        """Livello 2: * /"""
        return self._parse_term()

    def _parse_term(self) -> ast.Expression:
        """Livello 1: Valori atomici."""
        token = self._peek()
        
        if token.type == 'INTEGER':
            self._consume()
            return ast.Number(int(token.value), line=token.line, col=token.column)
        if token.type == 'FLOAT':
            self._consume()
            return ast.Number(float(token.value), is_float=True, line=token.line, col=token.column)
        if token.type == 'STRING':
            self._consume()
            return ast.String(token.value, line=token.line, col=token.column)
        if token.type == 'IDENTIFIER':
            self._consume()
            # Simple variable access
            return ast.Identifier(token.value, line=token.line, col=token.column)
            
        raise errors.SyntaxError(f"Unexpected token in expression: {token.type}", token.line, token.column)
