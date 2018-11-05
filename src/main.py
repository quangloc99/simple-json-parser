from JSONParser.JSONLexer import createJSONLexer

if __name__ == '__main__':
    for i in createJSONLexer("null, true, \"abcxyz\": 123"):
        print(i, i.isValue())
