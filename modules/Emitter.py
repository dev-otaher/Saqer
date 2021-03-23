from multiprocessing import Pipe
from typing import List

from PyQt5.QtCore import QThread, pyqtSignal

from modules.Student import Student
from modules.Students import Students


class Emitter(QThread):
    """ Emitter waits for data from the process and emits a signal for the UI to update its progress bar. """
    update_available = pyqtSignal(int)  # Signal indicating a frame is processed.
    std_list_signal = pyqtSignal(list)
    students = Students()

    def __init__(self, child_pipe: Pipe):
        super().__init__()
        self.child_pipe = child_pipe

    def run(self):
        while True:
            try:
                msg = self.child_pipe[0].recv()
            except EOFError:
                break
            except Exception as e:
                print(e)
            else:
                if type(msg) is int:
                    self.update_available.emit(msg)
                elif type(msg) is list:
                    self.students.extend(msg)
                    self.std_list_signal.emit(self.students)
        print("Emitter finished...")
