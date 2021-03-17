import pickle
import time
from multiprocessing import Process, Queue, Pipe
from threading import Thread

import cv2
import face_recognition
import imutils
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from imutils import paths
from imutils.video import VideoStream
from modules.frames_queue import Movie
from PyQt5 import QtCore


class Recognizer(Movie):
    def __init__(self, path, qsize, protoPath, modelPath, embedderPath, recognizerPath, lePath, to_emitter: Pipe, confidence=0.6):
        Movie.__init__(self, path, qsize=qsize)
        self.protoPath, self.modelPath = protoPath, modelPath
        self.embedderPath = embedderPath
        self.recognizer = pickle.loads(open(recognizerPath, 'rb').read())
        self.label_encoder = pickle.loads(open(lePath, 'rb').read())
        self.to_emitter = to_emitter
        self.confidence = confidence

    def get_locations(self, frame):
        f_copy = frame.copy()
        (h, w) = f_copy.shape[:2]

        f_blob = cv2.dnn.blobFromImage(
            cv2.resize(f_copy, (300, 300)), 1.0, (w, h),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        detector = cv2.dnn.readNetFromCaffe(self.protoPath, self.modelPath)
        detector.setInput(f_blob)
        detections = detector.forward()

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
        embedder = cv2.dnn.readNetFromTorch(self.embedderPath)
        embedder.setInput(faceBlob)
        vec = embedder.forward()
        return vec

    def draw_box_over_faces(self, frame, locations):
        f = frame.copy()
        for loc in locations:
            pt1, pt2 = (loc[0], loc[1]), (loc[2], loc[3])
            cv2.rectangle(f, pt1, pt2, (0, 255, 0), 2)
        return f

    def recognize(self, encoding):
        # perform classification to recognize the face
        preds = self.recognizer.predict_proba(encoding)[0]
        j = np.argmax(preds)
        p = preds[j]
        if p > 0.65:
            name = self.label_encoder.classes_[j]
        else:
            name = self.label_encoder.classes_[j]
        return (name, p)

    def xyz(self):
        while self.more():
            frame = imutils.resize(self.read(), width=1080)
            locations = self.get_locations(frame)
            # cv2.imshow("frame", recognizer.draw_box_over_faces(frame, locations))
            for loc in locations:
                face = self.get_face(frame, loc)
                if face is not None:
                    encoding = self.encode(face)
                    name, p = self.recognize(encoding)
                    text = '{}: {:.2f}%'.format(name, p * 100)
                    (startX, startY, endX, endY) = loc
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
            self.save_img(frame, "db/frames/")
            self.to_emitter[1].send(1)
            # self.emit(QtCore.PYQT_SIGNAL("done"), 1)
            # cv2.imshow('Frame', frame)
            # key = cv2.waitKey(1) & 0xFF
            # # if the 'q' key was pressed, break from the loop
            # if key == ord('q'):
            #     break


# if __name__ == '__main__':
#     recognizer = Recognizer("../model/deploy.prototxt",
#                             "../model/res10_300x300_ssd_iter_140000.caffemodel",
#                             "../model/openface_nn4.small2.v1.t7",
#                             "output/recognizer_12.03.2021_14.56.27.pickle",
#                             "output/labels_12.03.2021_14.56.27.pickle",
#                             0.8)
#     path = "../class_videos/1k - 2.MOV"
#     movie = cv2.VideoCapture(path)
#     fps = movie.get(5)
#     # interval = 1 / fps
#     interval = 0.1
#
#     vs = Movie(path)
#     t = Thread(target=vs.pick_frames, args=(interval,))
#     t.start()
#     time.sleep(2.0)
#
#     while vs.more():
#         frame = imutils.resize(vs.read(), width=1080)
#         locations = recognizer.get_locations(frame)
#         # cv2.imshow("frame", recognizer.draw_box_over_faces(frame, locations))
#         for loc in locations:
#             face = recognizer.get_face(frame, loc)
#             if face is not None:
#                 encoding = recognizer.encode(face)
#                 name, p = recognizer.recognize(encoding)
#                 text = '{}: {:.2f}%'.format(name, p * 100)
#                 (startX, startY, endX, endY) = loc
#                 y = startY - 10 if startY - 10 > 10 else startY + 10
#                 cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
#                 cv2.putText(frame, text, (startX, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
#         cv2.imshow('Frame', frame)
#         key = cv2.waitKey(1) & 0xFF
#         # if the 'q' key was pressed, break from the loop
#         if key == ord('q'):
#             break
            # t.join(0.1)
            # break

        # cv2.imshow("frame", encoder.encode(frame))
        # cv2.waitKey(0)
