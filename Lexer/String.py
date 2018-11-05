from Lexer.Base import LexToken, doThenRet

class StringToken(LexToken):
    def __init__(self, data):
        super().__init__(data)
        self.content = []

    def __repr__(self):
        return "StringToken({})".format(self.content.__repr__())

    def __str__(self):
        return ''.join(self.content)

isBeginningOfString = lambda ch: ch == '"'
isHexDigit = lambda ch: ch.isdigit() or 'a' <= ch <= 'f' or 'A' <= ch <= 'F'

def beginParsingString(ch, dat):
    return (
        doThenRet(lambda: dat.update(returnValue = StringToken(dat)), parseString) if isBeginningOfString(ch)
        else Lexer.JSONLexer.lexingError(ch, dat)
    )

def parseString(ch, dat):
    return (
        endParsingString if ch == '"'
        else beginParsingEscapeCharacter(ch, dat) if ch == '\\'
        else doThenRet(lambda: dat["returnValue"].content.append(ch), parseString)
    )

def beginParsingEscapeCharacter(ch, dat):
    dat["escapeChar"] = ''
    return parseEscapeCharacter if ch == '\\' else Lexer.JSONLexer.lexingError(ch, dat)

def parseEscapeCharacter(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].content.append('\\' + ch), parseString) if ch in '"\\/bfnrt'
        else doThenRet(lambda: dat.update(unicodeVal = ''), parseUnicodeValue) if ch == 'u'
        else Lexer.JSONLexer.lexingError(ch, dat)
    )

def parseUnicodeValue(ch, dat):
    if isHexDigit(ch): dat["unicodeVal"] += ch
    return (
        Lexer.JSONLexer.lexingError(ch, dat) if not isHexDigit(ch)
        else parseUnicodeValue if len(dat["unicodeVal"]) < 4
        else doThenRet(lambda: dat["returnValue"].content.append('\\u' + dat["unicodeVal"].lower()), parseString)
    )

def endParsingString(ch, dat):
    return Lexer.JSONLexer.endParsing
        

import Lexer.JSONLexer