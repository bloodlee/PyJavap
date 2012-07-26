__author__ = 'yli'

import sys
from PyQt4.QtGui import QApplication, QPushButton

app = QApplication(sys.argv)
button = QPushButton("Hello,World")
button.show()

sys.exit(app.exec_())