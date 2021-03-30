from datetime import datetime
import os
import pickle
import cv2
import imutils
import numpy as np
from PyQt5.QtCore import pyqtSignal, QThread
from imutils import paths


class Encoder(QThread):
    update_available = pyqtSignal(int)
    def __init__(self, protoPath, modelPath, embedderPath, confidence=0.6, filename="encodings.pickle"):
        super().__init__()
        self._detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        self._embedder = cv2.dnn.readNetFromTorch(embedderPath)
        self.confidence = confidence
        self.file = filename
        self.dataset_path = str()

    def get_location(self, frame):
        f_copy = frame.copy()
        (h, w) = f_copy.shape[:2]

        # construct a blob from the image
        f_blob = cv2.dnn.blobFromImage(cv2.resize(f_copy, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0),
                                       swapRB=False, crop=False)

        self._detector.setInput(f_blob)
        detections = self._detector.forward()

        if len(detections) > 0:
            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidence:
                # compute the (x, y)-coordinates of the bounding box for the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                location = box.astype('int')
                return location

    def get_face(self, frame, location):
        (startX, startY, endX, endY) = location
        # extract face ROI
        face = frame[startY:endY, startX:endX]
        (fH, fW) = face.shape[:2]
        # ensure the face width and height are sufficiently large
        if not (fW < 20 or fH < 20):
            return face

    def encode(self, face):
        try:
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                             (96, 96), (0, 0, 0), swapRB=True, crop=False)
            self._embedder.setInput(faceBlob)
            vec = self._embedder.forward()
            return vec.flatten()
        except cv2.error:
            pass

    def save_encodings(self, data):
        try:
            f = open(f"{self.file}/encodings_{self.get_current_datetime()}.pickle", "wb")
            f.write(pickle.dumps(data))
            f.close()
        except Exception as e:
            print(e)

    def get_current_datetime(self):
        return datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

    def run(self):
        names = []
        embeddings = []
        for i, path in enumerate(self.dataset_path):
            frame = imutils.resize(cv2.imread(path), width=800)
            location = self.get_location(frame)
            if location is not None:
                face = self.get_face(frame, location)
                embedding = self.encode(face)
                if embedding is not None:
                    names.append(path.split(os.path.sep)[-2])
                    embeddings.append(embedding)
            self.update_available.emit(1)
        self.save_encodings({"names": names, "embeddings": embeddings})


# if __name__ == '__main__':
#     encoder = Encoder(protoPath="../model/deploy.prototxt",
#                       modelPath="../model/res10_300x300_ssd_iter_140000.caffemodel",
#                       embedderPath="../model/openface_nn4.small2.v1.t7",
#                       filename="output")
#
#     images_path = list(paths.list_images("../dataset"))
#     encoder.start(images_path)
