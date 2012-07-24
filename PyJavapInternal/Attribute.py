__author__ = 'jason'

__CODE_NAME = 'Code'

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
        super(CodeAttribute, self).__init__(__CODE_NAME, length)

        self.maxStack = -1
        self.maxLocals = -1
