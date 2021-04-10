import datetime
import multiprocessing
import os
import pickle
import time
from os import cpu_count
from sqlite3 import Error
from threading import Thread

import cv2
import imutils
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage
from imutils.video import FPS

from modules.AttendanceTaker import AttendanceTaker
from modules.AttendanceThread import AttendanceThread
from modules.FileVideoStreamInfo import FileVideoStreamInfo
from modules.Recognizer import Recognizer
from modules.VideoThread import VideoThread


class RegisterThread(VideoThread):
    # this class will handle the detection and recognition part using worker thread
    def __init__(self, stream_path):
        super().__init__(stream_path,
                         "db/model/deploy.prototxt",
                         "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                         "db/model/openface_nn4.small2.v1.t7")
        self.detector = self.embedder = None
        self.folder_path = None
        self.filename = None
        self.class_id = None

    def run(self):
        try:
            if self.stream_path is int:
                cap = cv2.VideoCapture(self.stream_path, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(self.stream_path)
            # time.sleep(1.0)
            self.threadActive = True
            first_frame = cap.read()[1]
            while self.threadActive:
                ret, frame = cap.read()
                frame = imutils.resize(frame, width=1080)
                if ret:
                    # convert the frame into RGB format
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # convert the frame into a Qt format and keep the aspect ratio
                    convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    pic = convertToQtFormat.scaled(864, 486, Qt.KeepAspectRatio)
                    self.image_update.emit(pic)
            self.image_update.emit(QImage(first_frame, first_frame.shape[1], first_frame.shape[0], QImage.Format_RGB888))
            cap.release()
        except Error as e:
            print("sqlite", e)
        except Exception as e:
            print(e)
