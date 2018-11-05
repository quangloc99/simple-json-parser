from .Token import Token as LexToken
from .LexingError import LexingError
from .predefinedStates import endParsing
from ..utils import doThenRet

class LiteralToken(LexToken):
    def __init__(self, dat):
        super().__init__(dat)

    def isValue(self):
        return True

        
class TrueToken(LiteralToken):
    def toPythonValue(self):
        return True

class FalseToken(LiteralToken):
    def toPythonValue(self):
        return False

class NullToken(LiteralToken):
    def toPythonValue(self):
        return None

def generateStates(matchString, cls):
    def generateCurrentState(currentMatchingChar, nextState):
        def currentState(ch, dat):
            nonlocal currentMatchingChar, nextState
            return nextState if ch == currentMatchingChar else LexingError.raises(dat)
        return currentState

    def finalState(ch, dat):
        dat['returnValue'] = cls(dat)
        return endParsing

    curState = finalState
    for i in range(len(matchString) - 1, -1, -1):
        curState = generateCurrentState(matchString[i], curState)
    
    return curState

isBeginningOfLiteral = lambda ch: ch in 'tfn'

beginParsingTrue = generateStates("true", TrueToken)
beginParsingFalse = generateStates("false", FalseToken)
beginParsingNull = generateStates("null", NullToken)

def beginParsingLiteral(ch, dat):
    return (
        beginParsingTrue(ch, dat) if ch == 't'
        else beginParsingFalse(ch, dat) if ch == 'f'
        else beginParsingNull(ch, dat) if ch == 'n'
        else LexingError.raises(dat)
    )


