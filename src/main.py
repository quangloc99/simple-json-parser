from JSONParser.JSONLexer import createJSONLexer

if __name__ == '__main__':
    print('\n'.join(map(lambda x: type(x).__name__, list(createJSONLexer("null true false")))))
