from createFiniteStateMachine import createFiniteStateMachine

from Lexer.Base import doThenRet, LexingError
from Lexer.Number import beginParsingNumber, isBeginningOfNumber
from Lexer.String import beginParsingString, isBeginningOfString
from Lexer.Signs import beginParsingSign, isASign

def beginParsing(ch, dat):
    return skipSpaces(ch, dat)
endParsing = beginParsing

def skipSpaces(ch, dat):
    return (
        endParsing if ord(ch) == 0
        else doThenRet(dat['updateLineNum'], skipSpaces) if ch == '\n'
        else skipSpaces if ch.isspace()
        else mainParsePhase(ch, dat)
    )

def mainParsePhase(ch, dat):
    return (
        beginParsingNumber(ch, dat) if isBeginningOfNumber(ch)
        else beginParsingString(ch, dat) if isBeginningOfString(ch)
        else beginParsingSign(ch, dat) if isASign(ch)
        else LexingError.raises(dat)
    )

def JSONLexer(input):
    dat = {'lineNum': 1}
    def updateLineNum():
        dat['lineNum'] += 1
    dat['updateLineNum'] = updateLineNum
    return createFiniteStateMachine(input, set([beginParsing, endParsing]), beginParsing, dat);
    
