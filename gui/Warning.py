from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from gui import InstructorDashboard

class Warning(QDialog):

    def __init__(self, msg):
        super(Warning, self).__init__()
        loadUi("gui/interfaces/Warning.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.setWindowModality(Qt.ApplicationModal)
        self.i_yes.clicked.connect(self.save_recording)
        self.i_no.clicked.connect(lambda: self.hide())
        self.i_message.setText(msg)
        self.show()

    def save_recording(self):
        pass
