from multiprocessing import Pipe
from functools import partial
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog

from gui import Login
from modules.AttendanceThread import AttendanceThread
from modules.Emitter import Emitter

class AdminDashboard(QDialog):
    def __init__(self):
        super(AdminDashboard, self).__init__()
        uic.loadUi("gui/interfaces/AdminDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_header.mouseMoveEvent = self.move_window

        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.mousePressEvent = self.logout

        self.initialize_header()

        self.i_choose_video.clicked.connect(self.choose_video)
        self.i_start.clicked.connect(self.start_offline_attendance)

        self.i_video_note.setHidden(True)
        self.i_progress_label.setHidden(True)
        self.i_progress_bar.setHidden(True)

        child_pipe = Pipe()

        self.attendance_thread = AttendanceThread(child_pipe)
        self.attendance_thread.signal.connect(self.set_bar_max)

        self.emitter = Emitter(child_pipe)
        self.emitter.update_available.connect(self.update_progress)

        self.show()

    def initialize_header(self):
        self.i_register_student.clicked.connect(partial(self.goto, self.i_register_sec))
        self.i_train_model.clicked.connect(partial(self.goto, self.i_train_sec))
        self.i_offline_atten.clicked.connect(partial(self.goto, self.i_offline_sec))
        self.i_settings.clicked.connect(partial(self.goto, self.i_settings_sec))

    def set_bar_max(self, val):
        self.i_progress_bar.setMaximum(val)

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, e):
        self.clickPosition = e.globalPos()

    def goto(self, widget):
        self.i_choices.setCurrentWidget(widget)

    def choose_video(self):
        video_path = QFileDialog.getOpenFileName(self, 'Choose Video...', '', 'Video (*.mp4 , *.mkv , *.MOV)')
        self.i_video_path.setText(video_path[0])

    def start_offline_attendance(self):
        try:
            self.i_video_note.setHidden(True)
            # path = self.i_video_path.text()
            path = "D:\Playground\Python\FaceAttendance - Parallelism\class_videos\\1k - 2.MOV"
            if path == "":
                self.i_video_note.setHidden(False)
            else:
                self.i_progress_label.setHidden(False)
                self.i_progress_bar.setHidden(False)
                self.i_progress_bar.setValue(0)
                self.emitter.start()
                self.attendance_thread.path = path
                self.attendance_thread.start()
        except Exception as e:
            print(e)

    def update_progress(self, val):
        try:
            self.i_progress_bar.setValue(self.i_progress_bar.value() + val)
        except Exception as e:
            print(e)

    def logout(self):
        try:
            print("logout")
            Login.Login()
            print("logout2")
            self.destroy()
            print("logout3")
        except Exception as e:
            print(e)



