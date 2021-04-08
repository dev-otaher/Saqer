import multiprocessing
from os import cpu_count
from threading import Thread
from PyQt5.QtCore import pyqtSignal, QThread
from modules.FileVideoStreamInfo import FileVideoStreamInfo
from modules.Recognizer import Recognizer


class AttendanceThread(QThread):
    max_signal = pyqtSignal(int)

    def __init__(self, child_pipe: multiprocessing.Pipe, path=""):
        super(AttendanceThread, self).__init__(parent=None)
        self.path = path
        self.child_pipe = child_pipe

    def run(self):
        try:
            vs_info = FileVideoStreamInfo(self.path)
            fps, total_frames, duration = vs_info.get_fps(), vs_info.get_total_frames(), vs_info.get_duration(True)
            CPUs, interval = cpu_count() - 2, 0.5
            chunk_size = duration / CPUs
            qsize = 128 // CPUs
            total_picked_frames = duration / interval
            self.max_signal.emit(int(total_picked_frames))

            for i in range(CPUs):
                r = Recognizer(self.path,
                               qsize,
                               "db/model/deploy.prototxt",
                               "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                               "db/model/openface_nn4.small2.v1.t7",
                               "db/courses/CS 422/L6M3/dataset/output/recognizer.pickle",
                               "db/courses/CS 422/L6M3/dataset/output/labels.pickle",
                               to_emitter=self.child_pipe)
                Thread(target=r.vs.pick_frames, args=(interval, i * chunk_size, (i + 1) * chunk_size)).start()
                multiprocessing.Process(target=r.run).start()
        except Exception as e:
            print(e)
            Warning(str(e))
