import json
import sys

import requests
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from gui import ForgetPassword
import pyrebase


#each interface defined in a class
class Login(QDialog):

    #cnstructor of the class
    def __init__(self):
        super(Login, self).__init__()
        loadUi("./Interfaces files/LoginPage.ui", self)
        self.login.clicked.connect(self.loginfunc)
        self.password_note.setHidden(True)
        self.closewindow.clicked.connect(lambda: exit())
        self.minmizewindow.clicked.connect(lambda: self.showMinimized())
        self.Fpassword.mousePressEvent = self.forgetPassword
        self.Header.mouseMoveEvent = self.moveWindow
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.show()

    # Move window around
    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    # Opens forget password window
    def forgetPassword(self, eve):
        ForgetPassword.ForgetPassword()

    # Allows window to be clickable
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def loginfunc(self):
        self.password_note.setHidden(True)
        username = self.username.text()
        password = self.password.text()
        if username == "" or password == "":
            self.password_note.setHidden(False)
        else:
            try:
                with open('../db/fbConfig.json') as file:
                    config = json.load(file)
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                self.password_note.text = "Welcome, " + auth.sign_in_with_email_and_password(username, password)["displayName"]
                # self.password_note.setHidden(False)
                print("Success")
            except requests.exceptions.HTTPError:
                # print(json.loads(e.args[1])["error"]["message"])
                self.password_note.setHidden(False)
            except Exception as e:
                print(e)
                print("Something went wrong! Could not login.")


app=QApplication(sys.argv)
mainwindow = Login()
sys.exit(app.exec_())
