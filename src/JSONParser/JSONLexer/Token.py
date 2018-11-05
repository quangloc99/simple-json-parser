from ..Token import Token as ParserToken
class Token(ParserToken):
    def __init__(self, userData):
        super().__init__()
        self.lineNumber = userData["lineNum"]
