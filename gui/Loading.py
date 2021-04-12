from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer

from gui.Login import Login


class Loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(Loading, self).__init__()
        uic.loadUi("gui/interfaces/Loading.ui", self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.progress)
        self.timer.start(25)
        self.count = 0
        self.dots = ""
        self.show()

    def progress(self):
        self.i_progress_bar.setValue(self.count)
        if self.count > 100:
            self.timer.stop()
            self.main = Login()
            self.main.show()
            self.close()
        self.count += 1
        self.dots += "."
        if self.dots == "....":
            self.dots = ""
        self.i_loading.setText("Loading" + self.dots)

