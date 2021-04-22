import datetime
from os.path import sep
from sqlite3 import Error

import cv2
import imutils
import numpy
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage

from gui.Warning import Warning


class RegisterThread(QThread):
    # this class will handle the detection and recognition part using worker thread
    no_cam = pyqtSignal(str)
    image_update = pyqtSignal(QImage)
    def __init__(self, stream_path):
        super().__init__()
        self.stream_path = stream_path
        self.save = False
        self.uni_id = None

    def run(self):
        try:
            if self.stream_path is int:
                cap = cv2.VideoCapture(self.stream_path, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(self.stream_path)
            self.threadActive = True
            ret, first_frame = cap.read()
            if not ret:
                self.no_cam.emit("Failed to open camera or no camera found!")
                return
            while self.threadActive:
                ret, frame = cap.read()
                if ret:
                    frame = imutils.resize(frame, width=1080)
                    if self.save:
                        filename = str(datetime.datetime.now()).replace(":", ".")
                        cv2.imwrite(sep.join(['db', 'dataset', self.uni_id, f"{filename}.jpg"]), frame)
                        self.save = False
                    # convert the frame into RGB format
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # convert the frame into a Qt format and keep the aspect ratio
                    convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                    pic = convertToQtFormat.scaled(864, 486, Qt.KeepAspectRatio)
                    self.image_update.emit(pic)
                else:
                    self.no_cam.emit("Failed to open camera or no camera found!")
                    break
            black_frame = numpy.zeros((1920, 1080, 3), dtype=numpy.uint8)
            self.image_update.emit(QImage(black_frame, black_frame.shape[1], black_frame.shape[0], QImage.Format_RGB888))
            cap.release()
        except Error as e:
            Warning(str(e))
            print("sqlite", e)
        except Exception as e:
            Warning(str(e))
            print(e)
