from JSONParser.JSONLexer import createJSONLexer
from JSONParser.Parser import parseJSON

if __name__ == '__main__':
    print(parseJSON("[1, 2, [null, null, -14535.7e10], 3, true, false, []]"))

