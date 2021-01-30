import json
import sys
import time

import requests
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from gui import ForgetPassword
import pyrebase


# each interface defined in a class
class Login(QDialog):

    # class constructor
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("gui/Interfaces files/LoginPage.ui", self)
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
        username = self.username.text().strip()
        password = self.password.text()
        if username == "" or password == "":
            self.password_note.setHidden(False)
        else:
            try:
                with open('db/fbConfig.json') as file:
                    config = json.load(file)
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                db = firebase.database()
                user = auth.sign_in_with_email_and_password(username, password)
                isAdmin = db.child("users").child(str(user["localId"])).child("isAdmin").get()
                if isAdmin.val() == "True":
                    print("Is admin...")
                else:
                    print("Is instructor...")
            except requests.exceptions.HTTPError as e:
                print(e)
                # print(json.loads(e.args[1])["error"]["message"])
                self.password_note.setHidden(False)
            except Exception as e:
                print(e)
                print("Something went wrong! Could not login.")
