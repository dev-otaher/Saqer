from sqlite3 import Error

from PyQt5.QtCore import QModelIndex, QVariant
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy, QPushButton, QComboBox
from qtpy import QtWidgets
from gui.Warning import Warning


class Session:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_courses()

    def connect_widgets(self):
        self.parent.i_courses_cb.currentIndexChanged.connect(self.fill_classes)
        self.parent.i_start.clicked.connect(self.start_recording)

        # self.parent.i_courses_table.clicked.connect(self.fill_classes)
        # self.parent.i_classes_table.clicked.connect(self.fill_report)
        # self.parent.i_save.clicked.connect(self.save_attendance)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        self.hide_first_column(self.parent.i_classes_table)
        self.hide_first_column(self.parent.i_courses_table)
        self.hide_first_column(self.parent.i_attendance_table)

    def hide_first_column(self, table):
        table.setColumnHidden(0, True)
        table.setColumnHidden(0, True)

    def fill_courses(self):
        try:
            sql = '''
                    SELECT DISTINCT	course.id, course.title FROM class
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
        self.parent.i_courses_cb.addItem(str(c[1]), c[0])

    def fill_classes(self, index):
        try:
            course_id = self.parent.i_courses_cb.itemData(index)
            sql = '''
                    SELECT DISTINCT title FROM class
                    WHERE course_id=? AND instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (course_id, self.parent.UUID))
            classes = cur.fetchall()
            self.reset_combox(self.parent.i_classes_cb)
            for c in classes:
                self.add_class(c)
        except Error as e:
            Warning(str(e))
        except Exception as e:
            print(e)

    def add_class(self, c):
        self.parent.i_classes_cb.addItem(c[0])

    # def fill_report(self, location):
    #     try:
    #         row, column = location.row(), location.column()
    #         class_id = self.parent.i_classes_table.item(row, 0).text()
    #         if column == 1:
    #             sql = '''
    #                     SELECT class_id, student_id, status FROM attendance
    #                     WHERE class_id=?;
    #                     '''
    #         elif column == 2:
    #             sql = '''
    #                     SELECT happy, sad, neutral FROM behavior
    #                     WHERE class_id=?;
    #                     '''
    #         else:
    #             return
    #         cur = self.db_conn.cursor()
    #         cur.execute(sql, (class_id,))
    #         records = cur.fetchall()
    #         if column == 1:
    #             self.reset_table(self.parent.i_attendance_table)
    #             for r in records:
    #                 self.parent.i_attendance_table.insertRow(0)
    #                 self.parent.i_attendance_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(r[0])))
    #                 self.parent.i_attendance_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(r[1])))
    #                 checkbox = QtWidgets.QCheckBox()
    #                 checkbox.setChecked(r[2])
    #                 self.parent.i_attendance_table.setCellWidget(0, 2, checkbox)
    #             self.parent.goto(self.parent.i_stacked_widget, self.parent.i_attendance)
    #             self.parent.i_title.setText("View Reports - Attendance")
    #         elif column == 2:
    #             self.reset_table(self.parent.i_behaviour_table)
    #             for r in records:
    #                 self.parent.i_behaviour_table.insertRow(0)
    #                 for i in range(3):
    #                     self.parent.i_behaviour_table.setItem(0, i, QtWidgets.QTableWidgetItem(str(r[i])+"%"))
    #             self.parent.goto(self.parent.i_stacked_widget, self.parent.i_behaviour)
    #             self.parent.i_title.setText("View Reports - Behaviour")
    #     except Exception as e:
    #         print(e)

    def start_recording(self):
        self.parent.disable_btn(self.parent.i_start_session)
        self.parent.enable_btn(self.parent.i_end_session)
        self.parent.goto(self.parent.i_video_sec, self.parent.i_video_holder)

    def reset_combox(self, combobox):
        combobox.clear()

    def save_attendance(self):
        try:
            sql = '''
                    UPDATE attendance
                    SET status = ?
                    WHERE student_id = ?
                    '''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_attendance_table.rowCount()):
                student_id = self.parent.i_attendance_table.item(r, 1).text()
                status = int(self.parent.i_attendance_table.cellWidget(r, 2).isChecked())
                cur.execute(sql, (status, student_id))
                self.db_conn.commit()
        except Exception as e:
            Warning(str(e))
            print(e)
