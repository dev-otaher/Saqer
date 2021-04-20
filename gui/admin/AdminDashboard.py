import sys
from functools import partial
from os.path import sep

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog

from gui.Warning import Warning
from gui.admin.OfflineAttendance import OfflineAttendance
from gui.admin.RegisterStudent import RegisterStudent
from gui.admin.TrainModel import TrainModel
from modules.DBHelper import DBHelper


class AdminDashboard(QDialog):
    def __init__(self):
        super(AdminDashboard, self).__init__()
        uic.loadUi(sep.join(['gui', 'interfaces', 'AdminDashboard.ui']), self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.connect_widgets()
        self.db = DBHelper()
        self.register_student = RegisterStudent(parent_gui=self)
        self.train_model = TrainModel(parent_gui=self)
        self.offline_attendance = OfflineAttendance(parent_gui=self)
        self.show()

    def connect_widgets(self):
        self.connect_header()
        self.connect_side_widgets()
        self.connect_browser_btns()

    def connect_header(self):
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: sys.exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.clicked.connect(self.logout)

    def connect_side_widgets(self):
        self.i_register_student.clicked.connect(partial(self.goto, self.i_register_sec))
        self.i_train_model.clicked.connect(partial(self.goto, self.i_train_sec))
        self.i_offline_atten.clicked.connect(partial(self.goto, self.i_offline_sec))

    def connect_browser_btns(self):
        self.i_choose_folder.clicked.connect(self.browse_folder)
        self.i_choose_encodings.clicked.connect(self.browse_file)

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, e):
        self.clickPosition = e.globalPos()

    def goto(self, widget):
        self.i_choices.setCurrentWidget(widget)

    def browse_file(self):
        btn_text = self.sender().text()
        caption = filter = ""
        if btn_text == "Choose Encodings":
            caption = "Choose Encodings..."
            filter = "Pickle File (*.pickle)"
        elif btn_text == "Choose Video":
            caption = "Choose Video..."
            filter = "Video (*.mp4 , *.mkv , *.MOV)"
        path = QFileDialog.getOpenFileName(self, caption, '', filter)
        if btn_text == "Choose Encodings":
            self.i_pickle_path.setText(path[0])
        elif btn_text == "Choose Video":
            self.i_video_path.setText(path[0])

    def browse_folder(self):
        btn_text = self.sender().text()
        if btn_text == "Choose Folder":
            path = QFileDialog.getExistingDirectory(self, 'Choose Folder...')
            self.i_folder_path.setText(path)

    def logout(self):
        try:
            from gui.Login import Login
            if self.register_student is not None: self.register_student.stop_cam()
            if self.train_model.encoder is not None: self.train_model.encoder.is_thread_active = False
            mainwindow = Login()
            self.destroy()
        except Exception as e:
            Warning(str(e))
            print(e)
