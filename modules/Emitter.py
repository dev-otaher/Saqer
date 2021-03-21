from multiprocessing import Pipe
from typing import List

from PyQt5.QtCore import QThread, pyqtSignal

from modules.Student import Student


class Emitter(QThread):
    """ Emitter waits for data from the process and emits a signal for the UI to update its progress bar. """
    update_available = pyqtSignal(int)  # Signal indicating a frame is processed.
    std_list_signal = pyqtSignal(object)
    students: List[Student]
    def __init__(self, child_pipe: Pipe):
        super().__init__()
        self.child_pipe = child_pipe

    def run(self):
        while True:
            try:
                val = self.child_pipe[0].recv()
                print(type(val))
            except EOFError:
                break
            except Exception as e:
                print(e)
            else:
                if type(val) is int:
                    self.update_available.emit(val)
                elif type(val) is list:
                    self.std_list_signal.emit(val)
        print("Emitter finished...")
