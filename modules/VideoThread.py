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


class VideoThread(QThread):
    # this class will handle the detection and recognition part using worker thread
    image_update = pyqtSignal(QImage)
    std_list = pyqtSignal(object)
    # determine the state of the save record checkbox
    def __init__(self, stream_path, proto_path, model_path, embedder_path, recognizer_path, le_path, confidence=0.7):
        super(VideoThread, self).__init__()
        self.threadActive = True
        self.isRecordChecked = None
        self.class_id = None
        self.stream_path = stream_path
        self.proto_path, self.model_path, self.embedder_path = proto_path, model_path, embedder_path
        self.detector = cv2.dnn.readNetFromCaffe(self.proto_path, self.model_path)
        self.embedder = cv2.dnn.readNetFromTorch(self.embedder_path)
        self.recognizer = pickle.loads(open(recognizer_path, 'rb').read())
        self.label_encoder = pickle.loads(open(le_path, 'rb').read())
        self.confidence = confidence

    def get_locations(self, frame):
        (h, w) = frame.shape[:2]
        f_blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (w, h),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)
        self.detector.setInput(f_blob)
        detections = self.detector.forward()
        locations = []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence:
                # compute the (x, y)-coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                locations.append(box.astype('int'))
        return locations

    def get_face(self, frame, location):
        (startX, startY, endX, endY) = location
        # extract face ROI
        face = frame[startY:endY, startX:endX]
        (fH, fW) = face.shape[:2]
        # ensure the face width and height are sufficiently large
        if not (fW < 20 or fH < 20):
            return face
        return None

    def encode(self, face):
        faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                         (96, 96), (0, 0, 0), swapRB=True, crop=False)
        self.embedder.setInput(faceBlob)
        vec = self.embedder.forward()
        return vec

    def recognize(self, encoding):
        # perform classification to recognize the face
        preds = self.recognizer.predict_proba(encoding)[0]
        j = np.argmax(preds)
        p = preds[j]
        if p > 0.65:
            id = self.label_encoder.classes_[j]
        else:
            id = "Unknown"
        return id, p

    def run(self):
        fileName = str(datetime.datetime.now().strftime('%I%p-%M-%S--%d_%m_%Y'))
        try:
            taker = AttendanceTaker(self.class_id).populate_std_list()
            if self.stream_path == 0:
                cap = cv2.VideoCapture(self.stream_path, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(self.stream_path)
            time.sleep(2.0)
            text = ""
            first_loop = self.threadActive = True
            while self.threadActive:
                ret, frame = cap.read()
                frame = imutils.resize(frame, width=1080)
                if ret:
                    if self.isRecordChecked and first_loop:
                        writer = cv2.VideoWriter(os.path.sep.join(['db', fileName+'.avi']), cv2.VideoWriter_fourcc(*'XVID'), 10, (frame.shape[1], frame.shape[0]), True)
                        first_loop = False
                    if self.isRecordChecked:
                        # save the frame
                        writer.write(frame)
                    locations = self.get_locations(frame)
                    # loop over the detections
                    for loc in locations:
                        face = self.get_face(frame, loc)
                        if face is not None:
                            encoding = self.encode(face)
                            id, p = self.recognize(encoding)
                            if id is not None and id != "Unknown":
                                std = taker.get_std_by_id(str(id))
                                if std is not None:
                                    taker.increment(std)
                                    text = '{}: {:.2f}%'.format(std.name, p * 100)
                                else:
                                    text = '{}: {:.2f}%'.format("NIL", p * 100)
                            else:
                                text = '{}: {:.2f}%'.format(id, p * 100)
                        (startX, startY, endX, endY) = loc
                        # draw the bounding box of the face along with the
                        # associated probability
                        # text = '{:.2f}%'.format(confidence * 100)
                        y = startY - 10 if startY - 10 > 10 else startY + 10
                        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                        cv2.putText(frame, text, (startX, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
                # Convert cv to qt
                frame = cv2.flip(frame, 1)
                # convert the frame into RGB format
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # flip the image
                flippedImage = cv2.flip(Image, 1)
                # convert the frame into a Qt format and keep the aspect ratio
                convertToQtFormat = QImage(flippedImage.data, flippedImage.shape[1], flippedImage.shape[0], QImage.Format_RGB888)
                pic = convertToQtFormat.scaled(864, 486, Qt.KeepAspectRatio)
                self.image_update.emit(pic)
                taker.increment_checkpoint()
            cap.release()
            self.std_list.emit(taker)
        except Error as e:
            print("sqlite", e)
        except Exception as e:
            print(e)
