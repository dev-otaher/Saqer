import os
from imutils import paths
from gui.Success import Success
from modules.Encoder import Encoder
from modules.Trainer import Trainer


class TrainModel:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()

        self.encoder = Encoder(protoPath="db/model/deploy.prototxt",
                       modelPath="db/model/res10_300x300_ssd_iter_140000.caffemodel",
                       embedderPath="db/model/openface_nn4.small2.v1.t7")
        self.encoder.update_available.connect(self.update_progress)

        self.trainer = Trainer(75.0)
        self.trainer.finished.connect(lambda: Success(""))

    def connect_widgets(self):
        self.parent.i_extract.clicked.connect(self.extract_encodings)
        self.parent.i_train.clicked.connect(self.train)

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
            if path == "":
                self.parent.i_folder_note.setHidden(False)
            else:
                self.show_bar()
                self.reset_bar()
                self.encoder.file = path+"/output"
                images_path = list(paths.list_images(path))
                self.encoder.dataset_path = images_path
                self.set_bar_max(len(images_path))
                self.encoder.start()
        except Exception as e:
            print(e)

    def train(self):
        try:
            self.parent.i_pickle_note.setHidden(True)
            path = self.parent.i_pickle_path.text()
            # path = "D:/Playground/Python/FaceAttendance - Parallelism/class_videos/1k - 2.MOV"
            if path == "":
                self.parent.i_pickle_note.setHidden(False)
            else:
                self.show_bar()
                self.reset_bar()
                self.trainer.encodings_path = self.parent.i_pickle_path.text()
                dir = os.path.dirname(self.trainer.encodings_path)
                self.trainer.output_path = dir
                self.trainer.start()
        except Exception as e:
            print(e)

    def show_bar(self):
        self.parent.i_train_prolabel.setHidden(False)
        self.parent.i_train_progress.setHidden(False)

    def reset_bar(self):
        self.parent.i_train_progress.setValue(0)

    def update_progress(self, val):
        try:
            self.parent.i_train_progress.setValue(self.parent.i_train_progress.value() + val)
        except Exception as e:
            print(e)

