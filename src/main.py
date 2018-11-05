from JSONParser.JSONLexer import createJSONLexer
from JSONParser import parseJSON, generateJSON_AST

if __name__ == '__main__':
    with open("sample.json", "r") as inp, open("sample.yaml", "w") as out:
        out.write(generateJSON_AST(inp.read()).toYAML())

