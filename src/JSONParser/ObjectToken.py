from .Token import Token

class ObjectToken(Token):
    def __init__(self):
        self.content = {}

    def isValue(self):
        return True

    def toPythonValue(self):
        ans = {}
        for k, v in self.content.items():
            ans[k.toPythonValue()] = v.toPythonValue()
        return ans

    def toYAML(self, indentLevel = 0, indentPart = '  '):
        return '\n' + '\n'.join(map(
            lambda kv: indentPart * indentLevel + kv[0].toYAML(indentLevel, indentPart, forceQuote=False) + ": " + kv[1].toYAML(indentLevel + 1, indentPart),
            self.content.items()
        ))

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return self.content.__repr__()
