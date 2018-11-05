from test import TestJSONLexer
from Lexer.JSONLexer import JSONLexer

if __name__ == '__main__':
    print('\n'.join(map(lambda x: type(x).__name__, list(JSONLexer("null true false")))))
