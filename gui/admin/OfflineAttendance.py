from multiprocessing import Pipe
from sqlite3 import Error
from typing import List

from PyQt5.QtWidgets import QFileDialog
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

    def connect_widgets(self):
        self.parent.i_choose_video.clicked.connect(self.choose_video)
        self.parent.i_start.clicked.connect(self.start_offline_attendance)
        self.parent.i_save_recheck.clicked.connect(self.save_data)

    def hide_widgets(self):
        self.parent.i_video_note.setHidden(True)
        self.parent.i_progress_label.setHidden(True)
        self.parent.i_progress_bar.setHidden(True)
        self.parent.i_recheck_table.setHidden(True)
        self.parent.i_save_recheck.setHidden(True)

    def choose_video(self):
        video_path = QFileDialog.getOpenFileName(self.parent, 'Choose Video...', '', 'Video (*.mp4 , *.mkv , *.MOV)')
        self.parent.i_video_path.setText(video_path[0])

    def set_bar_max(self, val):
        self.parent.i_progress_bar.setMaximum(val)

    def start_offline_attendance(self):
        try:
            self.parent.i_video_note.setHidden(True)
            path = self.parent.i_video_path.text()
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
        self.parent.i_recheck_table.setColumnWidth(0, 212)
        self.parent.i_recheck_table.setColumnWidth(1, 212)
        self.parent.i_recheck_table.setColumnWidth(2, 212)
        self.parent.i_recheck_table.setColumnWidth(3, 212)
        self.parent.i_recheck_table.clearContents()
        self.parent.i_recheck_table.setRowCount(0)

    def show_recheck_table(self):
        self.reset_table()
        self.parent.i_recheck_table.setHidden(False)

    def fill_recheck_table(self):
        self.show_recheck_table()
        for std in self.students:
            self.parent.i_recheck_table.insertRow(0)
            self.parent.i_recheck_table.setItem(0, 0, QtWidgets.QTableWidgetItem(std.uni_id))
            self.parent.i_recheck_table.setItem(0, 1, QtWidgets.QTableWidgetItem(std.name))
            self.parent.i_recheck_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(std.appear_counter)))
            checkbox = QtWidgets.QCheckBox()
            check_state: bool = std.appear_counter/self.parent.i_progress_bar.maximum() > 0.8
            checkbox.setChecked(check_state)
            self.parent.i_recheck_table.setCellWidget(0, 3, checkbox)

    def save_data(self):
        try:
            sql = '''INSERT INTO attendance (student_id, status)
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
