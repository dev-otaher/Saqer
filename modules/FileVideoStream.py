# import the necessary packages
import time
from math import ceil
from multiprocessing import Queue
from multiprocessing.process import current_process

import cv2
from numpy import ndarray


class FileVideoStream:
    def __init__(self, path=None, queue_size=128, transform=None):
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
        if self.path is not None:
            return cv2.VideoCapture(self.path)

    def update(self):
        stream = self.get_stream()
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                break

            # otherwise, ensure the queue has room in it
            if not self.Q.full():
                # read the next frame from the file
                (grabbed, frame) = stream.read()

                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self.stopped = True

                # if there are transforms to be done, might as well
                # do them on producer thread before handing back to
                # consumer thread. ie. Usually the producer is so far
                # ahead of consumer that we have time to spare.
                #
                # Python is not parallel but the transform operations
                # are usually OpenCV native so release the GIL.
                #
                # Really just trying to avoid spinning up additional
                # native threads and overheads of additional
                # producer/consumer queues since this one was generally
                # idle grabbing frames.
                if self.transform:
                    frame = self.transform(frame)

                # add the frame to the queue
                self.Q.put(frame)
            else:
                time.sleep(0.1)  # Rest for 10ms, we have a full queue

        stream.release()

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
