import os
import sys
from PyQt5 import QtWidgets
from gui.Splash import Loading

print(os.getcwd())
app = QtWidgets.QApplication(sys.argv)
window = Loading()
app.exec_()
