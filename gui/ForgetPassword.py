import json
import re
from os.path import sep

import pyrebase
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from gui import Success
from gui.Warning import Warning


class ForgetPassword(QDialog):
    def __init__(self):
        super(ForgetPassword, self).__init__()
        loadUi(sep.join(['gui', 'interfaces', 'ForgetPassword.ui']), self)
        self.i_send.clicked.connect(self.send_email)
        self.i_close.clicked.connect(lambda: self.close())
        self.i_email_note.setHidden(True)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_header.mouseMoveEvent = self.move_window
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    #move window around
    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    # This function runs when the 'Send' button clicked
    def send_email(self):
        try:
            pattern = r"\"?([-a-zA-Z0-9_.`?{}]+@\w+\.\w+)\"?"
            re.compile(pattern)
            email = self.i_email.text().strip()
            if email == "" or not re.match(pattern, email):
                self.i_email_note.setHidden(False)
            else:
                with open(sep.join(['db', 'fbConfig.json'])) as file:
                  config = json.load(file)
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                auth.send_password_reset_email(email)
                Success.Success("We've sent reset link to your email.")
                self.destroy()
        except Exception as e:
            # if there's error in the email authentication show error message
            Warning(str(e))
            print(e)
