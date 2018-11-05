from JSONParser.JSONLexer import createJSONLexer
from JSONParser import parseJSON

if __name__ == '__main__':
    print(parseJSON('{"x": 1, "y": [1, 2, 3, {"4": 100}]}'))

