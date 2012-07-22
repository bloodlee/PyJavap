__author__ = 'jasonlee'

class ParsingException(Exception):
    """
    Define the exception during parsing
    """

    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)


