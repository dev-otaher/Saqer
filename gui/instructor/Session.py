import pickle
from datetime import datetime
from os.path import exists
from os.path import sep
from sqlite3 import Error, Connection

from PyQt5.QtGui import QPixmap
from qtpy import QtWidgets

from gui.Success import Success
from gui.Warning import Warning
from modules.VideoThread import VideoThread


def show_alert(msg):
    Warning(msg)

class Session:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn: Connection = self.parent.db.create_db_connection(sep.join(['db', 'saqer.db']))
        self.fill_courses()
        self.vt: VideoThread = None
        self.class_id = None
        self.date_time = str()

    def default_layout(self):
        self.parent.enable_btn(self.parent.i_start_session)
        self.parent.disable_btn(self.parent.i_end_session)
        self.parent.goto(self.parent.i_choices, self.parent.i_view_report_sec)
        self.parent.goto(self.parent.i_stacked_widget, self.parent.i_courses)

    def connect_widgets(self):
        self.parent.i_courses_cb.currentIndexChanged.connect(self.fill_classes)
        self.parent.i_start.clicked.connect(self.start_session)
        self.parent.i_end_session.clicked.connect(self.stop_session)
        self.parent.i_save_recheck.clicked.connect(self.save_attendance)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        self.hide_first_column(self.parent.i_classes_table)
        self.hide_first_column(self.parent.i_courses_table)

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
            with self.db_conn as con:
                courses = con.cursor().execute(sql, (self.parent.UUID,)).fetchall()
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
            with self.db_conn as con:
                classes = con.cursor().execute(sql, (course_id, self.parent.UUID)).fetchall()
                self.reset_combox(self.parent.i_classes_cb)
                for c in classes:
                    self.add_class(c)
        except Error as e:
            Warning(str(e))
        except Exception as e:
            Warning(str(e))
            print(e)

    def add_class(self, c):
        self.parent.i_classes_cb.addItem(c[1], c[0])

    def reset_combox(self, combobox):
        combobox.clear()

    def get_course_code(self):
        sql = '''
                SELECT code FROM course
                WHERE id=?;
                '''
        with self.db_conn as con:
            course_id = self.parent.i_courses_cb.currentData()
            course_code = con.cursor().execute(sql, (course_id,)).fetchall()[0][0]
            return course_code

    def prepare_thread(self):
        proto_path = sep.join(['db', 'model', 'deploy.prototxt'])
        model_path = sep.join(['db', 'model', 'res10_300x300_ssd_iter_140000.caffemodel'])
        embedder_path = sep.join(['db', 'model', 'openface_nn4.small2.v1.t7'])
        behaviour_path = sep.join(['db', 'model', 'epoch_75.hdf5'])
        if not exists(proto_path):
            Warning('Could not find "db/model/deploy.prototxt"!')
            return False
        elif not exists(model_path):
            Warning('Could not find "db/model/res10_300x300_ssd_iter_140000.caffemodel"!')
            return False
        elif not exists(embedder_path):
            Warning('Could not find "db/model/openface_nn4.small2.v1.t7"!')
            return False
        elif not exists(behaviour_path):
            Warning('Could not find "db/model/epoch_75.hdf5"!')
            return False
        else:
            class_title, course_code = self.parent.i_classes_cb.currentText(), self.get_course_code()
            r_path = sep.join(['db', 'courses', course_code, class_title, 'dataset', 'output', 'recognizer.pickle'])
            l_path = sep.join(['db', 'courses', course_code, class_title, 'dataset', 'output', 'labels.pickle'])
            if exists(r_path) and exists(l_path):
                self.vt = VideoThread(
                    sep.join(['video_samples', '1k.mp4']),
                    proto_path,
                    model_path,
                    embedder_path,
                    behaviour_path
                )
                self.vt.image_update.connect(self.update_holder)
                self.vt.std_list.connect(self.fill_recheck_table)
                self.vt.no_cam.connect(show_alert)
                self.vt.no_cam.connect(self.default_layout)
                self.vt.recognizer = pickle.loads(open(r_path, 'rb').read())
                self.vt.label_encoder = pickle.loads(open(l_path, 'rb').read())
                self.vt.isRecord = self.parent.i_save_recording_checkbox.isChecked()
                self.vt.folder_path = sep.join(['db', 'courses', course_code, class_title])
                self.date_time = self.vt.filename = str(datetime.now()).replace(":", ".")
                return True
            else:
                Warning("Recognizer or labels not found!")
                return False

    def start_session(self):
        if self.prepare_thread():
            self.vt.start()
            self.class_id = self.vt.class_id = self.parent.i_classes_cb.currentData()
            self.parent.disable_btn(self.parent.i_start_session)
            self.parent.enable_btn(self.parent.i_end_session)
            self.parent.goto(self.parent.i_video_sec, self.parent.i_video_holder)

    def update_holder(self, frame):
        try:
            # keep updating the label according to the new frame
            self.parent.i_cam_feed.setPixmap(QPixmap.fromImage(frame))
        except Exception as e:
            Warning(str(e))
            print(e)

    def stop_session(self):
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
            Warning(str(e))
            print(e)

    def add_record(self, uni_id, name, appear_counter, checkpoints):
        self.parent.i_recheck_table.insertRow(0)
        self.parent.i_recheck_table.setItem(0, 0, QtWidgets.QTableWidgetItem(uni_id))
        self.parent.i_recheck_table.setItem(0, 1, QtWidgets.QTableWidgetItem(name))
        self.parent.i_recheck_table.setItem(0, 2, QtWidgets.QTableWidgetItem(str(appear_counter) + f"/{checkpoints}"))

    def save_attendance(self):
        try:
            sql = '''
                    INSERT INTO attendance(date_time, student_id, class_id, status)
                    VALUES (?, ?, ?, ?)
                    '''
            b_sql = '''
                        INSERT INTO behavior(class_id, angry, scared, happy, sad, suprised, neutral, date_time) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        '''
            with self.db_conn as con:
                cur = con.cursor()
                for r in range(self.parent.i_recheck_table.rowCount()):
                    student_id = self.parent.i_recheck_table.item(r, 0).text()
                    status = int(self.parent.i_recheck_table.cellWidget(r, 3).isChecked())
                    cur.execute(sql, (self.date_time, student_id, self.class_id, status))
                    con.commit()
                self.parent.enable_btn(self.parent.i_start_session)
                self.parent.disable_btn(self.parent.i_end_session)
                self.parent.goto(self.parent.i_choices, self.parent.i_view_report_sec)
                self.parent.goto(self.parent.i_stacked_widget, self.parent.i_courses)
                parms = (
                            self.class_id,
                            self.vt.emotions[0][1],
                            self.vt.emotions[1][1],
                            self.vt.emotions[2][1],
                            self.vt.emotions[3][1],
                            self.vt.emotions[4][1],
                            self.vt.emotions[5][1],
                            self.date_time
                        )
                cur.execute(b_sql, parms)
                con.commit()
                Success("Attendance & Behaviour Saved!")
        except Exception as e:
            Warning(str(e))
            print(e)
