import datetime
from math import ceil
import cv2


class FileVideoStreamInfo:
    def __init__(self, path: str):
        self.stream = cv2.VideoCapture(path)
        self.path = path
        self._scounter = 0

    def get_fps(self):
        return self.stream.get(5)

    def get_total_frames(self):
        return self.stream.get(7)

    def get_duration(self, in_seconds=False):
        total_frames = self.get_total_frames()
        fps = self.get_fps()
        duration = total_frames / fps
        if in_seconds:
            return duration
        return datetime.timedelta(seconds=duration)
