import sys
from functools import partial
from os.path import sep

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from gui.Warning import Warning
from gui.instructor.Session import Session
from gui.instructor.ViewReports import ViewReports
from modules.DBHelper import DBHelper


class InstructorDashboard(QDialog):

    def __init__(self, UUID):
        super(InstructorDashboard, self).__init__()
        uic.loadUi(sep.join(['gui', 'interfaces', 'InstructorDashboard.ui']), self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.connect_widgets()
        self.UUID = UUID
        self.db = DBHelper()
        self.view_reports = ViewReports(self)
        self.session = Session(self)
        self.disable_btn(self.i_end_session)
        self.show()

    def connect_widgets(self):
        self.connect_header()
        self.connect_side_widgets()

    def connect_header(self):
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: sys.exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.clicked.connect(self.logout)

    def connect_side_widgets(self):
        self.connect_view_reports()
        self.i_start_session.clicked.connect(partial(self.goto, self.i_choices, self.i_start_session_sec))
        self.i_start_session.clicked.connect(partial(self.goto, self.i_video_sec, self.i_choose_course))
        self.i_end_session.clicked.connect(partial(self.goto, self.i_choices, self.i_end_session_sec))

    def connect_view_reports(self):
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_choices, self.i_view_report_sec))
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_stacked_widget, self.i_courses))
        self.i_view_reports.clicked.connect(partial(self.i_title.setText, "View Reports - Courses"))

    @staticmethod
    def goto(parent_widget, widget):
        parent_widget.setCurrentWidget(widget)

    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def end_session(self):
        self.i_choices.setCurrentWidget(self.i_end_session_sec)

    def enable_btn(self, btn):
        btn.setEnabled(True)
        btn.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                                         "#38DBD0;color:#ffffff}QPushButton:hover {background-color: "
                                         "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def disable_btn(self, btn):
        btn.setEnabled(False)
        btn.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                          "#727272;color:#ffffff}QPushButton:hover {background-color: "
                          "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def logout(self):
        try:
            if self.session.vt is not None: self.session.vt.threadActive = False
            from gui.Login import Login
            mainwindow = Login()
            self.destroy()
        except Exception as e:
            Warning(str(e))
            print(e)
