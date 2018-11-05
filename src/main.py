from JSONParser.JSONLexer import createJSONLexer
from JSONParser import generateJSON_AST

if __name__ == '__main__':
    print(generateJSON_AST("[1, 2, [null, null, -14535.7e10], 3, true, false, []]").toPythonValue())

