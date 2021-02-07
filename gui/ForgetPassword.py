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
        loadUi("./Interfaces files/ForgetPassword.ui", self)
        self.send.clicked.connect(self.sendEmail)
        self.close.clicked.connect(lambda: self.hide())
        self.password_note.setHidden(True)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.Header.mouseMoveEvent = self.moveWindow
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
            # get the email text
            email = self.email.text().strip()
            # open the firebase credentials and initialize the app
            # and instantiate the authentication service
            with open('db/fbConfig.json') as file:
                config = json.load(file)
            firebase = pyrebase.initialize_app(config)

            auth = firebase.auth()
            # if the email is successfully entered then send
            # the password reset steps and show success message
            auth.send_password_reset_email(email)
            ForgetPassSuccess.ForgetPassSuccess()
            self.destroy()
        except Exception as e:
            # if there's error in the email authentication show error message
            self.password_note.setHidden(False)
