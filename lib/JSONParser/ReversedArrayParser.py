from .finiteStateMachine import createFiniteStateMachine
from .ArrayToken import ArrayToken
from .ParsingError import ParsingError
from .utils import doThenRet
from .JSONLexer import OpenSquareBracketToken, CloseSquareBracketToken, CommaToken


def beginParsingReversedArray(tok, dat):
    return (
            doThenRet(lambda: dat.update(returnValue = ArrayToken()), handleEmptyArray) if isinstance(tok, CloseSquareBracketToken)
            else ParsingError.raises(tok)
    )

def handleEmptyArray(tok, dat):
    return (
            endParsingReversedArray if isinstance(tok, OpenSquareBracketToken)
            else parseValue(tok, dat)
    )

def parseValue(tok, dat):
    return (
            doThenRet(lambda: dat["returnValue"].content.append(tok), parseCommaOrBracket) if tok.isValue()
            else ParsingError.raises(tok)
    )

def parseCommaOrBracket(tok, dat):
    return (
            doThenRet(lambda: dat["returnValue"].content.reverse(), endParsingReversedArray) if isinstance(tok, OpenSquareBracketToken)
            else parseValue if isinstance(tok, CommaToken)
            else ParsingError.raises(tok)
    )

def endParsingReversedArray(tok, dat):
    pass

def createReversedArrayParser(reversedTokenSequences):
    return createFiniteStateMachine(
            reversedTokenSequences,
            set([endParsingReversedArray]), 
            beginParsingReversedArray
    )


