from Lexer.Base import LexToken, changeAndRet

class NumberToken(LexToken):
    def __init__(self, userData, isPositive = True):
        super().__init__(userData)
        self.isPositive = isPositive
        self.integerPart = ''
        self.fractionPart = ''
        self.hasPositiveExponent = True
        self.exponentPart = ''

    def update(self, part, ch):
        val = ord(ch) - ord('0')
        if part == 'i': self.integerPart += ch
        if part == 'f': self.fractionPart += ch
        if part == 'e': self.exponentPart += ch
        if part == 'se': self.hasPositiveExponent = val == '+' 

    def __repr__(self):
        return "NumberToken(positive={}, intPart={}, fracPart={}, positiveExp={}, exponentPart={})".format(
                self.isPositive,
                self.integerPart,
                self.fractionPart,
                self.hasPositiveExponent,
                self.exponentPart,
        )

    def __str__(self):
        return "{}{}.{}e{}{}".format(
            '+' if self.isPositive else '-',
            self.integerPart,
            '0' if self.fractionPart == '' else self.fractionPart,
            '+' if self.hasPositiveExponent else '-',
            '0' if self.exponentPart == '' else self.exponentPart
        )

isBeginningOfNumber = lambda ch: ch == '-' or ch.isdigit()
def beginParseNumber(ch, dat):
    if isBeginningOfNumber(ch):
        dat["returnValue"] = NumberToken(dat, ch != '-')
    return (
        beginParseIntegerPart(ch, dat) if ch.isdigit()
        else beginParseIntegerPart if ch == '-'
        else JSONLexer.lexingError
    )

def beginParseIntegerPart(ch, dat):
    return (
        changeAndRet(lambda: dat["returnValue"].update('i', ch), endParseIntegerPart) if ch == '0'
        else parseIntegerPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseIntegerPart(ch, dat):
    return (
        changeAndRet(lambda: dat["returnValue"].update('i', ch), parseIntegerPart) if ch.isdigit()
        else endParseIntegerPart(ch, dat)
    )

def endParseIntegerPart(ch, dat):
    return (
        beginParseFractionPart if ch == '.'
        else beginParseExponentPart1 if ch in 'eE'
        else Lexer.JSONLexer.endParse
    )

def beginParseFractionPart(ch, dat):
    return (
        parseFractionPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseFractionPart(ch, dat):
    return (
        changeAndRet(lambda: dat["returnValue"].update('f', ch), parseFractionPart) if ch.isdigit()
        else beginParseExponentPart1 if ch in 'eE'
        else Lexer.JSONLexer.endParse
    )

def beginParseExponentPart1(ch, dat):
    return (
        changeAndRet(lambda: dat["returnValue"].update('se', ch), beginParseExponentPart2) if ch in '+-'
        else beginParseExponentPart2(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def beginParseExponentPart2(ch, dat):
    return (
        parseExponentPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseExponentPart(ch, dat):
    return (
        changeAndRet(lambda: dat["returnValue"].update('e', ch), parseExponentPart) if ch.isdigit()
        else Lexer.JSONLexer.endParse
    )

import Lexer.JSONLexer
