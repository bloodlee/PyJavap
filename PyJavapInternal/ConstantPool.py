__author__ = 'jasonlee'

from PyJavapInternal.ParsingException import ParsingException
from PyJavapInternal import ByteToDec

CONSTANT_UTF8_INFO = 0x01
CONSTANT_INTEGER_INFO = 0x03
CONSTANT_FLOAT_INFO = 0x04
CONSTANT_LONG_INFO = 0x05
CONSTANT_DOUBLE_INFO = 0x06
CONSTANT_CLASS_INFO = 0x07
CONSTANT_STRING_INFO = 0x08
CONSTANT_FIELDREF_INFO = 0x09
CONSTANT_METHODREF_INFO = 0x0A
CONSTANT_INTERFACEMETHODREF_INFO = 0x0B
CONSTANT_NAMEANDTYPE_INFO = 0x0C

TYPE_UTF8 = "UTF8"

class ConstantInfo(object):
    """
    Base class of constant info.
    """

    def __init__(self, typeTag):
        self.type = typeTag

    def getTypeTag(self):
        return self.type

    def getTypeName(self):
        raise ParsingException("Not implement this function in ConstantInfo")

class ConstantClassInfo(ConstantInfo):
    """
    Constant Class Info
    """

    def __init__(self, nameIndex):
        super(ConstantClassInfo, self).__init__(CONSTANT_CLASS_INFO)
        self.nameIndex = nameIndex

    def setNameIndex(self, nameIndex):
        self.nameIndex = nameIndex

    def getNameIndex(self):
        return self.nameIndex

    def getTypeName(self):
        return "ClassInfo"

    def __str__(self):
        return "%s: #%d" % (self.getTypeName(), self.getNameIndex())

    @staticmethod
    def parse(fh): # fh stands for file handler
        """
        Constant class section has 3 bytes.
        """

        assert fh is not None

        nameIndex = ByteToDec(fh.read(2))

        return ConstantClassInfo(nameIndex)

class ConstantUTF8Info(ConstantInfo):
    """
    Constant UTF8 Info
    """

    def __init__(self, length, utf8):
        super(ConstantUTF8Info, self).__init__(CONSTANT_UTF8_INFO)
        self.length = length
        self.utf8 = utf8

    def getTypeName(self):
        return TYPE_UTF8

    def __str__(self):
        return "%s: %s (%d chars)" % (self.getTypeName(), self.utf8, self.length)

    def getUtf8(self):
        return self.utf8

    @staticmethod
    def parse(fh):
        """
        Constant UTF8 section
        """

        assert fh is not None

        length = ByteToDec(fh.read(2))
        content = fh.read(length)

        return ConstantUTF8Info(length, content)

class ConstantPool:
    """
    Utility to parse to constant pool of java class.
    """
    @staticmethod
    def getHandler(type):

        handlers = {
            CONSTANT_CLASS_INFO: ConstantClassInfo.parse,
            CONSTANT_UTF8_INFO: ConstantUTF8Info.parse,
        }

        if handlers.has_key(type):
            return handlers[type]
        else:
            return None

    @staticmethod
    def getContentBytes(type):

        typeContentBytes = {
            CONSTANT_UTF8_INFO: 2,
            CONSTANT_INTEGER_INFO: 4,
            CONSTANT_FLOAT_INFO: 4,
            CONSTANT_LONG_INFO: 8,
            CONSTANT_DOUBLE_INFO: 8,
            CONSTANT_CLASS_INFO: 2,
            CONSTANT_STRING_INFO: 2,
            CONSTANT_FIELDREF_INFO: 2 + 2,
            CONSTANT_METHODREF_INFO: 2 + 2,
            CONSTANT_INTERFACEMETHODREF_INFO: 2 + 2,
            CONSTANT_NAMEANDTYPE_INFO: 4
        }

        return typeContentBytes[type]

    @staticmethod
    def parse(count, fh):
        constants = []

        for index in range(count):
            type = ByteToDec(fh.read(1))

            handler = ConstantPool.getHandler(type)
            if handler is not None:
                constants.append(handler(fh))
            else:
                # skip several bytes
                if type == CONSTANT_UTF8_INFO:
                    # content bytes of UTF8 is variant,
                    # we need to read the length first
                    # then skip the bytes
                    length = ByteToDec(fh.read(2))
                    fh.read(length)
                else:
                    fh.read(ConstantPool.getContentBytes(type))

                constants.append(None)

        return constants


