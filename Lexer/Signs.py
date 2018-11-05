from Lexer.Base import LexToken, LexingError, doThenRet

class CommaToken(LexToken): pass
class ColonToken(LexToken): pass
class OpenCurlyBracketToken(LexToken): pass
class CloseCurlyBracketToken(LexToken): pass
class OpenSquareBracketToken(LexToken): pass
class CloseSquareBracketToken(LexToken): pass

signMap = {
    ',': CommaToken,
    ':': ColonToken,
    '{': OpenCurlyBracketToken,
    '}': CloseCurlyBracketToken,
    '[': OpenSquareBracketToken,
    ']': CloseSquareBracketToken,
}

isASign = lambda ch: ch in signMap

def beginParsingSign(ch, dat):
    return (
        doThenRet(lambda: dat.update(returnValue = signMap[ch](dat)), endParsingSign) if isASign(ch)
        else LexingError.raises(dat)
    )

def endParsingSign(ch, dat):
    return Lexer.JSONLexer.endParsing

import Lexer.JSONLexer

