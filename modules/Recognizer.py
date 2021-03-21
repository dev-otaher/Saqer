import pickle
from multiprocessing import Pipe
from multiprocessing.process import current_process
import cv2
import imutils
import numpy as np

from modules.AttendanceTaker import AttendanceTaker
from modules.FileVideoStream import FileVideoStream


class Recognizer:
    def __init__(self, path, qsize, proto_path, model_path, embedder_path, recognizer_path, le_path, to_emitter: Pipe,
                 confidence=0.6):
        self.vs = FileVideoStream(path, qsize)
        self.proto_path = proto_path
        self.model_path = model_path
        self.embedder_path = embedder_path
        self.recognizer = pickle.loads(open(recognizer_path, 'rb').read())
        self.label_encoder = pickle.loads(open(le_path, 'rb').read())
        self.confidence = confidence
        self.to_emitter = to_emitter


    def get_locations(self, frame):
        f_copy = frame.copy()
        (h, w) = f_copy.shape[:2]

        f_blob = cv2.dnn.blobFromImage(
            cv2.resize(f_copy, (300, 300)), 1.0, (w, h),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        detector = cv2.dnn.readNetFromCaffe(self.proto_path, self.model_path)
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
        embedder = cv2.dnn.readNetFromTorch(self.embedder_path)
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
        return name, p

    def run(self):
        taker = AttendanceTaker().populate_std_list()
        while self.vs.more():
            frame = imutils.resize(self.vs.read(), width=1080)
            locations = self.get_locations(frame)
            for loc in locations:
                face = self.get_face(frame, loc)
                if face is not None:
                    encoding = self.encode(face)
                    name, p = self.recognize(encoding)
                    std_id = taker.get_id_by_name(name)
                    if std_id is not None:
                        taker.increment(taker.get_std_by_id(std_id))
                    text = '{}: {:.2f}%'.format(name, p * 100)
                    (startX, startY, endX, endY) = loc
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)
            self.vs.save_frame(frame, "db/frames/")
            self.to_emitter[1].send(1)
        print(current_process().name, "sending list...")
        self.to_emitter[1].send(taker.students)
