def doThenRet(actions, ret):
    actions()
    return ret

class LexingError(Exception):
    def __init__(self, userData):
        self.lineNum = userData["lineNum"]

    def __str__(self):
        return "Lexing error at line number {}".format(self.lineNum)

class LexToken:
    def __init__(self, userData):
        self.lineNumber = userData["lineNum"]
