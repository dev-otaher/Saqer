from datetime import datetime
from sqlite3 import Error

from PyQt5.QtCore import QModelIndex, QVariant
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy, QPushButton, QComboBox
from qtpy import QtWidgets

from gui.Success import Success
from gui.Warning import Warning
from modules.Students import Students
from modules.VideoThread import VideoThread


class Session:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_courses()
        self.vt = VideoThread("D:/Playground/Python/FaceAttendance - Parallelism/class_videos/1k.mp4",
                              "db/model/deploy.prototxt",
                              "db/model/res10_300x300_ssd_iter_140000.caffemodel",
                              "db/model/openface_nn4.small2.v1.t7",
                              "db/courses/CS 422/L6M3/dataset/output/recognizer.pickle",
                              "db/courses/CS 422/L6M3/dataset/output/labels.pickle")
        self.vt.image_update.connect(self.update_holder)
        self.vt.std_list.connect(self.fill_recheck_table)
        self.class_id = None

    def connect_widgets(self):
        self.parent.i_courses_cb.currentIndexChanged.connect(self.fill_classes)
        self.parent.i_start.clicked.connect(self.start_session)
        self.parent.i_end_session.clicked.connect(self.stop_session)
        self.parent.i_save_recheck.clicked.connect(self.save_attendance)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        self.hide_first_column(self.parent.i_classes_table)
        self.hide_first_column(self.parent.i_courses_table)
        # self.hide_first_column(self.parent.i_recheck_table)

    def hide_first_column(self, table):
        table.setColumnHidden(0, True)
        table.setColumnHidden(0, True)

    def fill_courses(self):
        try:
            sql = '''
                    SELECT DISTINCT	course.id, course.title FROM course
                    INNER JOIN class ON class.course_id == course.id
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
                    SELECT DISTINCT id, title FROM class
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
        self.parent.i_classes_cb.addItem(c[1], c[0])

    def reset_combox(self, combobox):
        combobox.clear()

    def start_session(self):
        self.parent.disable_btn(self.parent.i_start_session)
        self.parent.enable_btn(self.parent.i_end_session)
        self.parent.goto(self.parent.i_video_sec, self.parent.i_video_holder)
        self.class_id = self.vt.class_id = self.parent.i_classes_cb.currentData()
        self.vt.isRecordChecked = self.parent.i_save_recording_checkbox.isChecked()
        self.vt.start()

    def update_holder(self, frame):
        try:
            # keep updating the label according to the new frame
            self.parent.i_cam_feed.setPixmap(QPixmap.fromImage(frame))
        except Exception as e:
            print(e.args)

    def stop_session(self):
        # self.parent.i_cam_feed.setPixmap(QPixmap(1,0))
        self.vt.threadActive = False
        self.vt.quit()

    def reset_table(self):
        self.parent.i_recheck_table.clearContents()
        self.parent.i_recheck_table.setRowCount(0)

    def show_recheck_table(self):
        self.reset_table()
        self.parent.i_recheck_table.setHidden(False)
        self.parent.i_save_recheck.setHidden(False)

    def fill_recheck_table(self, taker):
        self.show_recheck_table()
        try:
            checkpoints = taker.checkpoints
            for std in taker.students:
                self.add_record(std.uni_id, std.name, std.appear_counter, checkpoints)
                checkbox = QtWidgets.QCheckBox()
                is_present = std.appear_counter / checkpoints > 0.7
                checkbox.setChecked(is_present)
                self.parent.i_recheck_table.setCellWidget(0, 3, checkbox)
        except Exception as e:
            print(e)

    def add_record(self, uni_id, name, appear_counter, checkpoints):
        self.parent.i_recheck_table.insertRow(0)
        self.parent.i_recheck_table.setItem(0, 0, QtWidgets.QTableWidgetItem(uni_id))
        self.parent.i_recheck_table.setItem(0, 1, QtWidgets.QTableWidgetItem(name))
        self.parent.i_recheck_table.setItem(0, 2,QtWidgets.QTableWidgetItem(str(appear_counter) + f"/{checkpoints}"))

    def save_attendance(self):
        try:
            date_time = str(datetime.now())
            sql = '''
                    INSERT INTO attendance(date_time, student_id, class_id, status)
                    VALUES (?, ?, ?, ?)
                    '''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_recheck_table.rowCount()):
                student_id = self.parent.i_recheck_table.item(r, 0).text()
                status = int(self.parent.i_recheck_table.cellWidget(r, 3).isChecked())
                cur.execute(sql, (date_time, student_id, self.class_id, status))
                self.db_conn.commit()
            self.parent.enable_btn(self.parent.i_start_session)
            self.parent.disable_btn(self.parent.i_end_session)
            self.parent.goto(self.parent.i_choices, self.parent.i_view_report_sec)
            self.parent.goto(self.parent.i_stacked_widget, self.parent.i_courses)
            Success("Attendance Saved!")
        except Exception as e:
            Warning(str(e))
            print(e)
