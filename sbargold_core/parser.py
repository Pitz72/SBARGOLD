from typing import List, Optional
from .lexer import Token, Lexer
from . import ast
from . import errors

class Parser:
    """Parser per trasformare una lista di token in un Abstract Syntax Tree (AST)."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.in_function = False

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
            exprs = self._parse_argument_list()
            # Se non ci sono argomenti, stampa una riga vuota o errore? 
            # In SBARGOLD solitamente c'è almeno un argomento.
            return ast.PrintStatement(exprs, cmd_token.line, cmd_token.column)
        
        if token.type == 'CMD_IF':
            cmd_token = self._consume()
            condition = self._parse_expression()
            self._consume('BLOCK_START')
            body = self._parse_block()
            
            elif_branches = []
            else_body = None
            
            # Gestione ELSE IF (@?) e ELSE (@!)
            while self._peek().type == 'CMD_ELSE_IF':
                self._consume() # @?
                elif_cond = self._parse_expression()
                self._consume('BLOCK_START')
                elif_body = self._parse_block()
                elif_branches.append((elif_cond, elif_body))
                
            if self._peek().type == 'CMD_ELSE':
                self._consume() # @!
                self._consume('BLOCK_START')
                else_body = self._parse_block()
                
            return ast.IfStatement(condition, body, elif_branches, else_body, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_WHILE':
            cmd_token = self._consume()
            condition = self._parse_expression()
            self._consume('BLOCK_START')
            body = self._parse_block()
            return ast.WhileStatement(condition, body, cmd_token.line, cmd_token.column)

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
            
            # Entra nel contesto funzione
            old_in_function = self.in_function
            self.in_function = True
            try:
                body = self._parse_block()
            finally:
                self.in_function = old_in_function
                
            return ast.FunctionDefStatement(name, params, body, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_RETURN':
            if not self.in_function:
                raise errors.SyntaxError("SBARGOLD< (Return) used outside of a function definition", token.line, token.column)
            cmd_token = self._consume()
            expr = self._parse_expression()
            return ast.ReturnStatement(expr, cmd_token.line, cmd_token.column)

        if token.type == 'IDENTIFIER':
            # Parsing L-Value: può essere un semplice ID o un'espressione di accesso (obj.prop)
            # Salviamo la posizione per eventuale fallback
            start_pos = self.pos
            target_expr = self._parse_expression()
            
            # Se dopo l'espressione c'è SBARGOLD=, è un assegnamento (Mutazione)
            if self._match('CMD_ASSIGN'):
                cmd_token = self.tokens[self.pos-1]
                value_expr = self._parse_expression()
                return ast.AssignStatement(target_expr, value_expr, cmd_token.line, cmd_token.column)

            # --- Retro-compatibilità per gli altri comandi SBARGOLD che iniziano con identificatore ---
            # Se target_expr è un semplice identificatore, controlliamo i comandi classici (SBARGOLD?, SBARGOLD[], etc)
            if isinstance(target_expr, ast.Identifier):
                name = target_expr.name
                
                # Input: var SBARGOLD? "prompt"
                if self._match('CMD_INPUT'):
                    cmd_token = self.tokens[self.pos-1]
                    prompt = self._consume('STRING').value if self._peek().type == 'STRING' else None
                    return ast.InputStatement(name, prompt, cmd_token.line, cmd_token.column)

                # Array Declaration: name SBARGOLD[] ...
                if self._match('CMD_ARRAY'):
                    cmd_token = self.tokens[self.pos-1]
                    elements = self._parse_argument_list()
                    return ast.ArrayDeclStatement(name, elements, cmd_token.line, cmd_token.column)
                
                # Arithmetic assignment: result SBARGOLD+ a b
                if self._peek().type in ['CMD_ADD', 'CMD_SUB', 'CMD_MUL', 'CMD_DIV']:
                    op_token = self._consume()
                    op_map = {'CMD_ADD': '+', 'CMD_SUB': '-', 'CMD_MUL': '*', 'CMD_DIV': '/'}
                    left = self._parse_expression()
                    right = self._parse_expression()
                    bin_op = ast.BinOp(left, op_map[op_token.type], right, op_token.line, op_token.column)
                    # Nota: passiamo target_expr invece della stringa name per coerenza col nuovo AST
                    return ast.AssignStatement(target_expr, bin_op, op_token.line, op_token.column)
                
                # Function Call with return capture: result SBARGOLD$ func args
                if self._match('CMD_FUNC_CALL'):
                    cmd_token = self.tokens[self.pos-1]
                    func_name = self._consume('IDENTIFIER').value
                    args = self._parse_argument_list()
                    call_node = ast.FunctionCall(func_name, args, cmd_token.line, cmd_token.column)
                    return ast.AssignStatement(target_expr, call_node, cmd_token.line, cmd_token.column)

                # Dictionary Definition: name SBARGOLD[:] key1 val1 ...
                if self._match('CMD_DICT_DEF'):
                    cmd_token = self.tokens[self.pos-1]
                    keys, values = [], []
                    while self.pos < len(self.tokens):
                         next_t = self._peek()
                         if next_t.type in ['EOF', 'BLOCK_END'] or next_t.type.startswith('CMD_'): break
                         keys.append(self._parse_expression())
                         if self._peek().type in ['EOF', 'BLOCK_END'] or self._peek().type.startswith('CMD_'):
                             raise errors.SyntaxError("Dictionary expects key-value pairs", cmd_token.line, cmd_token.column)
                         values.append(self._parse_expression())
                    return ast.DictDeclStatement(name, keys, values, cmd_token.line, cmd_token.column)

                # String Concatenation assignment: result SBARGOLD& str1 str2
                if self._match('CMD_STR_CONCAT'):
                    cmd_token = self.tokens[self.pos-1]
                    left = self._parse_expression()
                    right = self._parse_expression()
                    concat_expr = ast.StringConcat(left, right, cmd_token.line, cmd_token.column)
                    return ast.AssignStatement(target_expr, concat_expr, cmd_token.line, cmd_token.column)

                # String Operation assignment: result SBARGOLD^ "OP" target args
                if self._match('CMD_STR_OP'):
                    cmd_token = self.tokens[self.pos-1]
                    op_name = self._parse_expression()
                    target = self._parse_expression()
                    args = self._parse_argument_list()
                    op_expr = ast.StringOp(op_name, target, args, cmd_token.line, cmd_token.column)
                    return ast.AssignStatement(target_expr, op_expr, cmd_token.line, cmd_token.column)

                # File Read assignment: result SBARGOLD<< filename
                if self._match('CMD_FILE_READ'):
                    cmd_token = self.tokens[self.pos-1]
                    path = self._parse_expression()
                    read_expr = ast.FileRead(path, cmd_token.line, cmd_token.column)
                    return ast.AssignStatement(target_expr, read_expr, cmd_token.line, cmd_token.column)

                # Property Access assignment: result SBARGOLD. target key
                if self._match('CMD_PROP_ACCESS'):
                    cmd_token = self.tokens[self.pos-1]
                    target = self._parse_expression()
                    key = self._parse_expression()
                    access_expr = ast.PropAccess(target, key, cmd_token.line, cmd_token.column)
                    return ast.AssignStatement(target_expr, access_expr, cmd_token.line, cmd_token.column)

            # Se arriviamo qui, l'espressione non è seguita da un comando di assegnazione valido
            curr = self._peek()
            raise errors.SyntaxError(f"Unexpected expression '{target_expr}' followed by unexpected token {curr.type} ({curr.value})", curr.line, curr.column)



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
            args = self._parse_argument_list()
            call_expr = ast.FunctionCall(func_name, args, cmd_token.line, cmd_token.column)
            return ast.PrintStatement([call_expr], cmd_token.line, cmd_token.column)

        # FIX #13: Errore esplicito per token sconosciuto invece di skip silenzioso
        # Questo previene parsing parziale di programmi con errori di sintassi
        unknown_token = self._peek()
        raise errors.SyntaxError(
            f"Unexpected or unsupported token '{unknown_token.type}' with value '{unknown_token.value}' "
            f"at line {unknown_token.line}, column {unknown_token.column}. "
            f"This may indicate a syntax error or unsupported language feature.",
            unknown_token.line, unknown_token.column
        )

    def _parse_block(self) -> List[ast.Statement]:
        """Esegue il parsing di un blocco di istruzioni delimitate da SBARGOLD{ }."""
        statements = []
        while self._peek().type != 'BLOCK_END' and self._peek().type != 'EOF':
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                # Se _parse_statement non ritorna nulla, evitiamo loop infiniti
                # ma dovrebbe sempre sollevare un errore se non trova uno statement valido
                self.pos += 1
        self._consume('BLOCK_END')
        return statements

    def _parse_argument_list(self) -> List[ast.Expression]:
        """Parsing robusto di una lista di argomenti fino a un terminatore."""
        args = []
        while self.pos < len(self.tokens):
            next_token = self._peek()
            
            # Terminator Logic (v24K.LINGOTTO-5)
            # Un terminatore è un blocco fine, EOF o un comando SBARGOLD di tipo statement.
            expression_commands = ['CMD_STR_CONCAT', 'CMD_STR_OP', 'CMD_FILE_READ', 'CMD_PROP_ACCESS', 'CMD_FUNC_CALL']
            
            # Se è un comando SBARGOLD che non è una sotto-espressione, ci fermiamo.
            if next_token.type == 'EOF' or next_token.type == 'BLOCK_END' or \
               (next_token.type.startswith('CMD_') and next_token.type not in expression_commands):
                break
            
            # Se è un IDENTIFIER, dobbiamo guardare avanti (Lookahead).
            # Se è l'inizio di una catena di assegnazione (x SBARGOLD= o x.y SBARGOLD=), ci fermiamo.
            if next_token.type == 'IDENTIFIER':
                assignment_commands = [
                    'CMD_ASSIGN', 'CMD_ADD', 'CMD_SUB', 'CMD_MUL', 'CMD_DIV', 
                    'CMD_INPUT', 'CMD_ARRAY', 'CMD_DICT_DEF', 'CMD_FUNC_CALL',
                    'CMD_STR_CONCAT', 'CMD_STR_OP', 'CMD_FILE_READ', 'CMD_PROP_ACCESS'
                ]
                
                # Lookahead per catene di accesso: x.y.z ...
                look_pos = 1
                while self._peek(look_pos).type == 'OP_DOT' and \
                      (self._peek(look_pos+1).type == 'IDENTIFIER' or self._peek(look_pos+1).type == 'INTEGER'):
                    look_pos += 2
                
                after_target = self._peek(look_pos)
                if after_target.type in assignment_commands:
                    break

            
            # SBARGOLD supporta identificatori, stringhe, numeri e comandi-espressione
            if next_token.type in ['INTEGER', 'FLOAT', 'STRING', 'IDENTIFIER', 
                                    'CMD_STR_CONCAT', 'CMD_STR_OP', 'CMD_FILE_READ', 
                                    'CMD_PROP_ACCESS', 'CMD_FUNC_CALL']:
                 args.append(self._parse_expression())
            else:
                # Se troviamo qualcosa di inaspettato (es. un operatore infix sparso),
                # lo saltiamo o segnaliamo? Per ora saltiamo per compatibilità.
                break
        return args

    # --- Expression Parsing with Precedence (PEMDAS) ---

    def _parse_expression(self) -> ast.Expression:
        """Entry point per le espressioni."""
        return self._parse_logical_or()

    def _parse_logical_or(self) -> ast.Expression:
        """Livello 6: OR logico"""
        left = self._parse_logical_and()
        
        while self._peek().type == 'OP_OR':
            op_token = self._consume()
            right = self._parse_logical_and()
            left = ast.BinOp(left, op_token.value, right, op_token.line, op_token.column)
            
        return left

    def _parse_logical_and(self) -> ast.Expression:
        """Livello 5: AND logico"""
        left = self._parse_comparison()
        
        while self._peek().type == 'OP_AND':
            op_token = self._consume()
            right = self._parse_comparison()
            left = ast.BinOp(left, op_token.value, right, op_token.line, op_token.column)
            
        return left

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
        
        # FIX #5: Implementazione completa PEMDAS - supporto operatori infix
        while self._peek().type in ['OP_ADD', 'OP_SUB']:
            op_token = self._consume()
            right = self._parse_multiplication()
            left = ast.BinOp(left, op_token.value, right, op_token.line, op_token.column)
        
        return left

    def _parse_multiplication(self) -> ast.Expression:
        """Livello 2: * /"""
        left = self._parse_dot_access()

        # FIX #5: Implementazione completa PEMDAS - supporto * e / infix
        while self._peek().type in ['OP_MUL', 'OP_DIV']:
            op_token = self._consume()
            right = self._parse_dot_access()
            left = ast.BinOp(left, op_token.value, right, op_token.line, op_token.column)

        return left

    def _parse_dot_access(self) -> ast.Expression:
        """Livello 0: Accesso proprietà infix (obj.prop). Massima priorità."""
        left = self._parse_term()
        
        while self._peek().type == 'OP_DOT':
            op_token = self._consume()
            # Zucchero sintattico: se dopo il punto c'è un IDENTIFIER, lo trattiamo come stringa letterale
            # Questo permette user.name invece di user."name"
            next_t = self._peek()
            if next_t.type == 'IDENTIFIER':
                self._consume()
                right = ast.String(next_t.value, next_t.line, next_t.column)
            else:
                right = self._parse_term()
            left = ast.PropAccess(left, right, op_token.line, op_token.column)
            
        return left


    def _parse_term(self) -> ast.Expression:
        """Livello 1: Valori atomici, prefissi unari e raggruppamenti."""
        token = self._peek()
        
        if token.type == 'LPAREN':
            self._consume() # consuma (
            expr = self._parse_expression()
            self._consume('RPAREN') # consuma )
            return expr

        if token.type == 'OP_NOT':
            op_token = self._consume()
            right = self._parse_term()
            return ast.UnaryOp(op_token.value, right, op_token.line, op_token.column)
            
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
            
        # SBARGOLD Prefix Expression Operators
        if token.type == 'CMD_STR_CONCAT':
            cmd_token = self._consume()
            left = self._parse_expression()
            right = self._parse_expression()
            return ast.StringConcat(left, right, cmd_token.line, cmd_token.column)
            
        if token.type == 'CMD_STR_OP':
            cmd_token = self._consume()
            op_name = self._parse_expression()
            target = self._parse_expression()
            args = self._parse_argument_list()
            return ast.StringOp(op_name, target, args, cmd_token.line, cmd_token.column)
            
        if token.type == 'CMD_FILE_READ':
            cmd_token = self._consume()
            path = self._parse_expression()
            return ast.FileRead(path, cmd_token.line, cmd_token.column)
            
        if token.type == 'CMD_PROP_ACCESS':
            cmd_token = self._consume()
            target = self._parse_expression()
            key = self._parse_expression()
            return ast.PropAccess(target, key, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_ARRAY':
            cmd_token = self._consume()
            elements = self._parse_argument_list()
            return ast.ArrayLiteral(elements, cmd_token.line, cmd_token.column)

        if token.type == 'CMD_FUNC_CALL':
            cmd_token = self._consume()
            func_name = self._consume('IDENTIFIER').value
            args = self._parse_argument_list()
            return ast.FunctionCall(func_name, args, cmd_token.line, cmd_token.column)
            
        raise errors.SyntaxError(f"Unexpected token in expression: {token.type}", token.line, token.column)
