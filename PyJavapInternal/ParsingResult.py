__author__ = 'jasonlee'

import PyJavapInternal

class ParsingResult:

    def __init__(self, cls_file_name):
        self.cls_file_name = cls_file_name
        self.magicNumber = [0xff, 0xff, 0xff, 0xff]
        self.majorVer = -1
        self.minorVer = -1

        self.const_pool_count = -1
        self.constants = None

    def setMagicNumber(self, magicNumber):
        self.magicNumber = magicNumber

    def setVersion(self, major, minor):
        self.majorVer = major
        self.minorVer = minor

    def setConstPoolCount(self, count):
        self.const_pool_count = count

    def setConstants(self, constants):
        self.constants = constants

    def __str__(self):

        result = ""

        result += "File Name: %s\n" % self.cls_file_name
        result += "Magic Number: %s\n" % PyJavapInternal.ByteToHex(self.magicNumber)
        result += "Major Version: %d\n" % self.majorVer
        result += "Minor Version: %d\n" % self.minorVer

        result += "Constant Pool (Count %d)\n" % self.const_pool_count

        if self.const_pool_count > 0 and self.constants is not None and len(self.constants) == self.const_pool_count:
            result += "==========================\n"

            for i in range(self.const_pool_count):
                result += 'Const %d: %s\n' % (i + 1, str(self.constants[i]))

        return result
