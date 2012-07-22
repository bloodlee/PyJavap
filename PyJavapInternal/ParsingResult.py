__author__ = 'jasonlee'

import PyJavapInternal

class ParsingResult:

    def __init__(self, cls_file_name):
        self.cls_file_name = cls_file_name

    def setMagicNumber(self, magicNumber):
        self.magicNumber = magicNumber

    def __str__(self):

        result = ""

        result += "File Name: %s\n" % self.cls_file_name
        result += "Magic Number: %s\n" % PyJavapInternal.ByteToHex(self.magicNumber)

        return result
