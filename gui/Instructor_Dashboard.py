from PyQt5.QtWidgets import QDialog
from PyQt5 import uic,QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import sys
from gui import Login

#each interface defined in a class
class Instructor_Dash(QDialog):

    #cnstructor of the class
    def __init__(self):

        super(Instructor_Dash, self).__init__()
        uic.loadUi("gui/Interfaces files/Instructor_Dashboard.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint))
        self.i_closewindow.clicked.connect(lambda: exit())
        self.i_minmizewindow.clicked.connect(lambda: self.showMinimized())
        self.i_Choices.setCurrentWidget(self.i_CoursesTable)
        self.i_ViewReports.clicked.connect(self.ViewReportsFunc)
        self.i_StartSession.clicked.connect(self.StartSessionFunc)
        self.i_EndSession.clicked.connect(self.EndSessionFunc)
        self.i_Header.mouseMoveEvent = self.moveWindow
        self.i_logout.mousePressEvent = self.logout
        self.i_Courses.setColumnWidth(0,289)
        self.i_Courses.setColumnWidth(1,289)
        self.i_Courses.setColumnWidth(2,289)
        self.i_Courses.horizontalHeaderItem(0).setText("Class")
        self.i_Courses.horizontalHeaderItem(1).setText("Class Title")
        self.i_Courses.horizontalHeaderItem(2).setText("Date & Time")
        self.i_Courses.doubleClicked.connect(self.on_click)


        self.filldata()
        self.show()


        # Move window around

    def moveWindow(self, e):
        if e.buttons() == Qt.LeftButton:
            self.move(self.pos() + e.globalPos() - self.clickPosition)
            self.clickPosition = e.globalPos()
            e.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def StartSessionFunc(self):
        self.i_Choices.setCurrentWidget(self.i_StartSessionWid)

    def ViewReportsFunc(self):
        self.i_Choices.setCurrentWidget(self.i_ViewReportsWid)
        self.i_ViewReportsWid_2.setCurrentWidget(self.i_CoursesTable)

    def EndSessionFunc(self):
        self.i_Choices.setCurrentWidget(self.i_EndSessionWid)

    def logout(self, eve):
        Login.Login()
        self.destroy()

    def filldata(self):
        classes = [{"Name":"CS411","Title":"Data Structure", "Time":"1:00 - 3:00 PM"}, {"Name":"CIS432","Title":"Shit", "Time":"1:00 - 3:00 PM"}]
        row = 0
        self.i_Courses.setRowCount(len(classes))



        for person in classes:
            self.i_Courses.setItem(row, 0, QtWidgets.QTableWidgetItem(person["Name"]))
            self.i_Courses.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["Title"])))
            self.i_Courses.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Time"]))
                                
            row = row+1

    def on_click(self, index):
        row = index.row()
        column = index.column()
        self.i_ViewReportsWid_2.setCurrentWidget(self.i_ClassSelected)
        self.i_ClassSelectedLabel.setText("I'm "+ self.i_Courses.item(row, column).text())


