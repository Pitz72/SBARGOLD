class SbargoldError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.message)

    def __str__(self):
        if self.line:
            return f"SBARGOLD ERROR: {self.message} at line {self.line}, column {self.column}"
        return f"SBARGOLD ERROR: {self.message}"

class RuntimeError(SbargoldError):
    pass

class SyntaxError(SbargoldError):
    pass
