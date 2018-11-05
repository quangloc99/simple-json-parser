from .Token import Token as LexToken
from .LexingError import LexingError
from .predefinedStates import endParsing
from ..utils import doThenRet, convertChar, specialYAMLChars

class StringToken(LexToken):
    def __init__(self, data):
        super().__init__(data)
        self.content = []

    def isValue(self):
        return True

    def toPythonValue(self):
        return ''.join(map(convertChar, self.content))

    def toYAML(self, indentLevel = 0, indentPart = '  ', forceQuote = True):
        ans = ''.join(self.content)
        forceQuote = forceQuote or  any([ch in specialYAMLChars for ch in ans])
        if forceQuote: ans = '"' + ans + '"'
        return ans

    def __repr__(self):
        return "StringToken({})".format(self.content.__repr__())

    def __str__(self):
        return ''.join(self.content)

isBeginningOfString = lambda ch: ch == '"'
isHexDigit = lambda ch: ch.isdigit() or 'a' <= ch <= 'f' or 'A' <= ch <= 'F'

def beginParsingString(ch, dat):
    return (
        doThenRet(lambda: dat.update(returnValue = StringToken(dat)), parseString) if isBeginningOfString(ch)
        else LexingError.raises(dat)
    )

def parseString(ch, dat):
    return (
        endParsingString if ch == '"'
        else beginParsingEscapeCharacter(ch, dat) if ch == '\\'
        else doThenRet(lambda: dat["returnValue"].content.append(ch), parseString)
    )

def beginParsingEscapeCharacter(ch, dat):
    dat["escapeChar"] = ''
    return parseEscapeCharacter if ch == '\\' else LexingError.raises(dat)

def parseEscapeCharacter(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].content.append('\\' + ch), parseString) if ch in '"\\/bfnrt'
        else doThenRet(lambda: dat.update(unicodeVal = ''), parseUnicodeValue) if ch == 'u'
        else LexingError.raises(dat)
    )

def parseUnicodeValue(ch, dat):
    if isHexDigit(ch): dat["unicodeVal"] += ch
    return (
        LexingError.raises(dat) if not isHexDigit(ch)
        else parseUnicodeValue if len(dat["unicodeVal"]) < 4
        else doThenRet(lambda: dat["returnValue"].content.append('\\u' + dat["unicodeVal"].lower()), parseString)
    )

def endParsingString(ch, dat):
    return endParsing
        
