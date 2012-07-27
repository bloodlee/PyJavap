__author__ = 'jason'

from PyJavapInternal import FieldAccessFlags

class Field(object):

    def __init__(self, name, descriptor, access):
        self.name = name
        self.descriptor = descriptor
        self.access = access
        self.attrCount = 0
        self.attributes = []

    def addAttribute(self, attribute):
        self.attrCount += 1
        self.attributes.append(attribute)

    def __str__(self):
        result = "Name: " + self.name + "(" + self.descriptor + ")"
        result += " Access: " + FieldAccessFlags.flagToStr(self.access)

        result += "\n"

        if len(self.attributes):
            result += "\tAttributes\n"
            for attr in self.attributes:
                result += "\t" + str(attr) + "\n"

        return result






