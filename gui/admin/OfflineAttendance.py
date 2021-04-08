import os
import time
from multiprocessing import Pipe
from sqlite3 import Error
from typing import List

from PyQt5.QtWidgets import QFileDialog
from cv2 import cv2
from qtpy import QtWidgets

from modules.AttendanceThread import AttendanceThread
from modules.DBHelper import DBHelper
from modules.Emitter import Emitter
from modules.Student import Student
from modules.Students import Students
from gui.Warning import Warning

class OfflineAttendance:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        child_pipe = Pipe()
        self.attendance_thread = AttendanceThread(child_pipe)
        self.emitter = Emitter(child_pipe)
        self.emitter.update_available.connect(self.update_progress)
        self.emitter.new_list.connect(self.combine_std_lists)
        self.students = Students()
        self.db = DBHelper()
        self.db_conn = DBHelper().create_db_connection("db/saqer.db")
        self.fill_instructor_cb()

    def connect_widgets(self):
        self.parent.i_start.clicked.connect(self.start_offline_attendance)
        self.parent.i_save_recheck.clicked.connect(self.save_data)
        self.parent.i_instructor_cb.currentIndexChanged.connect(self.fill_courses_cb)
        self.parent.i_course_cb.currentIndexChanged.connect(self.fill_classes_cb)

    def hide_widgets(self):
        self.parent.i_video_note.setHidden(True)
        self.parent.i_progress_label.setHidden(True)
        self.parent.i_progress_bar.setHidden(True)
        self.parent.i_recheck_table.setHidden(True)
        self.parent.i_save_recheck.setHidden(True)

    def fill_instructor_cb(self):
        sql = '''
                SELECT DISTINCT instructor_id FROM class;
                '''
        instructors = self.db_conn.cursor().execute(sql).fetchall()
        for inst in instructors:
            self.parent.i_instructor_cb.addItem(inst[0])

    def fill_courses_cb(self, index):
        try:
            instructor_id = self.parent.i_instructor_cb.itemText(index)
            sql = '''
                    SELECT DISTINCT course.id, course.code, course.title FROM course
                    INNER JOIN class ON course.id = class.course_id
                    WHERE class.instructor_id=?;
                    '''
            courses = self.db_conn.cursor().execute(sql, (instructor_id,)).fetchall()
            self.parent.i_course_cb.clear()
            for c in courses:
                self.parent.i_course_cb.addItem(c[2], c[0])
        except Exception as e:
            print(e)

    def fill_classes_cb(self, index):
        try:
            instructor_id = self.parent.i_instructor_cb.currentText()
            course_id = self.parent.i_course_cb.itemData(index)
            sql = '''
                    SELECT DISTINCT title FROM class
                    WHERE course_id=? AND instructor_id=?;
                    '''
            classes = self.db_conn.cursor().execute(sql, (course_id, instructor_id)).fetchall()
            self.parent.i_class_cb.clear()
            for c in classes:
                self.parent.i_class_cb.addItem(c[0])
        except Exception as e:
            print(e)

    def set_bar_max(self, val):
        self.parent.i_progress_bar.setMaximum(val)

    def get_course_code(self, id):
        sql = '''
                SELECT code FROM course
                WHERE id=?; 
                '''
        return self.db_conn.cursor().execute(sql, (id,)).fetchall()[0][0]

    def start_offline_attendance(self):
        try:
            self.parent.i_video_note.setHidden(True)
            course_id = self.parent.i_course_cb.currentData()
            course_code = self.get_course_code(course_id)
            class_title = self.parent.i_class_cb.currentText()
            print(course_code, class_title)
            path = os.getcwd()+f"/db/courses/{course_code}/{class_title}/1k.mp4"
            # vc = cv2.VideoCapture(path)
            # while True:
            #     ret, frame = vc.read()
            #     cv2.imshow("frame", frame)
            #     cv2.waitKey(0)
            # path = "D:/Playground/Python/FaceAttendance - Parallelism/class_videos/1k - 2.MOV"
            if path == "":
                self.parent.i_video_note.setHidden(False)
            else:
                self.reset_table()
                self.parent.i_progress_label.setHidden(False)
                self.parent.i_progress_bar.setHidden(False)
                self.parent.i_progress_bar.setValue(0)
                self.students.clear()
                self.attendance_thread.max_signal.connect(self.set_bar_max)
                self.emitter.start()
                self.attendance_thread.path = path
                self.attendance_thread.start()
        except Exception as e:
            print(e)

    def update_progress(self, val):
        try:
            self.parent.i_progress_bar.setValue(self.parent.i_progress_bar.value() + val)
        except Exception as e:
            print(e)

    def combine_std_lists(self, list: List[Student]):
        self.students.extend(list)
        if self.parent.i_progress_bar.value() == self.parent.i_progress_bar.maximum():
            self.parent.i_save_recheck.setHidden(False)
            self.fill_recheck_table()

    def reset_table(self):
        self.parent.i_recheck_table.clearContents()
        self.parent.i_recheck_table.setRowCount(0)

    def show_recheck_table(self):
        self.reset_table()
        self.parent.i_recheck_table.setHidden(False)

    def fill_recheck_table(self):
        self.show_recheck_table()
        checkpoints = self.parent.i_progress_bar.maximum()
        for std in self.students:
            self.add_record(std.uni_id, std.name, std.appear_counter, checkpoints)
            checkbox = QtWidgets.QCheckBox()
            is_present = std.appear_counter/self.parent.i_progress_bar.maximum() > 0.7
            checkbox.setChecked(is_present)
            self.parent.i_recheck_table.setCellWidget(0, 3, checkbox)

    def add_record(self, uni_id, name, appear_counter, checkpoints):
        self.parent.i_recheck_table.insertRow(0)
        self.parent.i_recheck_table.setItem(0, 0, QtWidgets.QTableWidgetItem(uni_id))
        self.parent.i_recheck_table.setItem(0, 1, QtWidgets.QTableWidgetItem(name))
        self.parent.i_recheck_table.setItem(0, 2,QtWidgets.QTableWidgetItem(str(appear_counter) + f"/{checkpoints}"))

    def save_data(self):
        try:
            sql = '''INSERT INTO attendence (student_id, status)
                            VALUES (?, ?)'''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_recheck_table.rowCount()):
                id = self.parent.i_recheck_table.item(r, 0).text()
                status = self.parent.i_recheck_table.cellWidget(r, 3).isChecked()
                cur.execute(sql, (id, status))
                self.db_conn.commit()
        except Error as e:
            Warning(str(e))
            print(e)
