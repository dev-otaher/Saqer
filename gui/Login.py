import json
import sys
from os.path import sep

import pyrebase
from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from cv2 import error

from gui.ForgetPassword import ForgetPassword
from gui.Warning import Warning


class Login(QDialog):

    # constructor of the class
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi(sep.join(['gui', 'interfaces', 'Login.ui']), self)
        self.i_login.clicked.connect(self.login)
        self.i_password_note.setHidden(True)
        self.i_close.clicked.connect(lambda: sys.exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_forget_pass.clicked.connect(self.forget_password)
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
            ForgetPassword()
        except Exception as e:
            Warning(str(e))
            print(e)

    # Allows window to be clickable
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def login(self):
        self.i_password_note.setHidden(True)
        username = self.i_username.text().strip()
        password = self.i_password.text().strip()
        if username == "" or password == "":
            self.i_password_note.setHidden(False)
        else:
            try:
                with open(sep.join(['db', 'fbConfig.json'])) as file:
                    config = json.load(file)
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                db = firebase.database()
                user = auth.sign_in_with_email_and_password(username, password)
                UUID = str(user["localId"])
                isAdmin = db.child("users").child(UUID).child("isAdmin").get().val()
                if isAdmin == "True":
                    from gui.admin.AdminDashboard import AdminDashboard
                    mainwindow = AdminDashboard()
                    self.destroy()
                elif isAdmin == "False":
                    from gui.instructor.InstructorDashboard import InstructorDashboard
                    mainwindow = InstructorDashboard(UUID)
                    self.destroy()
                else:
                    self.i_password_note.setHidden(False)
            except pyrebase.pyrebase.HTTPError:
                self.i_password_note.setHidden(False)
            except error as e :
                Warning(str(e.err))
            except Exception as e:
                Warning("Something went wrong! Could not login.")
                print(e)
