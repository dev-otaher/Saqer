from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import re
from Saqer.gui import ForgetPassSuccess


#The forget password window class
class ForgetPassword(QDialog):
    #the class constructor
    def __init__(self):
        super(ForgetPassword, self).__init__()
        loadUi("./Interfaces files/ForgetPassword.ui", self)
        self.send.clicked.connect(self.SendFunction)
        self.close.clicked.connect(lambda: self.hide())
        self.password_note.setHidden(True)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint ))
        self.Header.mouseMoveEvent = self.moveWindow
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    #moving forget password around
    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    #This function runs when the 'Send' button clicked
    def SendFunction(self):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        re.compile(pattern)
        email = self.email.text()

        if email == "":
            self.password_note.setHidden(False)
        elif not re.match(pattern,email):
            self.password_note.setHidden(False)
        else:
            ForgetPassSuccess.ForgetPassSuccess()
            self.destroy()