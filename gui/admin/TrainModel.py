from multiprocessing import Pipe
from sqlite3 import Error
from threading import Thread
from typing import List

from PyQt5.QtWidgets import QFileDialog
from imutils import paths
from qtpy import QtWidgets

from modules.AttendanceThread import AttendanceThread
from modules.DBHelper import DBHelper
from modules.Emitter import Emitter
from modules.Encoder import Encoder
from modules.Student import Student
from modules.Students import Students
from gui.Warning import Warning

class TrainModel:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.encoder = Encoder(protoPath="db/model/deploy.prototxt",
                       modelPath="db/model/res10_300x300_ssd_iter_140000.caffemodel",
                       embedderPath="db/model/openface_nn4.small2.v1.t7",
                       filename="")
        self.encoder.update_available.connect(self.update_progress)
        # child_pipe = Pipe()
        # self.attendance_thread = AttendanceThread(child_pipe)
        # self.emitter = Emitter(child_pipe)
        # self.emitter.update_available.connect(self.update_progress)
        # self.emitter.new_list.connect(self.combine_std_lists)
        # self.students = Students()
        # self.db = DBHelper()
        # self.db_conn = DBHelper().create_db_connection("db/saqer.db")

    def connect_widgets(self):
        self.parent.i_extract.clicked.connect(self.extract_encodings)

        # self.parent.i_train.clicked.connect(self.train)

    def hide_widgets(self):
        self.parent.i_folder_note.setHidden(True)
        self.parent.i_pickle_note.setHidden(True)
        self.parent.i_train_prolabel.setHidden(True)
        self.parent.i_train_progress.setHidden(True)

    def set_bar_max(self, val):
        self.parent.i_train_progress.setMaximum(val)

    def extract_encodings(self):
        try:
            self.parent.i_folder_note.setHidden(True)
            path = self.parent.i_folder_path.text()
            # path = "D:/Playground/Python/FaceAttendance - Parallelism/class_videos/1k - 2.MOV"
            if path == "":
                self.parent.i_folder_note.setHidden(False)
            else:
                self.show_bar()
                self.encoder.file = path+"/output"
                images_path = list(paths.list_images(path))
                self.encoder.dataset_path = images_path
                self.set_bar_max(len(images_path))
                self.encoder.start()
                # Thread(target=self.encoder.start, args=(images_path,)).start()
                # self.encoder.start(images_path)




                # self.students.clear()
                # self.attendance_thread.max_signal.connect(self.set_bar_max)
                # self.emitter.start()
                # self.attendance_thread.path = path
                # self.attendance_thread.start()
        except Exception as e:
            print(e)

    def show_bar(self):
        self.parent.i_train_prolabel.setHidden(False)
        self.parent.i_train_progress.setHidden(False)
        self.parent.i_train_progress.setValue(0)

    def update_progress(self, val):
        try:
            self.parent.i_train_progress.setValue(self.parent.i_train_progress.value() + val)
        except Exception as e:
            print(e)

