from multiprocessing import Pipe
from PyQt5.QtCore import QThread, pyqtSignal


class Emitter(QThread):
    """ Emitter waits for data from the process and emits a signal for the UI to update its progress bar. """
    update_available = pyqtSignal(int)  # Signal indicating a frame is processed.
    new_list = pyqtSignal(list)

    def __init__(self, child_pipe: Pipe):
        super().__init__()
        self.child_pipe = child_pipe

    def run(self):
        while True:
            try:
                msg = self.child_pipe[0].recv()
            except Exception as e:
                print(e)
            else:
                if type(msg) is int:
                    self.update_available.emit(msg)
                elif type(msg) is list:
                    self.new_list.emit(msg)
