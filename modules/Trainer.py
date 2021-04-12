import pickle
from datetime import datetime

from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC


class Trainer(QThread):
    finished = pyqtSignal(int)
    def __init__(self, C=5):
        super(Trainer, self).__init__()
        self.encodings_path = str()
        self.output_path = str()
        self.C = C

    def get_current_datetime(self):
        return datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

    def run(self):
        # load the face embeddings
        data = pickle.loads(open(self.encodings_path, 'rb').read())

        # encode the labels
        le = LabelEncoder()
        labels = le.fit_transform(data['names'])

        # train the model used to accept the 128-d embeddings of the face and
        # then produce the actual face recognition
        # recognizer = KNeighborsClassifier(n_neighbors=self.n_neighbours)
        recognizer = SVC(C=self.C, probability=True)
        recognizer.fit(data['embeddings'], labels)

        # write the actual face recognition model to disk
        f = open(f"{self.output_path}/recognizer.pickle", 'wb')
        f.write(pickle.dumps(recognizer))
        f.close()

        # write the label encoder to disk
        f = open(f"{self.output_path}/labels.pickle", 'wb')
        f.write(pickle.dumps(le))
        f.close()
        self.finished.emit(1)
