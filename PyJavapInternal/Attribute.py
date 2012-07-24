__author__ = 'jason'

from PyJavapInternal import ByteToHex

CODE_NAME = 'Code'

class Attribute(object):

    def __init__(self, name, length):
        self.name = name
        self.length = length

    def getName(self):
        return self.name

    def getLength(self):
        return self.length


class CodeAttribute(Attribute):

    def __init__(self, length):
        super(CodeAttribute, self).__init__(CODE_NAME, length)

        self.maxStack = -1
        self.maxLocal = -1

        self.exceptions = []

        self.code = None

    @staticmethod
    def getAttrName():
        return CODE_NAME

    def setMaxStack(self, maxStack):
        self.maxStack = maxStack

    def setMaxLocal(self, maxLocal):
        self.maxLocal = maxLocal

    def setCode(self, code):
        self.code = code

    def addException(self, exception):
        self.exceptions.append(exception)

    def __str__(self):

        result = ""

        result += "\tCodeAttr\n"
        result += "\t\tMax Stack: %d Max Local: %d\n" % (self.maxStack, self.maxLocal)
        result += "\t\tCode: " + self.code + "\n"

        if len(self.exceptions) > 0:

            result += "\t\tExceptions\n"
            result += "\t\t================\n"
            result += "\t\tStart\tEnd\tHandler\tClass\n"

            for i in range(len(self.exceptions)):
                result += "\t\t" + str(self.exceptions[i]) + "\n"

        return result
