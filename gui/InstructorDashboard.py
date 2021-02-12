from PyQt5.QtWidgets import QDialog
from PyQt5 import uic,QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QVariant
import sqlite3
from PyQt5.QtGui import QCursor, QColor
import sys
from gui import Login


#each interface defined in a class
class InstructorDashboard(QDialog):
    #cnstructor of the class
    def __init__(self):
        super(InstructorDashboard, self).__init__()
        uic.loadUi("gui/interfaces/InstructorDashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_close.clicked.connect(lambda: exit())
        self.i_minmize.clicked.connect(lambda: self.showMinimized())
        self.i_stacked_widget.setCurrentWidget(self.i_courses)
        self.i_view_reports.clicked.connect(self.view_reports)
        self.i_start_session.clicked.connect(self.start_session)
        self.i_end_session.clicked.connect(self.end_session)
        self.i_header.mouseMoveEvent = self.move_window
        self.i_logout.mousePressEvent = self.logout
        self.i_courses_table.setColumnWidth(0,289)
        self.i_courses_table.setColumnWidth(1,289)
        self.i_courses_table.setColumnWidth(2,289)
        self.i_courses_table.horizontalHeaderItem(0).setText("Class")
        self.i_courses_table.horizontalHeaderItem(1).setText("Class Title")
        self.i_courses_table.horizontalHeaderItem(2).setText("Date & Time")
        self.i_courses_table.clicked.connect(self.once_clicked)
        self.i_save.clicked.connect(self.save)
        self.fill_data()
        self.show()

    # Move window around
    def move_window(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def start_session(self):
        self.i_choices.setCurrentWidget(self.i_start_session_sec)

    def view_reports(self):
        self.i_choices.setCurrentWidget(self.i_view_report_sec)
        self.i_stacked_widget.setCurrentWidget(self.i_courses)
        self.i_title.setText("View Reports - Courses")

    def end_session(self):
        self.i_choices.setCurrentWidget(self.i_end_session_sec)

    def logout(self, eve):
        try:

            Login.Login()
            self.destroy()
        except Exception as e:
            print(e)

    def fill_data(self):

        classes = [{"Name":"CS411","Title":"Data Structure", "Time":"1:00 - 3:00 PM"}, {"Name":"CIS432","Title":"Operating Systems", "Time":"1:00 - 3:00 PM"}]
        row = 0
        self.i_courses_table.setRowCount(len(classes))
        for person in classes:
            self.i_courses_table.setItem(row, 0, QtWidgets.QTableWidgetItem(person["Name"]))
            self.i_courses_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["Title"])))
            self.i_courses_table.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Time"]))
            row = row+1

    def once_clicked(self, index):
        try:
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
            self.i_classes_table.clicked.connect(self.test)
        except Exception as e:
            print(e)

    def test(self, index):
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

    def save(self):
        try:
            for i in range(self.i_attendnace_table.rowCount()):
                state = self.i_attendnace_table.cellWidget(i, 2).isChecked()
                name = self.i_attendnace_table.item(i, 0).text()
                print(name)
                print(state)
        except Exception as e:
            print(e)


# app = QApplication(sys.argv)
# mainwindow = InstructorDashboard()
# sys.exit(app.exec_())