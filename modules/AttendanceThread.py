import multiprocessing
from threading import Thread

import cv2
from PyQt5.QtCore import pyqtSignal, QThread
from imutils.video import FPS

from modules.Recognizer import Recognizer


class AttendanceThread(QThread):
    signal = pyqtSignal(int)
    def __init__(self, child_pipe: multiprocessing.Pipe, parent=None, path=""):
        super(AttendanceThread, self).__init__(parent)
        self.path = path
        self.child_pipe = child_pipe

    def run(self):
        try:
            print("Started...")
            movie = cv2.VideoCapture(self.path)
            fps, interval, total_frames = movie.get(5), 0.5, movie.get(7)
            # CPUs, duration = cpu_count()-2, total_frames / fps
            CPUs, duration = 4, total_frames / fps
            chunk_size = duration / CPUs

            print(total_frames)
            self.signal.emit(int(total_frames))

            timer = FPS()
            timer.start()
            processes = []
            for i in range(CPUs):
                r = Recognizer(self.path,
                               64,
                               "db/model/deploy.prototxt",
                               "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                               "db/model/openface_nn4.small2.v1.t7",
                               "db/model/recognizer_12.03.2021_14.56.27.pickle",
                               "db/model/labels_12.03.2021_14.56.27.pickle",
                               to_emitter = self.child_pipe)
                t = Thread(target=r.pick_frames, args=(interval, i * chunk_size, (i + 1) * chunk_size))
                t.start()
                p = multiprocessing.Process(target=r.xyz)
                p.start()
                processes.append(p)

            # for process in processes:
            #     process.join()

            timer.stop()
            Warning(timer.elapsed())
        except Exception as e:
            print(e)
            Warning(str(e))


# from multiprocessing import Pool
# def f(x):
#     return x*x
# 
# if __name__ == '__main__':
#     with Pool(5) as p:
#         print(p.map(f, [1, 2, 3]))
