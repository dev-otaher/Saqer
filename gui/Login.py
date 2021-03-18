import json
import sys
import requests
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from gui import ForgetPassword
import pyrebase


class Login(QDialog):

    # constructor of the class
    def __init__(self):
        super(Login, self).__init__()
        print("x")
        uic.loadUi("gui/interfaces/Login.ui", self)
        self.i_login.clicked.connect(self.login)
        self.i_password_note.setHidden(True)
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_forget_pass.mousePressEvent = self.forget_password
        self.i_header.mouseMoveEvent = self.move_window
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.show()

    # Move window around
    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    # Opens forget password window
    def forget_password(self, eve):
        try:
            ForgetPassword.ForgetPassword()
        except Exception as e:
            print(e)

    # Allows window to be clickable
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def login(self):
        self.i_password_note.setHidden(True)
        username = self.i_username.text()
        password = self.i_password.text()
        if username == "" or password == "":
            self.i_password_note.setHidden(False)
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
                    from gui.AdminDashboard import AdminDashboard
                    AdminDashboard()

                else:
                    self.destroy()
                    from gui.InstructorDashboard import InstructorDashboard
                    InstructorDashboard()
            except requests.exceptions.HTTPError as e:
                print(e)
                # print(json.loads(e.args[1])["error"]["message"])
                self.i_password_note.setHidden(False)
            except Exception as e:
                print(e)
                print("Something went wrong! Could not login.")
