from .Token import Token
class ArrayToken(Token):
    def __init__(self):
        super().__init__()
        self.content = []

    def isValue(self):
        return True
    
    def __str__(self):
        return '[{}]'.format(', '.join(map(str, self.content)))

    def toPythonValue(self):
        return list(map(lambda x: x.toPythonValue(), self.content))

