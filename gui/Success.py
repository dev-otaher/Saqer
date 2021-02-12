from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class Success(QDialog):

    def __init__(self, msg:str):
        super(Success, self).__init__()
        loadUi("gui/interfaces/Success.ui", self)
        self.i_hide.clicked.connect(lambda: self.hide())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowModality(Qt.ApplicationModal)
        self.i_message.setText(msg)
        self.show()


