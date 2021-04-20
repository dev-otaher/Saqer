import multiprocessing
from os import cpu_count
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QThread

from gui.Warning import Warning
from modules.AttendanceTaker import AttendanceTaker
from modules.FileVideoStreamInfo import FileVideoStreamInfo
from modules.Recognizer import Recognizer
from modules.Students import Students


class AttendanceThread(QThread):
    max_signal = pyqtSignal(int)

    def __init__(self, child_pipe: multiprocessing.Pipe, path=""):
        super(AttendanceThread, self).__init__(parent=None)
        self.video_path = path
        self.child_pipe = child_pipe
        self.course_code = int()
        self.class_title = ""
        self.students = Students()

    def get_students(self, class_id):
        self.students = AttendanceTaker(class_id).populate_std_list().students

    def run(self):
        try:
            vs_info = FileVideoStreamInfo(self.video_path)
            fps, total_frames, duration = vs_info.get_fps(), vs_info.get_total_frames(), vs_info.get_duration(True)
            CPUs, interval = cpu_count() - 2, 0.5
            chunk_size = duration / CPUs
            qsize = 128 // CPUs
            total_picked_frames = duration / interval
            self.max_signal.emit(int(total_picked_frames))
            for i in range(CPUs):
                r = Recognizer(self.video_path,
                               qsize,
                               self.students,
                               "db/model/deploy.prototxt",
                               "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                               "db/model/openface_nn4.small2.v1.t7",
                               f"db/courses/{self.course_code}/{self.class_title}/dataset/output/recognizer.pickle",
                               f"db/courses/{self.course_code}/{self.class_title}/dataset/output/labels.pickle",
                               self.child_pipe)
                t = Thread(target=r.vs.pick_frames, args=(interval, i * chunk_size, (i + 1) * chunk_size))
                t.daemon = True
                t.start()
                p = multiprocessing.Process(target=r.run)
                p.daemon = True
                p.start()
        except Exception as e:
            Warning(str(e))
            print(e)
