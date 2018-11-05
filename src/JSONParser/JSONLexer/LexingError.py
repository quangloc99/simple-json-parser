class LexingError(Exception):
    def __init__(self, userData):
        self.lineNum = userData["lineNum"]

    def __str__(self):
        return "Lexing error at line number {}".format(self.lineNum)

    @classmethod
    def raises(cls, userData):
        raise cls(userData)


