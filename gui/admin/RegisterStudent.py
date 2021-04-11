import os
from os.path import exists
from sqlite3 import Connection, IntegrityError, Error

from gui.Success import Success
from gui.Warning import Warning
from PyQt5.QtGui import QPixmap

from modules.RegisterThread import RegisterThread


class RegisterStudent:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.db_conn: Connection = self.parent.db.create_db_connection("db/saqer.db")
        self.thread = RegisterThread(0)
        self.hide_widgets()
        self.connect_widgets()

    def connect_widgets(self):
        self.parent.i_open_cam.clicked.connect(self.start_cam)
        self.parent.i_stop_cam.clicked.connect(self.stop_cam)
        self.parent.i_capture.clicked.connect(self.capture)
        self.parent.i_register.clicked.connect(self.register)
        self.thread.image_update.connect(self.update_holder)

    def hide_widgets(self):
        self.parent.i_id_note.setHidden(True)
        self.parent.i_name_note.setHidden(True)

    def get_uni_id(self):
       return self.parent.i_university_id.text()

    def get_std_name(self):
        return self.parent.i_student_name.text()

    def start_cam(self):
        uni_id = self.get_uni_id()
        std_name = self.get_std_name()
        if uni_id == "":
            self.parent.i_id_note.setHidden(False)
        elif std_name == "":
            self.parent.i_name_note.setHidden(False)
        else:
            self.hide_widgets()
            self.thread.uni_id = uni_id
            self.thread.start()

    def stop_cam(self):
        self.thread.threadActive = False

    def capture(self):
        path = f"db/dataset/{self.parent.i_university_id.text()}"
        if not exists(path):
            os.mkdir(path)
        self.thread.save = True

    def connection_is_open(self):
        try:
            self.db_conn.execute("SELECT 1 FROM student LIMIT 1;")
            return True
        except Error:
            return False

    def create_connection(self):
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")

    def register(self):
        try:
            uni_id = self.get_uni_id()
            name = self.get_std_name()
            sql = '''
                    INSERT INTO student(uni_id, name)
                    VALUES (?, ?)
                    '''
            if self.connection_is_open() is False:
                self.create_connection()
            self.db_conn.cursor().execute(sql, (int(uni_id), name))
            self.db_conn.commit()
            Success("Data Saved!")
        except IntegrityError:
            Warning("Student already exists!")
        except Exception as e:
            Warning(str(e))
            print(e)


    def update_holder(self, frame):
        try:
            # keep updating the label according to the new frame
            self.parent.i_cam_feed.setPixmap(QPixmap.fromImage(frame))
        except Exception as e:
            print(e)

