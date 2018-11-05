from .ReversedArrayParser import createReversedArrayParser
from .ParsingError import ParsingError
from .JSONLexer import (
        createJSONLexer, 
        OpenCurlyBracketToken,
        OpenSquareBracketToken,
        CloseCurlyBracketToken,
        CloseSquareBracketToken,
)

isCloseBracket = lambda tok: isinstance(tok, CloseCurlyBracketToken) or isinstance(tok, CloseSquareBracketToken)
isOpenBracket = lambda tok: isinstance(tok, OpenCurlyBracketToken) or isinstance(tok, OpenSquareBracketToken)
isCurlyBracket = lambda tok: isinstance(tok, CloseCurlyBracketToken) or isinstance(tok, OpenCurlyBracketToken) 
isSameBracketType = lambda tok1, tok2: isCurlyBracket(tok1) == isCurlyBracket(tok2)
isBracket = lambda tok: isCloseBracket(tok) or isOpenBracket(tok)

def parseJSON(input):
    lexer = createJSONLexer(input)
    tokenStack = []
    bracketTokenStack = []

    def popTokenStackGenerator():
        nonlocal tokenStack
        while True:
            yield tokenStack.pop()

    for tok in lexer:
        tokenStack.append(tok)
        print(tokenStack)
        if not isBracket(tok):
            continue
        if isOpenBracket(tok):
            bracketTokenStack.append(tok)
            continue
        if len(bracketTokenStack) == 0 or not isSameBracketType(bracketTokenStack[-1], tok):
            raise ParsingError(tok)
        bracketTokenStack.pop()
        if isCurlyBracket(tok):
            pass
        else:
            array = next(createReversedArrayParser(popTokenStackGenerator()))
            tokenStack.append(array)
    return tokenStack[-1]

