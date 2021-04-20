import time
from math import floor
from os.path import sep
from sqlite3 import Error

import cv2
import imutils
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from gui.Warning import Warning
from modules.AttendanceTaker import AttendanceTaker


class VideoThread(QThread):
    # this class will handle the detection and recognition part using worker thread
    no_cam = pyqtSignal(str)
    image_update = pyqtSignal(QImage)
    std_list = pyqtSignal(object)
    def __init__(self, stream_path, proto_path, model_path, embedder_path, emotioner_path, confidence=0.8):
        super(VideoThread, self).__init__()
        self.threadActive = True
        self.isRecord = None
        self.folder_path = None
        self.filename = None
        self.class_id = None
        self.stream_path = stream_path
        self.proto_path, self.model_path, self.embedder_path = proto_path, model_path, embedder_path
        self.detector = None
        self.embedder = None
        self.emotioner_path = emotioner_path
        self.emotioner = None
        self.emotions = [['Angry', 0], ['Scared',0], ['Happy', 0], ['Sad', 0], ['Surprised', 0], ['Neutral', 0]]
        self.recognizer = None
        self.label_encoder = None
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

    def process_emotion(self, face):
        try:
            roi = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            if roi is None:
                print('roi is None')
                return
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype('float') / 255.0
            roi = img_to_array(roi)  # convert to keras-compatible array
            roi = np.expand_dims(roi, axis=0)
            preds = self.emotioner.predict(roi)[0]
            self.emotions[preds.argmax()][1] += 1
        except Exception as e:
            Warning(str(e))
            print(e)

    def convert_to_percetage(self, faces):
        for e in self.emotions:
            e[1] = floor(e[1]/faces*100)

    def run(self):
        try:
            self.detector = cv2.dnn.readNetFromCaffe(self.proto_path, self.model_path)
            self.embedder = cv2.dnn.readNetFromTorch(self.embedder_path)
            self.emotioner = load_model(self.emotioner_path)
            taker = AttendanceTaker(self.class_id).populate_std_list()
            if self.stream_path is int:
                cap = cv2.VideoCapture(self.stream_path, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(self.stream_path)
            time.sleep(1.0)
            text = ""
            first_loop = self.threadActive = found_cam = True
            while self.threadActive:
                ret, frame = cap.read()
                if (not ret) and first_loop:
                    self.no_cam.emit("Failed to open camera or no camera found!")
                    found_cam = False
                    break
                if ret:
                    frame = imutils.resize(frame, width=1080)
                    if self.isRecord and first_loop:
                        writer = cv2.VideoWriter(sep.join([self.folder_path, self.filename+'.avi']), cv2.VideoWriter_fourcc(*'XVID'), 10, (frame.shape[1], frame.shape[0]), True)
                    if self.isRecord:
                        writer.write(frame)
                    locations = self.get_locations(frame)
                    # loop over the detections
                    for loc in locations:
                        face = self.get_face(frame, loc)
                        if face is not None:
                            self.process_emotion(face)
                            encoding = self.encode(face)
                            id, p = self.recognize(encoding)
                            if id is not None and id != "Unknown":
                                std = taker.get_std_by_id(str(id))
                                if std is not None:
                                    taker.increment(std)
                                    text = '{} | {:.2f}%'.format(std.name, p * 100)
                                else:
                                    text = '{} | {:.2f}%'.format("NIL", p * 100)
                            else:
                                text = '{} | {:.2f}%'.format(id, p * 100)
                            taker.increment_faces()
                        (startX, startY, endX, endY) = loc
                        # draw the bounding box of the face along with the
                        # associated probability
                        y = startY - 10 if startY - 10 > 10 else startY + 10
                        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                        cv2.putText(frame, text, (startX, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
                    # convert the frame into RGB format
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # convert the frame into a Qt format and keep the aspect ratio
                    convertToQtFormat = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    pic = convertToQtFormat.scaled(864, 486, Qt.KeepAspectRatio)
                    self.image_update.emit(pic)
                    taker.increment_checkpoint()
                else:
                    break
                first_loop = False
            cap.release()
            if found_cam:
                self.std_list.emit(taker)
                self.convert_to_percetage(taker.faces)
        except Error as e:
            Warning(str(e))
            print(e)
        except Exception as e:
            Warning(str(e))
            print(e)
