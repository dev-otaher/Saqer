from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import re
from gui import ForgetPassSuccess


class ForgetPassword(QDialog):
    def __init__(self):
        super(ForgetPassword, self).__init__()
        loadUi("gui/Interfaces files/ForgetPassword.ui", self)
        self.i_send.clicked.connect(self.sendEmail)
        self.i_close.clicked.connect(lambda: self.hide())
        self.i_password_note.setHidden(True)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint ))
        self.i_Header.mouseMoveEvent = self.moveWindow
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    #move window around
    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    #This function runs when the 'Send' button clicked
    def sendEmail(self):
        pattern = r"\"?([-a-zA-Z0-9_.`?{}]+@\w+\.\w+)\"?"
        re.compile(pattern)
        email = self.i_email.text()
        if email == "" or not re.match(pattern,email):
            self.i_password_note.setHidden(False)
        else:
            ForgetPassSuccess.ForgetPassSuccess()
            self.destroy()
