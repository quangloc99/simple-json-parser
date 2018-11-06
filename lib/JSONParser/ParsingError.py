class ParsingError(Exception):
    def __init__(self, token):
        self.errorToken = token

    def __str__(self):
        return "Parsing error at line {}".format(self.errorToken.lineNumber)

    @classmethod
    def raises(cls, tok):
        raise cls(tok)
