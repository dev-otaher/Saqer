# import the necessary packages
from math import ceil
from multiprocessing.process import current_process
import cv2
import time
from multiprocessing import Queue
from numpy import ndarray


class FileVideoStream:
    def __init__(self, path: str, queue_size=128, transform=None):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.path = path
        self._scounter = 0
        self.stopped = False
        self.transform = transform

        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queue_size)

    def get_stream(self):
        return cv2.VideoCapture(self.path)

    def get_frame_by_id(self, stream, frame_id):
        stream.set(1, frame_id)
        ret, frame = stream.read()
        stream.set(1, 0)
        return ret, frame

    def pick_frames(self, interval=30, start=0, end=-1):
        stream = self.get_stream()
        fps = stream.get(5)
        while True:
            if self.stopped:
                break
            if not self.Q.full():
                frame_id = ceil(start * fps)
                ret, frame = self.get_frame_by_id(stream, frame_id)
                if (ret is False) or (end != -1 and start > end):
                    self.stop()
                    break
                self.Q.put(frame)
                start += interval
            else:
                time.sleep(0.1)
        stream.release()

    def save_frame(self, image: ndarray, path: str):
        if (path[-1] == '/') or (path == '\\'):
            path = path[0:-1]
        cv2.imwrite(f"{path}/{current_process().name}_{str(self._scounter).zfill(6)}.jpg", image)
        self._scounter += 1

    def save_frames(self, save_path: str, rotate=None):
        while self.more():
            img = self.read()
            if rotate is not None and rotate == cv2.ROTATE_90_COUNTERCLOCKWISE | cv2.ROTATE_90_CLOCKWISE | cv2.ROTATE_180:
                img = cv2.rotate(img, rotate)
            self.save_frame(img, save_path)

    def read(self):
        # return next frame in the queue
        return self.Q.get()

    # Insufficient to have consumer use while(more()) which does
    # not take into account if the producer has reached end of
    # file stream.
    def running(self):
        return self.more() or not self.stopped

    def more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.Q.qsize() == 0 and not self.stopped and tries < 5:
            time.sleep(0.1)
            tries += 1
        return self.Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
