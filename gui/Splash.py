import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer


from gui.Login import Login

count = 0
dots = ""


class Loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(Loading, self).__init__()
        uic.loadUi("Interfaces files/Loading.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.progress)
        self.timer.start(25)
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
        self.Loding_Label.setText("Loading" + dots)


app = QtWidgets.QApplication(sys.argv)
window = Loading()
app.exec_()
