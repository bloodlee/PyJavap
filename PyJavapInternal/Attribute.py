__author__ = 'jason'

from PyJavapInternal import ByteToHex, ByteToDec
from PyJavapInternal.ExceptionInfo import ExceptionInfo
from PyJavapInternal import InnerClassAccessFlags

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
            SOURCE_FILE_NAME: SourceFileAttribute.parse,
            SYNTHETIC_NAME: SyntheticAttribute.parse,
            DEPRECATED_NAME: DeprecatedAttribute.parse,
            INNER_CLASSES_NAME: InnerClassesAttribute.parse,
            CONSTANT_VALUE_NAME: ConstantValueAttribute.parse,
        }

        if parserDict.has_key(attrName):
            return parserDict[attrName]
        else:
            return None

class ConstantValueAttribute(Attribute):

    def __init__(self):
        super(ConstantValueAttribute, self).__init__(CONSTANT_VALUE_NAME)

        self.constantValueIndex = -1

    def setValueIndex(self, index):

        self.constantValueIndex = index

    def getValueIndex(self):

        return self.constantValueIndex

    def __str__(self):

        return "Constant Value: #%d" % self.constantValueIndex

    @staticmethod
    def parse(clsFile, result):

        attribute = ConstantValueAttribute()

        classIndex = ByteToDec(clsFile.read(2))

        attribute.setValueIndex(classIndex)

        return attribute

class SyntheticAttribute(Attribute):

    def __init__(self):
        super(SyntheticAttribute, self).__init__(SYNTHETIC_NAME)

    def __str__(self):
        return "Synthetic"

    @staticmethod
    def parse(clsFile, result):

        attribute = SyntheticAttribute()

        return attribute

class DeprecatedAttribute(Attribute):

    def __init__(self):
        super(DeprecatedAttribute, self).__init__(DEPRECATED_NAME)

    def __str__(self):
        return "Deprecated"

    @staticmethod
    def parse(clsFile, result):

        attribute = DeprecatedAttribute()

        return attribute

class InnerClassesAttribute(Attribute):

    class InnerClassesInfo:

        def __init__(self, innerClassIndex, outerClassIndex, innerNameIndex, innerClassAccessFlags):
            self.innerClassIndex = innerClassIndex
            self.outerClassIndex = outerClassIndex
            self.innerNameIndex = innerNameIndex
            self.innerClassAccessFlags = innerClassAccessFlags

        def __str__(self):

            result = ''

            result += '#%d(Inner class #%d, Outer class #%d, Access %s)' % (self.innerNameIndex,
                                                                                    self.innerClassIndex,
                                                                                    self.outerClassIndex, InnerClassAccessFlags.flagToStr(self.innerClassAccessFlags))
            return result

    def __init__(self):

        super(InnerClassesAttribute, self).__init__(INNER_CLASSES_NAME)

        self.classes = []

    def addInnerClass(self, innerClass):

        self.classes.append(innerClass)

    def __str__(self):

        result = ""

        result += "InnerClasses\n"
        result += "==============================\n"

        for innerClass in self.classes:

            result += str(innerClass) + "\n"

        result += "\n"

        return result


    @staticmethod
    def parse(clsFile, result):

        attribute = InnerClassesAttribute()

        numberOfClasses = ByteToDec(clsFile.read(2))

        if numberOfClasses > 0:

            for i in range(numberOfClasses):

                innerClassIndex = ByteToDec(clsFile.read(2))
                outerClassIndex = ByteToDec(clsFile.read(2))
                innerNameIndex = ByteToDec(clsFile.read(2))
                innerClassAccessFlags = ByteToDec(clsFile.read(2))

                innerClassInfo = InnerClassesAttribute.InnerClassesInfo(innerClassIndex, outerClassIndex, innerNameIndex, innerClassAccessFlags)

                attribute.addInnerClass(innerClassInfo)


        return attribute

class SourceFileAttribute(Attribute):

    def __init__(self):

        super(SourceFileAttribute, self).__init__(SOURCE_FILE_NAME)

        self.sourceFileName = ''

    def getSourceFile(self):
        return self.sourceFileName

    def setSourceFile(self, sourceFileName):
        self.sourceFileName = sourceFileName

    def __str__(self):

        return 'Source File: %s' % self.sourceFileName

    @staticmethod
    def parse(clsFile, result):

        attribute = SourceFileAttribute()

        sourceFileIndex = ByteToDec(clsFile.read(2))

        attribute.setSourceFile(result.getUtf8(sourceFileIndex))

        return attribute

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