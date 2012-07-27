__author__ = 'jasonlee'

from PyJavapInternal.ParsingException import ParsingException
from PyJavapInternal import ByteToDec,ByteToHex, ByteTo32BitFloat,ByteTo64BitFloat

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

class ConstantIntegerInfo(ConstantInfo):

    def __init__(self, integer):

        super(ConstantIntegerInfo, self).__init__(CONSTANT_INTEGER_INFO)

        self.integer = integer

    def getInteger(self):

        return self.integer

    def __str__(self):

        return "Integer: %d" % self.integer

    @staticmethod
    def parse(fh):

        assert fh is not None

        return ConstantIntegerInfo(ByteToDec(fh.read(4)))

class ConstantPlaceHolder(ConstantInfo):

    def __init__(self):
        super(ConstantPlaceHolder, self).__init__("PlaceHolder")

    def __str__(self):
        return "PlaceHolder"

class ConstantLongInfo(ConstantInfo):

    def __init__(self, long):

        super(ConstantLongInfo, self).__init__(CONSTANT_LONG_INFO)

        self.long = long

    def getLong(self):

        return self.long

    def __str__(self):

        return "Long: %d" % self.long

    @staticmethod
    def parse(fh):

        assert fh is not None

        return ConstantLongInfo(ByteToDec(fh.read(8)))

class ConstantFloatInfo(ConstantInfo):

    def __init__(self, floatNum):

        super(ConstantFloatInfo, self).__init__(CONSTANT_FLOAT_INFO)

        self.floatNum = floatNum

    def getFloat(self):

        return self.floatNum

    def __str__(self):

        return "Float: %s" % ByteTo32BitFloat(self.floatNum)

    @staticmethod
    def parse(fh):

        assert fh is not None

        return ConstantFloatInfo(fh.read(4))

class ConstantDoubleInfo(ConstantInfo):

    def __init__(self, doubleNum):

        super(ConstantDoubleInfo, self).__init__(CONSTANT_DOUBLE_INFO)

        self.doubleNum = doubleNum

    def getDouble(self):

        return self.doubleNum

    def __str__(self):

        return "Double: %s" % ByteTo64BitFloat(self.doubleNum)

    @staticmethod
    def parse(fh):

        assert fh is not None

        return ConstantDoubleInfo(fh.read(8))

class ConstantStringInfo(ConstantInfo):

    def __init__(self, stringIndex):

        super(ConstantStringInfo, self).__init__(CONSTANT_STRING_INFO)

        self.stringIndex = stringIndex

    def getStringIndex(self):

        return self.stringIndex

    def __str__(self):

        return "String: #%d" % self.stringIndex

    @staticmethod
    def parse(fh):

        assert fh is not None

        return ConstantStringInfo(ByteToDec(fh.read(2)))

class ConstantFieldrefInfo(ConstantInfo):

    def __init__(self, hostClassIndex, nameAndTypeIndex):

        super(ConstantFieldrefInfo, self).__init__(CONSTANT_FIELDREF_INFO)

        self.hostClassIndex = hostClassIndex
        self.nameAndTypeIndex = nameAndTypeIndex

    def getFieldClassIndex(self):

        return self.hostClassIndex

    def getNameAndTypeIndex(self):

        return self.nameAndTypeIndex

    def __str__(self):

        return 'Fieldref: #%d (#%d)' % (self.hostClassIndex, self.nameAndTypeIndex)

    @staticmethod
    def parse(fh):

        assert fh is not None

        classInfoIndex = ByteToDec(fh.read(2))
        nameAndTypeIndex = ByteToDec(fh.read(2))

        return ConstantFieldrefInfo(classInfoIndex, nameAndTypeIndex)

class ConstantMethodrefInfo(ConstantInfo):

    def __init__(self, hostClassIndex, nameAndTypeIndex):

        super(ConstantMethodrefInfo, self).__init__(CONSTANT_METHODREF_INFO)

        self.hostClassIndex = hostClassIndex
        self.nameAndTypeIndex = nameAndTypeIndex

    def getFieldClassIndex(self):

        return self.hostClassIndex

    def getNameAndTypeIndex(self):

        return self.nameAndTypeIndex

    def __str__(self):

        return 'Methodref: #%d (#%d)' % (self.hostClassIndex, self.nameAndTypeIndex)

    @staticmethod
    def parse(fh):

        assert fh is not None

        classInfoIndex = ByteToDec(fh.read(2))
        nameAndTypeIndex = ByteToDec(fh.read(2))

        return ConstantMethodrefInfo(classInfoIndex, nameAndTypeIndex)

class ConstantInterfacerefInfo(ConstantInfo):

    def __init__(self, hostClassIndex, nameAndTypeIndex):

        super(ConstantInterfacerefInfo, self).__init__(CONSTANT_INTERFACEMETHODREF_INFO)

        self.hostClassIndex = hostClassIndex
        self.nameAndTypeIndex = nameAndTypeIndex

    def getFieldClassIndex(self):

        return self.hostClassIndex

    def getNameAndTypeIndex(self):

        return self.nameAndTypeIndex

    def __str__(self):

        return 'Interfaceref: #%d (#%d)' % (self.hostClassIndex, self.nameAndTypeIndex)

    @staticmethod
    def parse(fh):

        assert fh is not None

        classInfoIndex = ByteToDec(fh.read(2))
        nameAndTypeIndex = ByteToDec(fh.read(2))

        return ConstantInterfacerefInfo(classInfoIndex, nameAndTypeIndex)


class ConstantNameAndTypeInfo(ConstantInfo):

    def __init__(self, nameIndex, descriptorIndex):

        super(ConstantNameAndTypeInfo, self).__init__(CONSTANT_NAMEANDTYPE_INFO)

        self.nameIndex = nameIndex
        self.descriptorIndex = descriptorIndex

    def getNameIndex(self):

        return self.nameIndex

    def getDescriptorIndex(self):

        return self.descriptorIndex

    def __str__(self):

        return 'NameAndType: #%d.#%d' % (self.nameIndex, self.descriptorIndex)

    @staticmethod
    def parse(fh):

        assert fh is not None

        nameIndex = ByteToDec(fh.read(2))
        descriptorIndex = ByteToDec(fh.read(2))

        return ConstantNameAndTypeInfo(nameIndex, descriptorIndex)



class ConstantPool:
    """
    Utility to parse to constant pool of java class.
    """
    @staticmethod
    def getHandler(type):

        handlers = {
            CONSTANT_CLASS_INFO: ConstantClassInfo.parse,
            CONSTANT_UTF8_INFO: ConstantUTF8Info.parse,
            CONSTANT_INTEGER_INFO: ConstantIntegerInfo.parse,
            CONSTANT_LONG_INFO: ConstantLongInfo.parse,
            CONSTANT_FLOAT_INFO: ConstantFloatInfo.parse,
            CONSTANT_DOUBLE_INFO: ConstantDoubleInfo.parse,
            CONSTANT_STRING_INFO: ConstantStringInfo.parse,
            CONSTANT_FIELDREF_INFO: ConstantFieldrefInfo.parse,
            CONSTANT_METHODREF_INFO: ConstantMethodrefInfo.parse,
            CONSTANT_INTERFACEMETHODREF_INFO: ConstantInterfacerefInfo.parse,
            CONSTANT_NAMEANDTYPE_INFO: ConstantNameAndTypeInfo.parse,
        }

        if handlers.has_key(type):
            return handlers[type]
        else:
            return None

    @staticmethod
    def getContentBytes(type):

        typeContentBytes = {
            CONSTANT_UTF8_INFO:      2,
            CONSTANT_INTEGER_INFO:   4,
            CONSTANT_FLOAT_INFO:     4,
            CONSTANT_LONG_INFO:      8,
            CONSTANT_DOUBLE_INFO:    8,
            CONSTANT_CLASS_INFO:     2,
            CONSTANT_STRING_INFO:    2,
            CONSTANT_FIELDREF_INFO:  4,
            CONSTANT_METHODREF_INFO: 4,
            CONSTANT_INTERFACEMETHODREF_INFO: 4,
            CONSTANT_NAMEANDTYPE_INFO: 4
        }

        if typeContentBytes.has_key(type):
            return typeContentBytes[type]
        else:
            return 0

    @staticmethod
    def parse(count, fh):
        constants = []

        skipped = False

        for index in range(count):

            if skipped:
                skipped = False
                constants.append(ConstantPlaceHolder())
                continue

            type = ByteToDec(fh.read(1))

            handler = ConstantPool.getHandler(type)
            if handler is not None:
                attribute = handler(fh)
                constants.append(attribute)
            else:
                readBytes = ConstantPool.getContentBytes(type)
                if readBytes:
                    fh.read(readBytes)
                    constants.append(None)

            if type == CONSTANT_LONG_INFO or type == CONSTANT_DOUBLE_INFO:
                skipped = True

        return constants


