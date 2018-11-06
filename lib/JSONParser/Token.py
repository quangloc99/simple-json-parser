class Token:
    def __init__(self):
        pass

    def isValue(self):
        return False

    def toPytnonValue(self):
        raise ValueError("Cannot convert type %s to Python value" % type(self).__name__)
