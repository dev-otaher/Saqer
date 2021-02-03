from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ForgetPassSuccess(QDialog):

    def __init__(self):
        super(ForgetPassSuccess, self).__init__()
        loadUi("gui/interfaces/ForgetPasswordSuccess.ui", self)
        self.i_Hide.clicked.connect(lambda: self.hide())
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowModality(Qt.ApplicationModal)
        self.show()


