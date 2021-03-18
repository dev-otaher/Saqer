import time
from math import ceil
from multiprocessing.process import current_process
import cv2
import face_recognition as fr
import itertools as it
import numpy
from modules.FileVideoStream import FileVideoStream

class Movie(FileVideoStream):
    def __init__(self, path: str, qsize=128):
        super().__init__(queue_size=qsize)
        # self.stream = self.get_stream(path)
        self.path = path
        self._scounter = 0

    # def start_picking(self, args=()):
    #     print("start_picking")
    #     self.pickThread = Thread(target=self.pick_frames, args=args)
    #     self.pickThread.start()
    #     return self

    def pick_frames(self, interval=30, start=0, end=-1):
        stream = cv2.VideoCapture(self.path)
        fps = stream.get(5)
        while True:
            if self.stopped:
                break
            if not self.Q.full():
                frameId = ceil(start * fps)
                stream.set(1, frameId)
                ret, frame = stream.read()
                stream.set(1, 0)
                if (ret is False) or (end != -1 and start > end):
                    self.stopped = True
                    break
                self.Q.put(frame)
                start += interval
            else:
                time.sleep(0.1)

    # def get_duration(self, in_seconds=False):
    #     print("get_duration")
    #     totalFrames = self.get_total_frames()
    #     fps = self.get_fps()
    #     duration = ceil(totalFrames / fps)
    #     if in_seconds:
    #         return duration
    #     return datetime.timedelta(seconds=duration)

    # def get_fps(self):
    #     print("get_fps")
    #     return self.fps

    # def get_total_frames(self):
    #     print("get_total_frames")
    #     return self.total_frames

    # def get_frame_id(self, second):
    #     print("get_frame_id")
    #     return ceil(second * self.fps)

    # def get_frames_id(self, interval, start=0, end=-1):
    #     print("get_frames_id")
    #     frameId = self.get_frame_id(start)
    #     ids = []
    #     if end == -1:
    #         end = int(self.get_duration(True))
    #     while start < end:
    #         ids.append(frameId)
    #         start += interval
    #         frameId = self.get_frame_id(start)
    #     return ids

    # def get_frame_by_id(self, frameId):
    #     self.stream.set(1, frameId)
    #     frame = self.stream.read()
    #     self.stream.set(1, 0)
    #     return frame

    # def get_frames_by_id(self, ids):
    #     print("get_frames_by_id")
    #     for frameId in ids:
    #         if not self.Q.full():
    #             (grabbed, frame) = self.get_frame_by_id(frameId)
    #             self.Q.put(frame)
    #         else:
    #             time.sleep(0.1)

    def video_to_frames(self, path: str):
        while self.more():
            # img = cv2.rotate(self.read(), cv2.ROTATE_90_COUNTERCLOCKWISE)
            img = self.read()
            cv2.imshow("f", img)
            cv2.waitKey(1) & 0xFF
            # if the 'q' key was pressed, break from the loop
            self.save_img(img, path)

    def save_img(self, image: numpy.ndarray, path: str):
        if (path[-1] == '/') or (path == '\\'):
            path = path[0:-1]
        cv2.imwrite(f"{path}/{current_process().name}_{str(self._scounter).zfill(6)}.jpg", image)
        self._scounter += 1

    def save_imgs(self, images, path: str):
        for img in images:
            self.save_img(img, path=path)

    ###############################################################################
    def detect_faces(self, img):
        gray_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
        locations = fr.face_locations(gray_img)
        return locations
        # if len(locations) > 0:
        #     for location in locations:
        #         pt1, pt2 = (location[3], location[0]), (location[1], location[2])
        #         cv2.rectangle(clrImg, pt1, pt2, border_color, thickness)
        #     return clrImg
        # elif len(locations) == 0 and return_all is True:
        #     return clrImg

    def draw_rec_on_faces(self, img, locations, border_color=(255, 255, 255), thickness=2):
        img_copy = img.copy()
        for location in locations:
            pt1, pt2 = (location[3], location[0]), (location[1], location[2])
            cv2.rectangle(img_copy, pt1, pt2, border_color, thickness)
        return img_copy

    def draw_matched_faces(self, image, face_locations, faces_comparison_result):
        img_copy = image.copy()
        for i, result in enumerate(faces_comparison_result):
            if result is numpy.True_:
                location = face_locations[i]
                cv2.rectangle(img_copy, (location[3], location[0]), (location[1], location[2]), (0, 255, 0), 2)
        return img_copy

    def grouper(self, iterable, n, fillvalue=None):
        iters = [iter(iterable)] * n
        yield it.zip_longest(*iters, fillvalue=fillvalue)

    def detect_and_save(self, images: list, path: str, border_color=(0, 0, 255), thickness=2):
        pass
        # imgs = detect_faces(images, border_color, thickness)
        # save_imgs(imgs, path)

    # def calculate_fps(self):

    def get_frames_by_interval(self, bar, interval=30):
        nextId = 0
        counter = 0

        time.sleep(1)

        while self.more():
            frame = self.read()
            if counter == nextId:
                self.save_img(frame, 'results/')
                nextId += int(interval * self.get_fps())
            # print(f"Saved frame #{counter}!")
            counter += 1
            bar.update(1)
            # print(f"Counter = {counter}, Next Id = {nextId}")

    def xyz(self):
        # import pickle
        # pkl_file = open('encodings/output/embeddings.pickle', 'rb')
        # mydict2 = pickle.load(pkl_file)
        # pkl_file.close()

        # known_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        # known_locations = fr.face_locations(known_img)
        # known_encodings = fr.face_encodings(known_img, known_locations)
        # known_encodings = mydict2["embeddings"]
        # print(known_encodings[0])
        while self.more():
            img = self.read()
            self.save_img(img, "results/mohanad/")
            # img = imutils.resize(self.read(), width=1080)
            # locations = self.detect_faces(img)
            # print(locations)
            # frame = self.draw_rec_on_faces(img, locations)
            # cv2.imshow("frame", frame)
            # key = cv2.waitKey(1) & 0xFF
            #
            # if the 'q' key was pressed, break from the loop
            # if key == ord('q'):
            #     break

            # if len(locations) > 0:
            #
            #     encoder = FaceEncoder()
            #     encoder.encode(frame)
                #
                #
                # unknown_encodings = fr.face_encodings(frame, locations, 1, "large")
                #
                #
                #
                #
                #
                #
                # matches = fr.compare_faces(unknown_encodings, known_encodings[0], 0.9)
                # self.save_img(self.draw_matched_faces(frame, locations, matches), "results/")






            # if len(locations) > 0:
            #     frame_with_faces = self.draw_rec_on_faces(frame, locations)
            #     self.save_img(frame_with_faces, 'results/')
            # bar.update(1)
    # cv2.VideoCapture(path)
