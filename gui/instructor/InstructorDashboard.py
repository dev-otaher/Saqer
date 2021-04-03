from functools import partial

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic, QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QColor
from gui import Login, Warning
from gui.instructor.ViewReports import ViewReports
from modules.DBHelper import DBHelper


class InstructorDashboard(QDialog):

    def __init__(self, UUID):
        super(InstructorDashboard, self).__init__()
        uic.loadUi("gui/interfaces/InstructorDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.connect_widgets()
        self.UUID = UUID

        self.i_start.clicked.connect(self.start_recording)
        self.i_save_recheck.clicked.connect(self.save_attendance)
        # self.i_save.clicked.connect(self.save)
        self.db = DBHelper()
        self.view_reports = ViewReports(self)
        self.disable_btn(self.i_end_session)
        self.show()

    def connect_widgets(self):
        self.connect_header()
        self.connect_side_widgets()

    def connect_header(self):
        self.i_header.mouseMoveEvent = self.move_window
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_logout.clicked.connect(self.logout)

    def connect_side_widgets(self):
        self.connect_view_reports()
        self.i_start_session.clicked.connect(partial(self.goto, self.i_choices, self.i_start_session_sec))
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

    def start_session(self):
        self.goto(self.i_choices, self.i_start_session_sec)
        self.goto(self.i_video_sec, self.i_choose_course)

    def start_recording(self):
        self.disable_btn(self.i_start_session)
        self.enable_btn(self.i_end_session)
        self.goto(self.i_video_sec, self.i_video_holder)

    def end_session(self):
        Warning.Warning("Save Class Recording?")
        self.i_choices.setCurrentWidget(self.i_end_session_sec)

    def save_attendance(self):
        print('save attendance test')

    def show_behaviour(self, index):
        column = index.column()
        row = index.row()
        if column == 1:
            # print("i'm "+ self.i_Courses_2.item(row, 1).text()+ " of date: "+ self.i_Courses_2.item(row, 2).text())
            self.i_stacked_widget.setCurrentWidget(self.i_behaviour)
            self.i_behaviour_table.setColumnWidth(0, 217)
            self.i_behaviour_table.setColumnWidth(1, 217)
            self.i_behaviour_table.setColumnWidth(2, 217)
            self.i_behaviour_table.setColumnWidth(3, 217)
            self.i_behaviour_table.horizontalHeaderItem(0).setText("Happy")
            self.i_behaviour_table.horizontalHeaderItem(1).setText("Sad")
            self.i_behaviour_table.horizontalHeaderItem(2).setText("Sleepy")
            self.i_behaviour_table.horizontalHeaderItem(3).setText("Natural")

            classes = [{"Happy": "20%", "Sad": "35%", "Sleepy": "15%", "Natural": "30%", "To": "30%"}]

            row = 0
            self.i_behaviour_table.setRowCount(len(classes))

            for behaviour in classes:
                self.i_behaviour_table.setItem(row, 0, QtWidgets.QTableWidgetItem(behaviour["Happy"]))
                self.i_behaviour_table.setItem(row, 1, QtWidgets.QTableWidgetItem(behaviour["Sad"]))
                self.i_behaviour_table.setItem(row, 2, QtWidgets.QTableWidgetItem(behaviour["Sleepy"]))
                self.i_behaviour_table.setItem(row, 3, QtWidgets.QTableWidgetItem(behaviour["Natural"]))

                row = row + 1

        elif column == 0:
            # print("i'm "+ self.i_Courses_2.item(row, 0).text()+ " of date: "+ self.i_Courses_2.item(row, 2).text())
            self.i_stacked_widget.setCurrentWidget(self.i_attendnace)

            self.i_attendnace_table.setColumnWidth(0, 289)
            self.i_attendnace_table.setColumnWidth(1, 289)
            self.i_attendnace_table.setColumnWidth(2, 289)
            self.i_attendnace_table.horizontalHeaderItem(0).setText("Student ID")
            self.i_attendnace_table.horizontalHeaderItem(1).setText("Name")
            self.i_attendnace_table.horizontalHeaderItem(2).setText("Present")

            classes = [{"ID": "2170007739", "Name": "Khalid Awlaqi"},
                       {"ID": "2170007760", "Name": "Waleed Al-Harthi"}]

            row = 0
            self.i_attendnace_table.setRowCount(len(classes))

            for attendance in classes:
                self.i_attendnace_table.setItem(row, 0, QtWidgets.QTableWidgetItem(attendance["ID"]))
                self.i_attendnace_table.setItem(row, 1, QtWidgets.QTableWidgetItem(attendance["Name"]))
                self.checkbox = QtWidgets.QCheckBox("")
                self.checkbox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                self.i_attendnace_table.setCellWidget(row, 2, self.checkbox)

                row = row + 1

    def enable_btn(self, btn):
        btn.setEnabled(True)
        self.i_end_session.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                                         "#38DBD0;color:#ffffff}QPushButton:hover {background-color: "
                                         "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def disable_btn(self, btn):
        btn.setEnabled(False)
        btn.setStyleSheet("QPushButton {border-radius: 25px;background-color: "
                          "#727272;color:#ffffff}QPushButton:hover {background-color: "
                          "#23b2a8; color: rgb(255, 255, 255);} QPushButton:pressed { background-color: #38DBD0; }")

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)
