from functools import partial

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic,QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QVariant
import sqlite3
from PyQt5.QtGui import QCursor, QColor
import sys
from gui import Login, Warning


#each interface defined in a class
from gui.instructor.ViewReports import ViewReports
from modules.DBHelper import DBHelper


class InstructorDashboard(QDialog):
    #cnstructor of the class
    def __init__(self, UUID):
        super(InstructorDashboard, self).__init__()
        uic.loadUi("gui/interfaces/InstructorDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.connect_widgets()
        self.UUID = UUID

        self.i_start.clicked.connect(self.start_recording)
        self.i_save_recheck.clicked.connect(self.save_attendance)
        self.i_courses_table.clicked.connect(self.select_course)
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
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_choices, self.i_view_report_sec))
        self.i_view_reports.clicked.connect(partial(self.goto, self.i_stacked_widget, self.i_courses))
        self.i_start_session.clicked.connect(partial(self.goto, self.i_choices, self.i_start_session_sec))
        self.i_end_session.clicked.connect(partial(self.goto, self.i_choices, self.i_end_session_sec))

    @staticmethod
    def goto(parent_widget, widget):
        parent_widget.setCurrentWidget(widget)

    # Move window around
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

    def view_reports(self):
        self.i_choices.setCurrentWidget(self.i_view_report_sec)
        self.i_stacked_widget.setCurrentWidget(self.i_courses)
        self.i_title.setText("View Reports - Courses")

    def end_session(self):
        Warning.Warning("Save Class Recording?")
        self.i_choices.setCurrentWidget(self.i_end_session_sec)

    def save_attendance(self):
        print('save attendance test')

    def logout(self):
        try:
            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)

    def select_course(self, index):
        try:
            print(index)
            row = index.row()
            column = index.column()
            self.i_title.setText("View Reports of: "+ self.i_courses_table.item (row, 1).text()+" "+self.i_courses_table.item (row, 2).text())
            self.i_stacked_widget.setCurrentWidget(self.i_classes)
            self.i_classes_table.setColumnWidth(0, 174)
            self.i_classes_table.setColumnWidth(1, 174)
            self.i_classes_table.setColumnWidth(2, 174)
            self.i_classes_table.setColumnWidth(3, 174)
            self.i_classes_table.setColumnWidth(4, 174)
            self.i_classes_table.horizontalHeaderItem(0).setText("Attendance")
            self.i_classes_table.horizontalHeaderItem(1).setText("Behaviour")
            self.i_classes_table.horizontalHeaderItem(2).setText("Attendance Date")
            self.i_classes_table.horizontalHeaderItem(3).setText("From")
            self.i_classes_table.horizontalHeaderItem(4).setText("To")

            classes = [{"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "09/01/2020", "From": "1:00 PM", "To": "03:00 PM"},
                       {"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "10/01/2020", "From": "8:00 PM", "To": "10:00 PM"},
                       {"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "11/01/2020", "From": "12:00 PM", "To": "03:00 PM"}]
            row = 0
            self.i_classes_table.setRowCount(len(classes))
            for person in classes:
                atten = QtWidgets.QTableWidgetItem(person["Attendance1"])
                atten.setForeground(QColor(56, 219, 208))
                behv =  QtWidgets.QTableWidgetItem(person["Behaviour"])
                behv.setForeground(QColor(56, 219, 208))
                rest = QtWidgets.QTableWidgetItem(person["Attendance"])
                rest2 = QtWidgets.QTableWidgetItem(person["From"])
                rest3 = QtWidgets.QTableWidgetItem(person["To"])

                rest.setForeground(QColor(255, 255, 255))
                rest2.setForeground(QColor(255, 255, 255))
                rest3.setForeground(QColor(255, 255, 255))


                self.i_classes_table.setItem(row, 0, atten)
                self.i_classes_table.setItem(row, 1, behv)
                self.i_classes_table.setItem(row, 2, rest)
                self.i_classes_table.setItem(row, 3, rest2)
                self.i_classes_table.setItem(row, 4, rest3)
                row = row + 1
            self.i_classes_table.clicked.connect(self.show_behaviour)
        except Exception as e:
            print(e)

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

            classes = [{"Happy": "20%", "Sad": "35%", "Sleepy": "15%","Natural": "30%", "To": "30%"}]

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

