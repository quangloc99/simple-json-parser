from Lexer.Base import LexToken, doThenRet

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
def beginParsingNumber(ch, dat):
    if isBeginningOfNumber(ch):
        dat["returnValue"] = NumberToken(dat, ch != '-')
    return (
        beginParsingIntegerPart(ch, dat) if ch.isdigit()
        else beginParsingIntegerPart if ch == '-'
        else JSONLexer.lexingError
    )

def beginParsingIntegerPart(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].update('i', ch), endParsingIntegerPart) if ch == '0'
        else parseIntegerPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseIntegerPart(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].update('i', ch), parseIntegerPart) if ch.isdigit()
        else endParsingIntegerPart(ch, dat)
    )

def endParsingIntegerPart(ch, dat):
    return (
        beginParsingFractionPart if ch == '.'
        else beginParsingExponentPart1 if ch in 'eE'
        else Lexer.JSONLexer.endParsing
    )

def beginParsingFractionPart(ch, dat):
    return (
        parseFractionPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseFractionPart(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].update('f', ch), parseFractionPart) if ch.isdigit()
        else beginParsingExponentPart1 if ch in 'eE'
        else Lexer.JSONLexer.endParsing
    )

def beginParsingExponentPart1(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].update('se', ch), beginParsingExponentPart2) if ch in '+-'
        else beginParsingExponentPart2(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def beginParsingExponentPart2(ch, dat):
    return (
        parseExponentPart(ch, dat) if ch.isdigit()
        else JSONLexer.lexingError
    )

def parseExponentPart(ch, dat):
    return (
        doThenRet(lambda: dat["returnValue"].update('e', ch), parseExponentPart) if ch.isdigit()
        else Lexer.JSONLexer.endParsing
    )

import Lexer.JSONLexer
