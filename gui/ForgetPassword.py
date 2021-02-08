from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import json
from gui import ForgetPassSuccess
import pyrebase


class ForgetPassword(QDialog):
    def __init__(self):
        super(ForgetPassword, self).__init__()
        loadUi("gui/interfaces/ForgetPassword.ui", self)
        self.i_send.clicked.connect(self.sendEmail)
        self.i_close.clicked.connect(lambda: self.hide())
        self.i_password_note.setHidden(True)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint ))
        self.i_Header.mouseMoveEvent = self.moveWindow
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    # Move window around
    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    # This function runs when the 'Send' button clicked
    def sendEmail(self):
        try:
            pattern = r"\"?([-a-zA-Z0-9_.`?{}]+@\w+\.\w+)\"?"
            re.compile(pattern)
            email = self.email.text().strip()
            if email == "" or not re.match(pattern,email):
                self.i_password_note.setHidden(False)
            else:
                with open('db/fbConfig.json') as file:
                  config = json.load(file)
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                auth.send_password_reset_email(email)
                ForgetPassSuccess.ForgetPassSuccess()
                self.destroy()
        except Exception as e:
            # if there's error in the email authentication show error message
            self.password_note.setHidden(False)
