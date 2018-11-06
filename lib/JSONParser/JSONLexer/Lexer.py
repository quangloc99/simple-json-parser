from ..finiteStateMachine import createFiniteStateMachine
from ..utils import doThenRet

from .LexingError import LexingError
from .Number import beginParsingNumber, isBeginningOfNumber
from .String import beginParsingString, isBeginningOfString
from .Signs import beginParsingSign, isASign
from .Literals import beginParsingLiteral, isBeginningOfLiteral
from .predefinedStates import endParsing

def skipSpaces(ch, dat):
    return (
        endParsing if ord(ch) == 0
        else doThenRet(dat['updateLineNum'], skipSpaces) if ch == '\n'
        else skipSpaces if ch.isspace()
        else mainParsePhase(ch, dat)
    )

beginParsing = skipSpaces

def mainParsePhase(ch, dat):
    return (
        beginParsingNumber(ch, dat) if isBeginningOfNumber(ch)
        else beginParsingString(ch, dat) if isBeginningOfString(ch)
        else beginParsingSign(ch, dat) if isASign(ch)
        else beginParsingLiteral(ch, dat) if isBeginningOfLiteral(ch)
        else LexingError.raises(dat)
    )

def createJSONLexer(input):
    dat = {'lineNum': 1}
    def updateLineNum():
        dat['lineNum'] += 1
    dat['updateLineNum'] = updateLineNum
    return createFiniteStateMachine(input, set([endParsing]), beginParsing, dat);
    
