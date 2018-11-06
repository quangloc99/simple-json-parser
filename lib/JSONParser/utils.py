import string
def doThenRet(actions, ret):
    actions()
    return ret

specialYAMLChars = set(string.digits + ':{}[],&*#?|-<>=!%@\\ ')

convertTable = {
        "\\": "\\",
        "\"": "\"",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r"
}

def convertChar(ch):
    if len(ch) == 1:
        return ch
    if ch[1] in convertTable:
        return convertTable[ch[1]]
    if ch[1] == 'u':
        return chr(int(ch[2:], 16))
    raise ValueError


