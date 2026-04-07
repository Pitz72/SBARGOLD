import re
from typing import List, Tuple, Optional

class Token:
    """Rappresenta un'unità atomica di codice (Token) con metadati di posizione."""
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"

class Lexer:
    """Analizzatore lessicale che converte il sorgente Sbargold in una sequenza di Token."""
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self) -> List[Token]:
        """Esegue la scansione completa del codice sorgente."""
        while self.pos < len(self.code):
            char = self.code[self.pos]

            # Gestione spazi e invio
            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
                continue

            # Commenti (SBARGOLD#)
            if self.code[self.pos:].startswith('SBARGOLD#'):
                self._skip_comment()
                continue

            # Comandi SBARGOLD
            if self.code[self.pos:].startswith('SBARGOLD'):
                self._read_command()
                continue
            
            # Stringhe letterali
            if char == '"':
                self._read_string()
                continue

            # Numeri (Interi e Float)
            if char.isdigit() or (char == '-' and self._peek_digit()):
                self._read_number()
                continue

            # Punto isolato per accesso proprietà (es. obj.prop)
            if char == '.' and not (self.pos + 1 < len(self.code) and self.code[self.pos+1].isdigit()):
                self.tokens.append(Token('OP_DOT', '.', self.line, self.column))
                self.pos += 1; self.column += 1; continue

            # Identificatori (Variabili e Funzioni)
            if char.isalpha() or char == '_':
                self._read_identifier()
                continue
            
            # Operatori generici
            self._read_operator()

        # FIX #15: Token EOF con posizione valida (inizio dell'ultima riga, non fuori range)
        # Usa (1, 1) come posizione sicura per EOF, o la posizione corrente se valida
        eof_line = max(1, self.line)
        eof_col = max(1, self.column)
        self.tokens.append(Token('EOF', '', eof_line, eof_col))
        return self.tokens

    def _peek_digit(self) -> bool:
        """Controlla se il carattere successivo è una cifra (per numeri negativi)."""
        if self.pos + 1 < len(self.code):
            return self.code[self.pos + 1].isdigit()
        return False

    def _skip_comment(self):
        """Ignora tutto il testo fino alla fine della riga."""
        while self.pos < len(self.code) and self.code[self.pos] != '\n':
            self.pos += 1

    def _read_command(self):
        """Legge un comando atomico SBARGOLD e ne valida il suffisso."""
        start_col = self.column
        valid_suffixes = {
            '[]': 'CMD_ARRAY',
            '[:]': 'CMD_DICT_DEF',
            '>>': 'CMD_FILE_WRITE',
            '<<': 'CMD_FILE_READ',
            '!': 'CMD_PRINT',
            '?': 'CMD_INPUT',
            '=': 'CMD_ASSIGN',
            '+': 'CMD_ADD',
            '-': 'CMD_SUB',
            '*': 'CMD_MUL',
            '/': 'CMD_DIV',
            '@?': 'CMD_ELSE_IF',
            '@!': 'CMD_ELSE',
            '@': 'CMD_IF',
            '~~': 'CMD_WHILE',
            '~': 'CMD_LOOP',
            '{': 'BLOCK_START',
            '}': 'BLOCK_END',
            '>': 'CMD_FUNC_DEF',
            '<': 'CMD_RETURN',
            '$': 'CMD_FUNC_CALL',
            '&': 'CMD_STR_CONCAT',
            '^': 'CMD_STR_OP',
            '|': 'CMD_IMPORT',
            '.': 'CMD_PROP_ACCESS',
        }
        
        cmd_prefix = 'SBARGOLD'
        remaining = self.code[self.pos + len(cmd_prefix):]
        
        # Match suffissi più lunghi per primi
        for suffix, token_type in sorted(valid_suffixes.items(), key=lambda x: len(x[0]), reverse=True):
            if remaining.startswith(suffix):
                self.tokens.append(Token(token_type, f'SBARGOLD{suffix}', self.line, start_col))
                self.pos += len(cmd_prefix) + len(suffix)
                self.column += len(cmd_prefix) + len(suffix)
                return
        
        # Caso KEYWORD pura (SBARGOLD come parola riservata)
        if len(remaining) == 0 or remaining[0].isspace():
             self.tokens.append(Token('KEYWORD', 'SBARGOLD', self.line, start_col))
             self.pos += len(cmd_prefix)
             self.column += len(cmd_prefix)
             return
             
        # Errore di sintassi per comando sconosciuto
        from . import errors
        end_pos = self.pos
        while end_pos < len(self.code) and not self.code[end_pos].isspace():
            end_pos += 1
        malformed = self.code[self.pos:end_pos]
        raise errors.SyntaxError(f"Malformed SBARGOLD command: '{malformed}'", self.line, start_col)

    def _read_string(self):
        """Legge una stringa tra doppi apici.
        
        FIX #14: Ottimizzato con lista + join per evitare O(n²) string building.
        """
        start_col = self.column
        self.pos += 1
        self.column += 1
        chars = []  # FIX #14: Usa lista per accumulare caratteri
        
        while self.pos < len(self.code) and self.code[self.pos] != '"':
            chars.append(self.code[self.pos])  # FIX #14: O(1) append invece di O(n) concat
            self.pos += 1
            self.column += 1
            
        if self.pos < len(self.code):
            self.pos += 1
            self.column += 1
            value = ''.join(chars)  # FIX #14: O(n) join una sola volta alla fine
            self.tokens.append(Token('STRING', value, self.line, start_col))
        else:
            from . import errors
            raise errors.SyntaxError("Unterminated string", self.line, start_col)

    def _read_number(self):
        """Legge un numero intero o decimale.
        
        FIX #14: Ottimizzato con lista + join per evitare O(n²) string building.
        """
        start_col = self.column
        chars = []
        
        if self.code[self.pos] == '-':
            chars.append('-')
            self.pos += 1; self.column += 1
            
        while self.pos < len(self.code) and self.code[self.pos].isdigit():
            chars.append(self.code[self.pos])
            self.pos += 1; self.column += 1
            
        # Consuma il punto decimale SOLO SE seguito da una cifra
        if self.pos < len(self.code) and self.code[self.pos] == '.' and \
           (self.pos + 1 < len(self.code) and self.code[self.pos+1].isdigit()):
            chars.append('.')
            self.pos += 1; self.column += 1
            while self.pos < len(self.code) and self.code[self.pos].isdigit():
                chars.append(self.code[self.pos])
                self.pos += 1; self.column += 1
            
        value_str = ''.join(chars)
        if '.' in value_str:
            self.tokens.append(Token('FLOAT', value_str, self.line, start_col))
        else:
            self.tokens.append(Token('INTEGER', value_str, self.line, start_col))

    def _read_identifier(self):
        """Legge un identificatore (variabile/funzione) o parola chiave.
        
        FIX #14: Ottimizzato con lista + join per evitare O(n²) string building.
        """
        start_col = self.column
        chars = []  # FIX #14: Usa lista per accumulare caratteri
        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_' or self.code[self.pos] == ':'):
            chars.append(self.code[self.pos])  # FIX #14: O(1) append
            self.pos += 1
            self.column += 1
            
        value = ''.join(chars)  # FIX #14: O(n) join una sola volta
        if value == 'in':
            self.tokens.append(Token('KEYWORD', 'in', self.line, start_col))
        elif value == 'AND':
            self.tokens.append(Token('OP_AND', 'AND', self.line, start_col))
        elif value == 'OR':
            self.tokens.append(Token('OP_OR', 'OR', self.line, start_col))
        elif value == 'NOT':
            self.tokens.append(Token('OP_NOT', 'NOT', self.line, start_col))
        else:
            self.tokens.append(Token('IDENTIFIER', value, self.line, start_col))

    def _read_operator(self):
        """Legge operatori multi-carattere e simboli speciali."""
        char = self.code[self.pos]
        start_col = self.column
        
        # Operatori a due caratteri
        multi_ops = {
            '==': 'OP_EQ', '!=': 'OP_NEQ', '<=': 'OP_LTE', '>=': 'OP_GTE'
        }
        for op, ttype in multi_ops.items():
            if self.code[self.pos:].startswith(op):
                self.tokens.append(Token(ttype, op, self.line, start_col))
                self.pos += 2; self.column += 2; return

        # Operatori aritmetici infix (PEMDAS support)
        # FIX #5: Aggiungi supporto per espressioni infix nel lexer
        arithmetic_ops = {'+': 'OP_ADD', '-': 'OP_SUB', '*': 'OP_MUL', '/': 'OP_DIV'}
        if char in arithmetic_ops:
            self.tokens.append(Token(arithmetic_ops[char], char, self.line, start_col))
            self.pos += 1; self.column += 1; return

        # Operatori a carattere singolo (confronto, raggruppamento e accesso)
        single_ops = {'>': 'OP_GT', '<': 'OP_LT', '(': 'LPAREN', ')': 'RPAREN', '.': 'OP_DOT'}
        if char in single_ops:
            self.tokens.append(Token(single_ops[char], char, self.line, start_col))
            self.pos += 1; self.column += 1; return
            
        # FIX #6: Errore per caratteri sconosciuti invece di ignorarli silenziosamente
        # Questo previene errori di sintassi mascherati e comportamenti imprevedibili
        from . import errors
        raise errors.SyntaxError(
            f"Unexpected character '{char}' (ASCII: {ord(char)}) at line {self.line}, column {start_col}. "
            f"If this is a valid character, it may not be supported by SBARGOLD.",
            self.line, start_col
        )
