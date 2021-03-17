from multiprocessing import Pipe

from PyQt5.QtCore import QThread, pyqtSignal


class Emitter(QThread):
    """ Emitter waits for data from the capitalization process and emits a signal for the UI to update its text. """
    update_available = pyqtSignal(int)  # Signal indicating new UI data is available.
    def __init__(self, child_pipe: Pipe):
        super().__init__()
        self.child_pipe = child_pipe

    def run(self):
        while True:
            try:
                val = self.child_pipe[0].recv()
            except EOFError:
                print("EOFError")
                break
            except Exception as e:
                print(e)
            else:
                self.update_available.emit(val)
