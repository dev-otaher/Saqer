import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog

count = 0
dots = ""


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi("LoginPage.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.password_note.setHidden(True)
        self.closewindow.clicked.connect(lambda: self.close())
        self.minmizewindow.clicked.connect(lambda: self.showMinimized())


class Loding(QtWidgets.QMainWindow):
    def __init__(self):
        super(Loading, self).__init__()
        uic.loadUi("Loding.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.progress)
        self.timer.start(150)
        self.show()

    def progress(self):
        global count
        global dots
        self.progressBar.setValue(count)
        if count > 100:
            self.timer.stop()
            self.main = Login()
            self.main.show()
            self.close()
        count += 1
        dots += "."
        if dots == "....":
            dots = ""
        self.Loading.setText("Loading" + dots)


app = QtWidgets.QApplication(sys.argv)
window = Loding()
app.exec_()
