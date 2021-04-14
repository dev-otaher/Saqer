import datetime
from sqlite3 import Error

import cv2
import imutils
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage

from gui.Warning import Warning
from modules.VideoThread import VideoThread


class RegisterThread(VideoThread):
    # this class will handle the detection and recognition part using worker thread
    def __init__(self, stream_path):
        super().__init__(stream_path,
                         "db/model/deploy.prototxt",
                         "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                         "db/model/openface_nn4.small2.v1.t7",
                         "db/model/epoch_75.hdf5")
        self.detector = self.embedder = self.emotioner = None
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
            if ret is False:
                self.no_cam.emit("Failed to open camera or no camera found!")
                return
            while self.threadActive:
                ret, frame = cap.read()
                if ret:
                    frame = imutils.resize(frame, width=1080)
                    if self.save:
                        filename = str(datetime.datetime.now()).replace(":", ".")
                        cv2.imwrite(f"db/dataset/{self.uni_id}/{filename}.jpg", frame)
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
            self.image_update.emit(QImage(first_frame, first_frame.shape[1], first_frame.shape[0], QImage.Format_RGB888))
            cap.release()
        except Error as e:
            Warning(str(e))
            print("sqlite", e)
        except Exception as e:
            Warning(str(e))
            print(e)
