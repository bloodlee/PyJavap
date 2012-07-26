__author__ = 'jason'

import ui_MainDlg

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyJavapInternal.Parser import Parser
from PyJavapInternal.ParsingResult import ParsingResult
from PyJavapInternal.ParsingException import ParsingException
from PyJavapInternal import ByteToDec, ByteToHex
from PyJavapInternal import ClassAccessFlags

class PyAnalyzerMainDialog(QDialog, ui_MainDlg.Ui_Dialog):

    def __init__(self, parent=None):
        super(PyAnalyzerMainDialog, self).__init__(parent)

        self.setupUi(self)

        QObject.connect(self.loadButton, SIGNAL(QString.fromUtf8("pressed()")), self.loadClassFile)
        QMetaObject.connectSlotsByName(self)

        self.update()

    def loadClassFile(self):

        fileName = QFileDialog.getOpenFileName(self, QString.fromUtf8("Select a Java class file"), '.', QString.fromUtf8("Java Class (*.class)"))

        if fileName:

            self.classFileText.setText(fileName)

            parser = Parser(fileName)

            try:
                result = parser.parse()
                print result

                self.magicNumText.setText(ByteToHex(result.getMagicNumber()))

                (majVer, minVer) = result.getVersions()

                self.majVerText.setText(str(majVer))
                self.minVerText.setText(str(minVer))

                self.accessFlagText.setText(ClassAccessFlags.flagToStr(result.getAccessFlag()))

                constants = result.getConstants()
                self.tabWidget.setTabText(1, "Constant Pool (%d)" % len(constants))

            except ParsingException,e:
                print e

        else:
            print 'Select nothing.'