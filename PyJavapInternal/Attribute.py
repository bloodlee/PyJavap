__author__ = 'jason'

from PyJavapInternal import ByteToHex, ByteToDec
from PyJavapInternal.ExceptionInfo import ExceptionInfo

CODE_NAME = 'Code'
LINE_NUMBER_TABLE_NAME = 'LineNumberTable'
LOCAL_VARIABLE_TABLE_NAME = "LocalVariableTable"
SOURCE_FILE_NAME = 'SourceFile'
CONSTANT_VALUE_NAME = 'ConstantValue'
INNER_CLASSES_NAME = 'InnerClasses'
DEPRECATED_NAME = 'Deprecated'
SYNTHETIC_NAME = 'Synthetic'

class Attribute(object):

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    @staticmethod
    def getParser(attrName):

        parserDict = {
            CODE_NAME: CodeAttribute.parse,
            LINE_NUMBER_TABLE_NAME: LineNumberTableAttribute.parse,
            LOCAL_VARIABLE_TABLE_NAME: LocalVariableTableAttribute.parse,
        }

        if parserDict.has_key(attrName):
            return parserDict[attrName]
        else:
            return None

class LocalVariableTableAttribute(Attribute):

    class LocalVarInfo(object):

        def __init__(self, startPC, length, name, descriptor, index):
            self.startPC = startPC
            self.length = length
            self.name = name
            self.descriptor = descriptor
            self.index = index

        def __str__(self):
            return "Var: %s(%s) startPC: %d length: %d index: %d" % (self.name, self.descriptor, self.startPC, self.length, self.index)

    def __init__(self):
        super(LocalVariableTableAttribute, self).__init__(LOCAL_VARIABLE_TABLE_NAME)
        self.varInfos = []

    def addVarInfo(self, varInfo):
        self.varInfos.append(varInfo)

    def __str__(self):

        result = ""

        result += "Local Variable Table\n"
        result += "===============================\n"

        for varInfo in self.varInfos:
            result += str(varInfo) + "\n"

        result += "\n"

        return result

    @staticmethod
    def parse(clsFile, result):

        attribute = LocalVariableTableAttribute()

        variableCount = ByteToDec(clsFile.read(2))

        for i in range(variableCount):
            startPC = ByteToDec(clsFile.read(2))
            length = ByteToDec(clsFile.read(2))
            argName = result.getUtf8(ByteToDec(clsFile.read(2)))
            descriptorName = result.getUtf8(ByteToDec(clsFile.read(2)))
            index = ByteToDec(clsFile.read(2))

            info = LocalVariableTableAttribute.LocalVarInfo(startPC, length, argName, descriptorName, index)

            attribute.addVarInfo(info)

        return attribute


class LineNumberTableAttribute(Attribute):
    def __init__(self):
        super(LineNumberTableAttribute, self).__init__(LINE_NUMBER_TABLE_NAME)

        # a dict {start_pc, line_number}
        self.code2Line = {}

    def getCode2Line(self):

        return self.code2Line

    def addCode2Line(self, startPC, lineNumber):
        self.code2Line[startPC] = lineNumber

    def __str__(self):
        result = ""
        result += "LineNumberTable\n"
        result += "======================\n"

        for aKey in self.code2Line.keys():
            result += "%5d -> %5d\n" % (aKey, self.code2Line[aKey])

        result += "\n"

        return result

    @staticmethod
    def parse(clsFile, result):

        attribute = LineNumberTableAttribute()

        tableLen = ByteToDec(clsFile.read(2))

        for i in range(tableLen):
            startPC = ByteToDec(clsFile.read(2))
            lineNumber = ByteToDec(clsFile.read(2))

            attribute.addCode2Line(startPC, lineNumber)

        return attribute


class CodeAttribute(Attribute):

    def __init__(self):
        super(CodeAttribute, self).__init__(CODE_NAME)

        self.maxStack = -1
        self.maxLocal = -1

        self.exceptions = []

        self.code = None

        self.attributes = []

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

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

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

        for subAttr in self.attributes:
            result += str(subAttr)
            result += "\n"

        return result

    @staticmethod
    def parse(clsFile, result):
        codeAttr = CodeAttribute()

        maxStack = ByteToDec(clsFile.read(2))
        maxLocal = ByteToDec(clsFile.read(2))

        codeLength = ByteToDec(clsFile.read(4))
        code = ByteToHex(clsFile.read(codeLength))

        codeAttr.setMaxStack(maxStack)
        codeAttr.setMaxLocal(maxLocal)
        codeAttr.setCode(code)

        exceptionLen = ByteToDec(clsFile.read(2))
        if exceptionLen > 0:
            for i in range(exceptionLen):
                startPC = ByteToDec(clsFile.read(2))
                endPC = ByteToDec(clsFile.read(2))
                handlerPC = ByteToDec(clsFile.read(2))
                classIndex = ByteToDec(clsFile.read(2))

                exceptionClassName = "any"
                if classIndex > 0: # if class index is 0, the class name is any.
                    exceptionClassName = result.getClassName(classIndex)

                exceptionInfo = ExceptionInfo(startPC, endPC, handlerPC, exceptionClassName)

                codeAttr.addException(exceptionInfo)

        subAttrCount = ByteToDec(clsFile.read(2))
        if subAttrCount > 0:
            for i in range(subAttrCount):
                subAttr = result.getUtf8(ByteToDec(clsFile.read(2)))
                subAttrLength = ByteToDec(clsFile.read(4))

                parser = Attribute.getParser(subAttr)
                if parser is not None:
                    attribute = parser(clsFile, result)
                    codeAttr.addAttribute(attribute)
                else:
                    clsFile.read(subAttrLength)

        return codeAttr