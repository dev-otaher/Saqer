from PyQt5.QtWidgets import QDialog
from PyQt5 import uic,QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt, QVariant
import sqlite3
from PyQt5.QtGui import QCursor, QColor
import sys
from gui import Login, Warning
from PyQt5.QtCore import Qt, QTimer



#each interface defined in a class
class AdminDashboard(QDialog):
    #cnstructor of the class
    def __init__(self):
        super(AdminDashboard, self).__init__()
        uic.loadUi("gui/interfaces/AdminDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_register_student.clicked.connect(self.register_student)
        self.i_train_model.clicked.connect(self.train_model)
        self.i_offline_atten.clicked.connect(self.offline_attendance)
        self.i_settings.clicked.connect(self.settings)
        self.i_video_note.setHidden(True)
        self.i_folder_note.setHidden(True)
        self.i_pickle_note.setHidden(True)
        self.i_offline_prolabel.setHidden(True)
        self.i_offline_progress.setHidden(True)
        self.i_train_prolabel.setHidden(True)
        self.i_train_progress.setHidden(True)
        self.i_choose_video.clicked.connect(self.choose_video)
        self.i_choose_folder.clicked.connect(self.choose_folder)
        self.i_choose_file.clicked.connect(self.choose_pickle)
        self.i_start.clicked.connect(self.start_offline_attendance)
        self.i_extract.clicked.connect(self.extract_encodings)
        self.i_train.clicked.connect(self.train_encodings)

        self.i_logout.mousePressEvent = self.logout
        self.show()


    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()


    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()


    def register_student(self):
        self.i_choices.setCurrentWidget(self.i_register_sec)


    def train_model(self):
        self.i_choices.setCurrentWidget(self.i_train_sec)


    def offline_attendance(self):
        self.i_choices.setCurrentWidget(self.i_offline_sec)


    def settings(self):
        self.i_choices.setCurrentWidget(self.i_settings_sec)


    def choose_video(self):
        video_path = QFileDialog.getOpenFileName(self,'Choose Video', '', 'Video (*.mp4 , *.mkv)')
        self.i_video_path.setText(video_path[0])


    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self,'Choose Folder')
        self.i_folder_path.setText(folder_path)


    def choose_pickle(self):
        pickle_path = QFileDialog.getOpenFileName(self,'Choose Pickle', '', 'Pickle (*.pickle)')
        self.i_pickle_path.setText(pickle_path[0])


    def start_offline_attendance(self):
        video_path = self.i_video_path.text()
        find_mp4 = video_path.find('.mp4')
        find_mkv = video_path.find('.mkv')

        if find_mp4 == -1 and find_mkv == -1 :
            self.i_video_note.setHidden(False)
        else:
            self.i_video_note.setHidden(True)
            self.i_offline_progress.setHidden(False)
            self.i_offline_label.setHidden(False)


    def extract_encodings(self):
        folder_path = self.i_folder_path.text()
        validating_folder = folder_path.find('')

        if self.i_folder_path.text() == '':
            self.i_folder_note.setHidden(False)
        else:
            self.i_folder_note.setHidden(True)


    def train_encodings(self):
        pickle_path = self.i_pickle_path.text()
        validating_pickle = pickle_path.find('.pickle')

        if validating_pickle == -1:
            self.i_pickle_note.setHidden(False)
        else:
            self.i_pickle_note.setHidden(True)
            self.i_train_prolabel.setHidden(False)
            self.i_train_progress.setHidden(False)

    def logout(self, eve):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
