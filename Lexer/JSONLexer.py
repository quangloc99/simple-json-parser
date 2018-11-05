from createFiniteStateMachine import createFiniteStateMachine
from Lexer.Number import beginParseNumber, isBeginningOfNumber
from Lexer.Base import changeAndRet

def beginParse(ch, dat):
    return skipSpaces(ch, dat)
endParse = beginParse

def lexingError(ch, dat):
    raise LexingError(dat)

def skipSpaces(ch, dat):
    return (
        beginParse if ord(ch) == 0
        else changeAndRet(dat['updateLineNum'], skipSpaces) if ch == '\n'
        else skipSpaces if ch.isspace()
        else mainParsePhase(ch, dat)
    )

def mainParsePhase(ch, dat):
    return (
        beginParseNumber(ch, dat) if isBeginningOfNumber(ch)
        else parsingError(ch, dat)
    )

def JSONLexer(input):
    dat = {'lineNum': 1}
    def updateLineNum():
        dat['lineNum'] += 1
    dat['updateLineNum'] = updateLineNum
    return createFiniteStateMachine(input, set([beginParse]), beginParse, dat);
    
