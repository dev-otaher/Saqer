from sqlite3 import Error

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy, QPushButton
from qtpy import QtWidgets

from gui.Success import Success
from gui.Warning import Warning


def hide_column(table, index):
    table.setColumnHidden(index, True)


def reset_table(table):
    table.clearContents()
    table.setRowCount(0)


class ViewReports:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_courses()

    def connect_widgets(self):
        self.parent.i_courses_table.clicked.connect(self.fill_classes)
        self.parent.i_classes_table.clicked.connect(self.fill_report)
        self.parent.i_save.clicked.connect(self.save_attendance)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        hide_column(self.parent.i_classes_table, 0)
        hide_column(self.parent.i_courses_table, 0)
        hide_column(self.parent.i_attendance_table, 0)
        hide_column(self.parent.i_attendance_table, 4)

    def fill_courses(self):
        try:
            sql = '''
                    SELECT DISTINCT	course.id, course.code, course.title FROM class 
                    INNER JOIN course ON class.course_id == course.id 
                    WHERE instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (self.parent.UUID,))
            courses = cur.fetchall()
            for course in courses:
                self.add_course(course)
        except Error as e:
            Warning(str(e))
            print(e)

    def add_course(self, c):
        self.parent.i_courses_table.insertRow(0)
        for i in range(3):
            self.parent.i_courses_table.setItem(0, i, QtWidgets.QTableWidgetItem(str(c[i])))

    def fill_classes(self, location: QModelIndex):
        try:
            row = location.row()
            course_id = self.parent.i_courses_table.item(row, 0).text()

            sql = '''
                    SELECT DISTINCT class.id, title, date_time FROM class
                    INNER JOIN attendance a on class.id = a.class_id
                    WHERE course_id=? AND instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (course_id, self.parent.UUID))
            classes = cur.fetchall()

            reset_table(self.parent.i_classes_table)
            for c in classes:
                self.add_class(c)

            self.parent.goto(self.parent.i_stacked_widget, self.parent.i_classes)
            self.parent.i_title.setText("View Reports - Classes")
        except Error as e:
            Warning(str(e))
        except Exception as e:
            print(e)

    def add_class(self, c):
        self.parent.i_classes_table.insertRow(0)
        a = QtWidgets.QTableWidgetItem("Attendance")
        a.setForeground(QColor(56, 219, 208))
        self.parent.i_classes_table.setItem(0, 1, a)
        b = QtWidgets.QTableWidgetItem("Behaviour")
        b.setForeground(QColor(56, 219, 208))
        self.parent.i_classes_table.setItem(0, 2, b)
        # fill "Id" column
        self.parent.i_classes_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(c[0])))
        # fill "Title" column
        self.parent.i_classes_table.setItem(0, 3, QtWidgets.QTableWidgetItem(str(c[1])))
        # fill "Date & Time" column
        self.parent.i_classes_table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(c[2])))

    def fill_report(self, location):
        try:
            row, column = location.row(), location.column()
            class_id = self.parent.i_classes_table.item(row, 0).text()
            date_time = self.parent.i_classes_table.item(row, 4).text()
            if column == 1:
                sql = '''
                        SELECT class_id, student_id, s.name, status, date_time FROM attendance
                        INNER JOIN student s on s.uni_id = attendance.student_id
                        WHERE class_id=? AND date_time=?;
                        '''
            elif column == 2:
                sql = '''
                        SELECT happy, sad, neutral FROM behavior 
                        WHERE class_id=? AND date_time=?;
                        '''
            else:
                return
            cur = self.db_conn.cursor()
            cur.execute(sql, (class_id, date_time))
            records = cur.fetchall()
            if column == 1:
                reset_table(self.parent.i_attendance_table)
                for r in records:
                    self.parent.i_attendance_table.insertRow(0)
                    self.parent.i_attendance_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(r[0])))
                    self.parent.i_attendance_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(r[1])))
                    self.parent.i_attendance_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(r[2])))
                    checkbox = QtWidgets.QCheckBox()
                    checkbox.setChecked(r[3])
                    self.parent.i_attendance_table.setCellWidget(0, 3, checkbox)
                    self.parent.i_attendance_table.setItem(0, 4, QtWidgets.QTableWidgetItem(str(r[4])))
                self.parent.goto(self.parent.i_stacked_widget, self.parent.i_attendance)
                self.parent.i_title.setText("View Reports - Attendance")
            elif column == 2:
                reset_table(self.parent.i_behaviour_table)
                for r in records:
                    self.parent.i_behaviour_table.insertRow(0)
                    for i in range(3):
                        self.parent.i_behaviour_table.setItem(0, i, QtWidgets.QTableWidgetItem(str(r[i]) + "%"))
                self.parent.goto(self.parent.i_stacked_widget, self.parent.i_behaviour)
                self.parent.i_title.setText("View Reports - Behaviour")
        except Exception as e:
            print(e)



    def save_attendance(self):
        try:
            sql = '''
                    UPDATE attendance
                    SET status = ?
                    WHERE student_id = ? AND class_id = ? AND date_time=?
                    '''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_attendance_table.rowCount()):
                class_id = self.parent.i_attendance_table.item(r, 0).text()
                student_id = self.parent.i_attendance_table.item(r, 1).text()
                status = int(self.parent.i_attendance_table.cellWidget(r, 3).isChecked())
                date_time = self.parent.i_attendance_table.item(r, 4).text()
                cur.execute(sql, (status, student_id, class_id, date_time))
                self.db_conn.commit()
            Success("Attendance Updated!")
            self.parent.goto(self.parent.i_stacked_widget, self.parent.i_courses)
        except Exception as e:
            Warning(str(e))
            print(e)
