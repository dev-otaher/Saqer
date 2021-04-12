import os
import sys

from PyQt5 import QtWidgets

from gui.Login import Login

print(os.getcwd())
app = QtWidgets.QApplication(sys.argv)
window = Login()
app.exec_()
