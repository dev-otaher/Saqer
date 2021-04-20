from os import getcwd, mkdir
from os.path import sep, exists, dirname

from imutils import paths

from gui.Success import Success
from gui.Warning import Warning
from modules.Encoder import Encoder
from modules.Trainer import Trainer


class TrainModel:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.encoder = None
        self.trainer = Trainer(75.0)
        self.trainer.finished.connect(lambda: Success("Model trained successfully!"))

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

    def prepare_encoder(self):
        proto_path = sep.join([getcwd(), 'db', 'model', 'deploy.prototxt'])
        model_path = sep.join([getcwd(), 'db', 'model', 'res10_300x300_ssd_iter_140000.caffemodel'])
        embedder_path = sep.join([getcwd(), 'db', 'model', 'openface_nn4.small2.v1.t7'])
        if not exists(proto_path):
            Warning('Could not find "db/model/deploy.prototxt"!')
            return False
        elif not exists(model_path):
            Warning('Could not find "db/model/res10_300x300_ssd_iter_140000.caffemodel"!')
            return False
        elif not exists(embedder_path):
            Warning('Could not find "db/model/openface_nn4.small2.v1.t7"!')
            return False
        else:
            self.encoder = Encoder(proto_path, model_path, embedder_path)
            self.encoder.update_available.connect(self.update_progress)
            return True

    def extract_encodings(self):
        try:
            self.parent.i_folder_note.setHidden(True)
            path = self.parent.i_folder_path.text()
            images_path = list(paths.list_images(path))
            if path == "":
                self.parent.i_folder_note.setText("No folder selected!")
                self.parent.i_folder_note.setHidden(False)
            elif len(images_path) == 0:
                self.parent.i_folder_note.setText("No pictures found!")
                self.parent.i_folder_note.setHidden(False)
            elif self.prepare_encoder():
                self.reset_bar()
                self.show_bar()
                self.encoder.output_path = sep.join([path, 'output'])
                if not exists(self.encoder.output_path): mkdir(self.encoder.output_path)
                self.encoder.dataset_path = images_path
                self.set_bar_max(len(images_path))
                self.encoder.start()
        except Exception as e:
            Warning(str(e))
            print(e)

    def train(self):
        try:
            self.parent.i_pickle_note.setHidden(True)
            path = self.parent.i_pickle_path.text()
            if path == "":
                self.parent.i_pickle_note.setHidden(False)
            elif not exists(path):
                Warning("Could not find file! File might be deleted or not accessible!")
            else:
                self.show_bar()
                self.reset_bar()
                self.trainer.encodings_path = self.parent.i_pickle_path.text()
                dir = dirname(self.trainer.encodings_path)
                self.trainer.output_path = dir
                self.trainer.start()
        except Exception as e:
            Warning(str(e))
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
            Warning(str(e))
            print(e)
