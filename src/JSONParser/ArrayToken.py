from .Token import Token
class ArrayToken(Token):
    def __init__(self):
        super().__init__()
        self._isValue = True
        self.content = []
    
    def __str__(self):
        return '[{}]'.format(', '.join(map(str, self.content)))

