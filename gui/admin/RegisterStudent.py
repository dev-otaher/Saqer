from os.path import exists
from os.path import sep
from sqlite3 import Connection, IntegrityError

from PyQt5.QtGui import QPixmap

from gui.Success import Success
from gui.Warning import Warning
from modules.RegisterThread import RegisterThread


def show_alert(msg):
    Warning(msg)

class RegisterStudent:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.db_conn: Connection = self.parent.db.create_db_connection(sep.join(['db', 'saqer.db']))
        self.thread = RegisterThread(0)
        self.hide_widgets()
        self.connect_widgets()

    def connect_widgets(self):
        self.parent.i_open_cam.clicked.connect(self.start_cam)
        self.parent.i_stop_cam.clicked.connect(self.stop_cam)
        self.parent.i_capture.clicked.connect(self.capture)
        self.parent.i_register.clicked.connect(self.register)
        self.thread.image_update.connect(self.update_holder)
        self.thread.no_cam.connect(show_alert)

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
        path = os.path.sep.join(['db', 'dataset', self.parent.i_university_id.text()])
        if not exists(path):
            os.mkdir(path)
        self.thread.save = True

    def register(self):
        try:
            uni_id = self.get_uni_id()
            name = self.get_std_name()
            if uni_id == "":
                self.parent.i_id_note.setHidden(False)
            elif name == "":
                self.parent.i_name_note.setHidden(False)
            else:
                sql = '''
                        INSERT INTO student(uni_id, name)
                        VALUES (?, ?)
                        '''
                with self.db_conn as con:
                    con.cursor().execute(sql, (int(uni_id), name))
                    con.commit()
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
            Warning(str(e))
            print(e)

