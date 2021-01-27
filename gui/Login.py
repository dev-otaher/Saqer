import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from Saqer.gui import ForgetPassword


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
        self.Fpassword.mousePressEvent = self.forgetpass
        self.Header.mouseMoveEvent = self.moveWindow
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.show()

        # Function for moving the window anywhere in the screen

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

        # It runs the forget password window

    def forgetpass(self, eve):
        ForgetPassword.ForgetPassword()

    #Used to move the screen
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def loginfunc(self):
        username = self.username.text()
        password = self.password.text()
        if username == "" and password == "":
            self.password_note.setHidden(False)



app=QApplication(sys.argv)
mainwindow=Login()
sys.exit(app.exec_())