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
        uic.loadUi("gui/Interfaces files/Instructor_Dashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_closewindow.clicked.connect(lambda: exit())
        self.i_minmizewindow.clicked.connect(lambda: self.showMinimized())
        self.i_tablesWidgets.setCurrentWidget(self.i_CoursesTable)
        self.i_ViewReports.clicked.connect(self.view_reports)
        self.i_StartSession.clicked.connect(self.start_session)
        self.i_EndSession.clicked.connect(self.end_session)
        self.i_Header.mouseMoveEvent = self.move_window
        self.i_logout.mousePressEvent = self.logout
        self.i_Courses.setColumnWidth(0,289)
        self.i_Courses.setColumnWidth(1,289)
        self.i_Courses.setColumnWidth(2,289)
        self.i_Courses.horizontalHeaderItem(0).setText("Class")
        self.i_Courses.horizontalHeaderItem(1).setText("Class Title")
        self.i_Courses.horizontalHeaderItem(2).setText("Date & Time")
        self.i_Courses.clicked.connect(self.once_clicked)
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
        self.i_Choices.setCurrentWidget(self.i_StartSessionWid)

    def view_reports(self):
        self.i_Choices.setCurrentWidget(self.i_ViewReportsWid)
        self.i_tablesWidgets.setCurrentWidget(self.i_CoursesTable)
        self.i_TableTitle.setText("View Reports - Courses")

    def end_session(self):
        self.i_Choices.setCurrentWidget(self.i_EndSessionWid)

    def logout(self, eve):
        Login.Login()
        self.destroy()

    def fill_data(self):

        classes = [{"Name":"CS411","Title":"Data Structure", "Time":"1:00 - 3:00 PM"}, {"Name":"CIS432","Title":"Operating Systems", "Time":"1:00 - 3:00 PM"}]
        row = 0
        self.i_Courses.setRowCount(len(classes))
        for person in classes:
            self.i_Courses.setItem(row, 0, QtWidgets.QTableWidgetItem(person["Name"]))
            self.i_Courses.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["Title"])))
            self.i_Courses.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Time"]))
            row = row+1

    def once_clicked(self, index):

        row = index.row()
        column = index.column()
        self.i_TableTitle.setText("View Reports of: "+ self.i_Courses.item (row, 1).text()+" "+self.i_Courses.item (row, 2).text())
        self.i_tablesWidgets.setCurrentWidget(self.i_ClassSelected)
        self.i_Courses_2.setColumnWidth(0, 174)
        self.i_Courses_2.setColumnWidth(1, 174)
        self.i_Courses_2.setColumnWidth(2, 174)
        self.i_Courses_2.setColumnWidth(3, 174)
        self.i_Courses_2.setColumnWidth(4, 174)
        self.i_Courses_2.horizontalHeaderItem(0).setText("Attendance")
        self.i_Courses_2.horizontalHeaderItem(1).setText("Behaviour")
        self.i_Courses_2.horizontalHeaderItem(2).setText("Attendance Date")
        self.i_Courses_2.horizontalHeaderItem(3).setText("From")
        self.i_Courses_2.horizontalHeaderItem(4).setText("To")


        classes = [{"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "09/01/2020", "From": "1:00 PM", "To": "03:00 PM"},
                   {"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "10/01/2020", "From": "8:00 PM", "To": "10:00 PM"},
                   {"Attendance1":"Attendance Reports" ,"Behaviour":"Behaviour Reports","Attendance": "11/01/2020", "From": "12:00 PM", "To": "03:00 PM"}]
        row = 0
        self.i_Courses_2.setRowCount(len(classes))
        try:
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


                self.i_Courses_2.setItem(row, 0, atten)
                self.i_Courses_2.setItem(row, 1, behv)
                self.i_Courses_2.setItem(row, 2, rest)
                self.i_Courses_2.setItem(row, 3, rest2)
                self.i_Courses_2.setItem(row, 4, rest3)
                row = row + 1
        except Exception as e:
            print(e)
        self.i_Courses_2.clicked.connect(self.test)

    def test(self, index):
        column = index.column()
        row = index.row()
        if column == 1:
            # print("i'm "+ self.i_Courses_2.item(row, 1).text()+ " of date: "+ self.i_Courses_2.item(row, 2).text())
            self.i_tablesWidgets.setCurrentWidget(self.i_BehaviourReport)
            self.i_Courses_behaviour.setColumnWidth(0, 217)
            self.i_Courses_behaviour.setColumnWidth(1, 217)
            self.i_Courses_behaviour.setColumnWidth(2, 217)
            self.i_Courses_behaviour.setColumnWidth(3, 217)
            self.i_Courses_behaviour.horizontalHeaderItem(0).setText("Happy")
            self.i_Courses_behaviour.horizontalHeaderItem(1).setText("Sad")
            self.i_Courses_behaviour.horizontalHeaderItem(2).setText("Sleepy")
            self.i_Courses_behaviour.horizontalHeaderItem(3).setText("Natural")

            classes = [{"Happy": "20%", "Sad": "35%", "Sleepy": "15%","Natural": "30%", "To": "30%"}]

            row = 0
            self.i_Courses_behaviour.setRowCount(len(classes))

            for behaviour in classes:
                self.i_Courses_behaviour.setItem(row, 0, QtWidgets.QTableWidgetItem(behaviour["Happy"]))
                self.i_Courses_behaviour.setItem(row, 1, QtWidgets.QTableWidgetItem(behaviour["Sad"]))
                self.i_Courses_behaviour.setItem(row, 2, QtWidgets.QTableWidgetItem(behaviour["Sleepy"]))
                self.i_Courses_behaviour.setItem(row, 3, QtWidgets.QTableWidgetItem(behaviour["Natural"]))

                row = row + 1

        elif column == 0:
            # print("i'm "+ self.i_Courses_2.item(row, 0).text()+ " of date: "+ self.i_Courses_2.item(row, 2).text())
            self.i_tablesWidgets.setCurrentWidget(self.i_AttendnaceReport)

            self.i_Courses_attendnace.setColumnWidth(0, 289)
            self.i_Courses_attendnace.setColumnWidth(1, 289)
            self.i_Courses_attendnace.setColumnWidth(2, 289)
            self.i_Courses_attendnace.horizontalHeaderItem(0).setText("Student ID")
            self.i_Courses_attendnace.horizontalHeaderItem(1).setText("Name")
            self.i_Courses_attendnace.horizontalHeaderItem(2).setText("Present")

            classes = [{"ID": "2170007739", "Name": "Khalid Awlaqi"},
                       {"ID": "2170007760", "Name": "Waleed Al-Harthi"}]

            row = 0
            self.i_Courses_attendnace.setRowCount(len(classes))

            for attendance in classes:
                self.i_Courses_attendnace.setItem(row, 0, QtWidgets.QTableWidgetItem(attendance["ID"]))
                self.i_Courses_attendnace.setItem(row, 1, QtWidgets.QTableWidgetItem(attendance["Name"]))
                self.checkbox = QtWidgets.QCheckBox("")
                self.checkbox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                self.i_Courses_attendnace.setCellWidget(row, 2, self.checkbox)

                row = row + 1

    def save(self):
        try:
            for i in range(self.i_Courses_attendnace.rowCount()):
                state = self.i_Courses_attendnace.cellWidget(i, 2).isChecked()
                name = self.i_Courses_attendnace.item(i, 0).text()
                print(name)
                print(state)
        except Exception as e:
            print(e)

#
# app = QApplication(sys.argv)
# mainwindow = InstructorDashboard()
# sys.exit(app.exec_())