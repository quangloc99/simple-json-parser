from .ObjectToken import ObjectToken
from .ParsingError import ParsingError
from .finiteStateMachine import createFiniteStateMachine
from .utils import doThenRet
from .JSONLexer import (
        StringToken,
        ColonToken,
        CommaToken,
        OpenCurlyBracketToken,
        CloseCurlyBracketToken,
)

def beginParsingReversedObject(tok, dat):
    return (
            doThenRet(lambda: dat.update(returnValue = ObjectToken()), handleEmptyObject) if isinstance(tok, CloseCurlyBracketToken)
            else ParsingError.raises(tok)
    )

def handleEmptyObject(tok, dat):
    return (
            endParsingReversedObject if isinstance(tok, OpenCurlyBracketToken)
            else parseValue(tok, dat)
    )

def parseValue(tok, dat):
    return (
            doThenRet(lambda: dat.update(curVal = tok), parseColon) if tok.isValue()
            else ParsingError.raises(tok)
    )

def parseColon(tok, dat):
    return (
            parseString if isinstance(tok, ColonToken)
            else ParsingError.raises(tok)
    )

def parseString(tok, dat):
    return (
            doThenRet(lambda: dat["returnValue"].content.update({tok: dat["curVal"]}), parseCommaOrBracket) if isinstance(tok, StringToken)
            else ParsingError.raises(tok)
    )

def parseCommaOrBracket(tok, dat):
    return (
            parseValue if isinstance(tok, CommaToken)
            else endParsingReversedObject if isinstance(tok, OpenCurlyBracketToken)
            else ParsingError.raises(tok)
    )

def endParsingReversedObject(tok, dat):
    pass

def createReversedObjectParser(reversedTokenSequences):
    return createFiniteStateMachine(
        reversedTokenSequences,
        set([endParsingReversedObject]),
        beginParsingReversedObject
    )

