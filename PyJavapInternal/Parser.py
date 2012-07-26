__author__ = 'jasonlee'

import os.path
import os
from PyJavapInternal.ParsingResult import ParsingResult
from PyJavapInternal.ParsingException import ParsingException
from PyJavapInternal import ByteToDec
from PyJavapInternal.ConstantPool import ConstantPool
from PyJavapInternal.Field import Field
from PyJavapInternal.Method import Method
from PyJavapInternal.Attribute import Attribute
from PyJavapInternal.Attribute import *
from PyJavapInternal.ExceptionInfo import ExceptionInfo

class Parser:


    def __init__(self, cls_file_name):
        self.cls_file_name = cls_file_name
        self.result = ParsingResult(self.cls_file_name)
        self.clsFile = None

    def __verify(self):
        """
        Verify the given arguments.
        """

        if not (os.path.exists(self.cls_file_name) and os.path.isfile(self.cls_file_name)):
            raise ParsingException("Can't find the class file %s" % self.cls_file_name)

    def __parseMagicNum(self):
        """
        Parse the magic num (the first 4 bytes)
        """

        assert self.clsFile is not None

        # get first four bytes
        magicNumBytes = self.clsFile.read(4)
        self.result.setMagicNumber(magicNumBytes)

    def __parseVersion(self):
        """
        Parse the version of this class file.
        Version is composed by minor version and major version.
        Each will occupy 2 bytes.
        """

        assert self.clsFile is not None

        majorVerBytes = self.clsFile.read(2)
        minorVerBytes = self.clsFile.read(2)

        self.result.setVersion(ByteToDec(minorVerBytes), ByteToDec(majorVerBytes))

    def __parseConstantPool(self):
        """
        Parse the constant pool of class file
        First 2 bytes of this section is the count.
        Pay attention here. Constant index starts from 1, not 0.
        """

        assert self.clsFile is not None

        const_count = ByteToDec(self.clsFile.read(2)) - 1
        self.result.setConstPoolCount(const_count)

        constants = ConstantPool.parse(const_count, self.clsFile)
        self.result.setConstants(constants)


    def __parseAccessFlag(self):
        """
        Parse the access flag
        """

        assert self.clsFile is not None

        accessFlag = ByteToDec(self.clsFile.read(2))
        self.result.setAccessFlag(accessFlag)

    def __parseThis(self):
        """
        Parse "this" section
        """

        assert self.clsFile is not None

        thisIndex = ByteToDec(self.clsFile.read(2))
        self.result.setThisIndex(thisIndex)

    def __parseSuper(self):
        """
        Parse "super" section
        """

        assert self.clsFile is not None

        superIndex = ByteToDec(self.clsFile.read(2))
        self.result.setSuperIndex(superIndex)

    def __parseInterface(self):
        """
        Parse "interface" section
        """

        assert self.clsFile is not None

        interfaceCount = ByteToDec(self.clsFile.read(2))

        interfaceIndex = []
        if interfaceCount > 0:
            for i in range(interfaceCount):
                interfaceIndex.append(ByteToDec(self.clsFile.read(2)))

        self.result.setInterfaces(interfaceCount, interfaceIndex)

    def __parseFields(self):
        """
        Parse fields sections.
        """

        assert self.clsFile is not None

        fieldCount = ByteToDec(self.clsFile.read(2))

        fields = []
        for index in range(fieldCount):
            accessFlag = ByteToDec(self.clsFile.read(2))
            name = self.result.getUtf8(ByteToDec(self.clsFile.read(2)))
            descriptor = self.result.getUtf8(ByteToDec(self.clsFile.read(2)))

            field = Field(name, descriptor, accessFlag)

            attrCount = ByteToDec(self.clsFile.read(2))
            if attrCount > 0:
                for i in range(attrCount):
                    attributeIndex = self.clsFile.read(2)
                    attributeLength = ByteToDec(self.clsFile.read(4))
                    self.clsFile.read(attributeLength)

            fields.append(field)

        self.result.setFields(fieldCount, fields)

    def __parseMethods(self):
        """
        Parse methods section.
        """

        assert  self.clsFile is not None

        methodCount = ByteToDec(self.clsFile.read(2))

        methods = []
        for index in range(methodCount):
            accessFlag = ByteToDec(self.clsFile.read(2))
            name = self.result.getUtf8(ByteToDec(self.clsFile.read(2)))
            descriptor = self.result.getUtf8(ByteToDec(self.clsFile.read(2)))

            method = Method(name, descriptor, accessFlag)

            attrCount = ByteToDec(self.clsFile.read(2))
            if attrCount > 0:
                for i in range(attrCount):
                    attributeName = self.result.getUtf8(ByteToDec(self.clsFile.read(2)))
                    attributeLength = ByteToDec(self.clsFile.read(4))

                    # for now, only parse the "Code Attribute
                    parser = Attribute.getParser(attributeName)

                    if parser is not None:
                        attribute = parser(self.clsFile, self.result)
                        method.addAttribute(attribute)
                    else:
                        self.clsFile.read(attributeLength)

            methods.append(method)

        self.result.setMethods(methodCount, methods)


    def parse(self):

        try:
            self.__verify()

            # parse the magic number of class file
            self.clsFile = open(self.cls_file_name, 'rb')

            # following functions' order is very important
            self.__parseMagicNum()
            self.__parseVersion()
            self.__parseConstantPool()
            self.__parseAccessFlag()
            self.__parseThis()
            self.__parseSuper()
            self.__parseInterface()
            self.__parseFields()
            self.__parseMethods()

        except ParsingException,e:

            raise e

        finally:
            if self.clsFile:
                self.clsFile.close()
                self.clsFile = None

        return self.result


