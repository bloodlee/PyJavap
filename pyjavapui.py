__author__ = 'yli'

import sys
from PyQt4.QtGui import QApplication
from PyJavapGuiInternal.PyAnalyzerMainDialog import PyAnalyzerMainDialog

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainDlg = PyAnalyzerMainDialog()
    mainDlg.show()

    sys.exit(app.exec_())