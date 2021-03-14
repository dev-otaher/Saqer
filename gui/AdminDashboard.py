import multiprocessing
from functools import partial
from multiprocessing import cpu_count
from threading import Thread

import cv2
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
from imutils.video import FPS

from gui import Login
from modules.Recognizer import Recognizer


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
        self.i_choose_video.clicked.connect(self.choose_video)
        self.i_start.clicked.connect(self.start_offline_attendance)
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

    def choose_video(self):
        video_path = QFileDialog.getOpenFileName(self, 'Choose Video...', '', 'Video (*.mp4 , *.mkv , *.MOV)')
        self.i_video_path.setText(video_path[0])

    def start_offline_attendance(self):
        try:
            self.i_video_note.setHidden(True)
            path = self.i_video_path.text()
            if path == "":
                self.i_video_note.setHidden(False)
            else:
                self.i_progress_label.setHidden(False)
                self.i_progress_bar.setHidden(False)

                movie = cv2.VideoCapture(path)
                fps, interval, total_frames = movie.get(5), 0.10, movie.get(7)
                CPUs, duration = cpu_count()-2, total_frames / fps
                chunk_size = duration / CPUs

                timer = FPS()
                timer.start()
                processes = []
                for i in range(CPUs):
                    r = Recognizer(path,
                                   64,
                                   "db/model/deploy.prototxt",
                                   "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                                   "db/model/openface_nn4.small2.v1.t7",
                                   "db/model/recognizer_12.03.2021_14.56.27.pickle",
                                   "db/model/labels_12.03.2021_14.56.27.pickle")
                    t = Thread(target=r.pick_frames, args=(interval, i * chunk_size, (i + 1) * chunk_size))
                    t.start()
                    p = multiprocessing.Process(target=r.xyz)
                    p.start()
                    processes.append(p)

                for process in processes:
                    process.join()
                timer.stop()
                Warning(timer.elapsed())
        except Exception as e:
            print(e)
            Warning(str(e))

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
