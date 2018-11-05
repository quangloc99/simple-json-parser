def changeAndRet(changes, ret):
    changes()
    return ret

class LexingError(Exception):
    def __init__(self, lineNum):
        self.lineNum = lineNum

    def __str__(self):
        return "Lexing error at line number {}".format(self.lineNum)

class LexToken:
    def __init__(self, lineNumber):
        self.lineNumber = lineNumber
