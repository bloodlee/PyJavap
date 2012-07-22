__author__ = 'jasonlee'

import os.path
import os
from PyJavapInternal.ParsingResult import ParsingResult
import types

class Parser:

    def __init__(self, cls_file_name):
        self.cls_file_name = cls_file_name

    def __verify(self):

        if not (os.path.exists(self.cls_file_name) and os.path.isfile(self.cls_file_name)):
            print("Can't find the class file")
            return False

        return True

    def parse(self):

        if self.__verify():

            result = ParsingResult(self.cls_file_name)

            clsFile = None
            try:
                # parse the magic number of class file
                with open(self.cls_file_name, 'rb') as clsFile:

                    # get first four bytes
                    magicNumBytes = clsFile.read(4)
                    result.setMagicNumber(magicNumBytes)

                    return result

            finally:
                clsFile.close()


        return None