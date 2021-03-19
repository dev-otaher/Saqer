import time
from math import ceil
from multiprocessing.process import current_process
import cv2
import face_recognition as fr
import itertools as it
import numpy
from modules.FileVideoStream import FileVideoStream

class Movie(FileVideoStream):
    def __init__(self, qsize=128):
        super().__init__(queue_size=qsize)
        # self.stream = self.get_stream(path)

    # def get_frame_id(self, second):
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

    def get_frame_by_id(self, frameId):
        self.stream.set(1, frameId)
        frame = self.stream.read()
        self.stream.set(1, 0)
        return frame

    # def get_frames_by_id(self, ids):
    #     print("get_frames_by_id")
    #     for frameId in ids:
    #         if not self.Q.full():
    #             (grabbed, frame) = self.get_frame_by_id(frameId)
    #             self.Q.put(frame)
    #         else:
    #             time.sleep(0.1)

