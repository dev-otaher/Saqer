from functools import partial

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt, QVariant
import sqlite3
from PyQt5.QtGui import QCursor, QColor
import sys
from gui import Login, Warning
from PyQt5.QtCore import Qt, QTimer


# each interface defined in a class
class AdminDashboard(QDialog):
    def __init__(self):
        super(AdminDashboard, self).__init__()
        uic.loadUi("gui/interfaces/AdminDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_header.mouseMoveEvent = self.move_window

        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.mousePressEvent = self.logout

        self.i_register_student.clicked.connect(partial(self.goto, self.i_register_sec))
        self.i_train_model.clicked.connect(partial(self.goto, self.i_train_sec))
        self.i_offline_atten.clicked.connect(partial(self.goto, self.i_offline_sec))
        self.i_settings.clicked.connect(partial(self.goto, self.i_settings_sec))

        self.i_video_note.setHidden(True)
        self.i_progress_label.setHidden(True)
        self.i_progress_bar.setHidden(True)

        self.show()

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, e):
        self.clickPosition = e.globalPos()

    def goto(self, widget):
        self.i_choices.setCurrentWidget(widget)
        if widget is self.i_offline_sec:
            self.i_choose_video.clicked.connect(self.choose_video)
            self.i_start.clicked.connect(self.start_offline_attendance)

    def choose_video(self):
        video_path = QFileDialog.getOpenFileName(self, 'Choose Video...', '', 'Video (*.mp4 , *.mkv , *.MOV)')
        self.i_video_path.setText(video_path[0])

    def start_offline_attendance(self):
        self.i_video_note.setHidden(True)
        if self.i_video_path.text() == "":
            self.i_video_note.setHidden(False)
        else:
            self.i_progress_label.setHidden(False)
            self.i_progress_bar.setHidden(False)
            pass

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
