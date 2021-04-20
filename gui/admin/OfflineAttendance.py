from multiprocessing import Pipe
from os import getcwd
from os.path import exists, sep
from sqlite3 import Error
from typing import List

from qtpy import QtWidgets

from gui.Success import Success
from gui.Warning import Warning
from modules.AttendanceThread import AttendanceThread
from modules.DBHelper import DBHelper
from modules.Emitter import Emitter
from modules.Student import Student
from modules.Students import Students


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
        self.db_conn = DBHelper().create_db_connection(sep.join(['db', 'saqer.db']))
        self.fill_instructor_cb()

    def connect_widgets(self):
        self.parent.i_start.clicked.connect(self.start_offline_attendance)
        self.parent.i_save_recheck.clicked.connect(self.save_data)
        self.parent.i_instructor_cb.currentIndexChanged.connect(self.fill_courses_cb)
        self.parent.i_course_cb.currentIndexChanged.connect(self.fill_classes_cb)
        self.parent.i_class_cb.currentIndexChanged.connect(self.fill_dates_cb)

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
        with self.db_conn as con:
            instructors = con.cursor().execute(sql).fetchall()
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
            with self.db_conn as con:
                courses = con.cursor().execute(sql, (instructor_id,)).fetchall()
                self.parent.i_course_cb.clear()
                for c in courses:
                    self.parent.i_course_cb.addItem(c[2], c[0])
        except Exception as e:
            Warning(str(e))
            print(e)

    def fill_classes_cb(self, index):
        try:
            instructor_id = self.parent.i_instructor_cb.currentText()
            course_id = self.parent.i_course_cb.itemData(index)
            sql = '''
                    SELECT DISTINCT id, title FROM class
                    WHERE course_id=? AND instructor_id=?;
                    '''
            with self.db_conn as con:
                classes = con.cursor().execute(sql, (course_id, instructor_id)).fetchall()
                self.parent.i_class_cb.clear()
                for c in classes:
                    self.parent.i_class_cb.addItem(c[1], c[0])
        except Exception as e:
            Warning(str(e))
            print(e)

    def fill_dates_cb(self, index):
        class_id = self.parent.i_class_cb.itemData(index)
        sql = '''
                SELECT DISTINCT date_time FROM attendance
                WHERE class_id=?  
                '''
        with self.db_conn as con:
            dates_times = con.cursor().execute(sql, (class_id,)).fetchall()
            self.parent.i_date_cb.clear()
            for dt in dates_times:
                self.parent.i_date_cb.addItem(dt[0])

    def set_bar_max(self, val):
        self.parent.i_progress_bar.setMaximum(val)

    def get_course_code(self, id):
        sql = '''
                SELECT code FROM course
                WHERE id=?; 
                '''
        with self.db_conn as con:
            course_code = con.cursor().execute(sql, (id,)).fetchall()[0][0]
            return course_code

    def reset_progress_bar(self):
        self.parent.i_progress_label.setHidden(False)
        self.parent.i_progress_bar.setHidden(False)
        self.parent.i_progress_bar.setValue(0)

    def prepare_thread(self, path, code, class_id, class_title):
        self.attendance_thread.max_signal.connect(self.set_bar_max)

        self.attendance_thread.video_path = path
        self.attendance_thread.course_code = code
        self.attendance_thread.class_title = class_title
        self.attendance_thread.get_students(class_id)

    def start_offline_attendance(self):
        try:
            self.parent.i_video_note.setHidden(True)
            course_code = self.get_course_code(self.parent.i_course_cb.currentData())
            class_title = self.parent.i_class_cb.currentText()
            dt = self.parent.i_date_cb.currentText()
            recording_path = sep.join([getcwd(), 'db', 'courses', course_code, class_title, f"{dt}.avi"])
            recognizer_path = sep.join(
                [getcwd(), 'db', 'courses', course_code, class_title, 'dataset', 'output', 'recognizer.pickle'])
            labels_path = sep.join(
                [getcwd(), 'db', 'courses', course_code, class_title, 'dataset', 'output', 'labels.pickle'])
            proto_path = sep.join(['db', 'model', 'deploy.prototxt'])
            model_path = sep.join(['db', 'model', 'res10_300x300_ssd_iter_140000.caffemodel'])
            embedder_path = sep.join(['db', 'model', 'openface_nn4.small2.v1.t7'])
            if not exists(recording_path):
                self.parent.i_video_note.setHidden(False)
            elif not exists(proto_path):
                Warning('Could not find "db/model/deploy.prototxt"!')
            elif not exists(model_path):
                Warning('Could not find "db/model/res10_300x300_ssd_iter_140000.caffemodel"!')
            elif not exists(embedder_path):
                Warning('Could not find "db/model/openface_nn4.small2.v1.t7"!')
            elif not exists(recognizer_path):
                Warning('Could not find "recognizer.pickle"! Train model first!')
            elif not exists(labels_path):
                Warning('Could not find "labels.pickle"! Train model first!')
            else:
                self.reset_table(self.parent.i_recheck_table)
                self.reset_progress_bar()
                self.students.clear()
                self.emitter.start()
                class_id = self.parent.i_class_cb.currentData()
                self.prepare_thread(recording_path, course_code, class_id, class_title)
                self.attendance_thread.start()
        except Exception as e:
            Warning(str(e))
            print(e)

    def update_progress(self, val):
        try:
            self.parent.i_progress_bar.setValue(self.parent.i_progress_bar.value() + val)
        except Exception as e:
            Warning(str(e))
            print(e)

    def combine_std_lists(self, list: List[Student]):
        self.students.extend(list)
        if self.parent.i_progress_bar.value() == self.parent.i_progress_bar.maximum():
            self.parent.i_save_recheck.setHidden(False)
            self.fill_recheck_table()

    def reset_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def show_recheck_table(self):
        self.reset_table(self.parent.i_recheck_table)
        self.parent.i_recheck_table.setHidden(False)

    def fill_recheck_table(self):
        self.show_recheck_table()
        checkpoints = self.parent.i_progress_bar.maximum()
        for std in self.students:
            self.add_record(std.uni_id, std.name, std.appear_counter, checkpoints)
            checkbox = QtWidgets.QCheckBox()
            is_present = std.appear_counter / self.parent.i_progress_bar.maximum() > 0.7
            checkbox.setChecked(is_present)
            self.parent.i_recheck_table.setCellWidget(0, 3, checkbox)

    def add_record(self, uni_id, name, appear_counter, checkpoints):
        self.parent.i_recheck_table.insertRow(0)
        self.parent.i_recheck_table.setItem(0, 0, QtWidgets.QTableWidgetItem(uni_id))
        self.parent.i_recheck_table.setItem(0, 1, QtWidgets.QTableWidgetItem(name))
        self.parent.i_recheck_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(appear_counter) + f"/{checkpoints}"))

    def save_data(self):
        try:
            sql = '''
                    UPDATE attendance
                    SET status = ?
                    WHERE student_id = ? AND class_id = ? AND date_time=?
                    '''
            with self.db_conn as con:
                cur = con.cursor()
                for i in range(self.parent.i_recheck_table.rowCount()):
                    id = self.parent.i_recheck_table.item(i, 0).text()
                    status = self.parent.i_recheck_table.cellWidget(i, 3).isChecked()
                    class_id = self.parent.i_class_cb.currentData()
                    dt = self.parent.i_date_cb.currentText()
                    cur.execute(sql, (status, id, class_id, dt))
                    con.commit()
                self.hide_widgets()
                Success("Attendance Updated!")
        except Error as e:
            Warning(str(e))
            print(e)
        except Exception as e:
            Warning(str(e))
            print(e)
