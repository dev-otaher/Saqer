from functools import partial
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from gui import Login
from gui.admin.OfflineAttendance import OfflineAttendance


class AdminDashboard(QDialog):
    def __init__(self):
        super(AdminDashboard, self).__init__()
        uic.loadUi("gui/interfaces/AdminDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.connect_widgets()
        self.offline_attendance = OfflineAttendance(parent_gui=self)
        self.show()

    def connect_widgets(self):
        self.connect_header()
        self.connect_side_widgets()

    def connect_header(self):
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.clicked.connect(self.logout)

    def connect_side_widgets(self):
        self.i_register_student.clicked.connect(partial(self.goto, self.i_register_sec))
        self.i_train_model.clicked.connect(partial(self.goto, self.i_train_sec))
        self.i_offline_atten.clicked.connect(partial(self.goto, self.i_offline_sec))
        self.i_settings.clicked.connect(partial(self.goto, self.i_settings_sec))

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, e):
        self.clickPosition = e.globalPos()

    def goto(self, widget):
        self.i_choices.setCurrentWidget(widget)

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
