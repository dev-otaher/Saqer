from PyQt5.QtGui import QPixmap, QColor

from modules.RegisterThread import RegisterThread


class RegisterStudent:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.thread = RegisterThread(0)
        self.hide_widgets()
        self.connect_widgets()

    def connect_widgets(self):
        self.parent.i_open_cam.clicked.connect(self.start_cam)
        self.parent.i_stop_cam.clicked.connect(self.stop_cam)
        self.thread.image_update.connect(self.update_holder)

    def hide_widgets(self):
        self.parent.i_id_note.setHidden(True)
        self.parent.i_name_note.setHidden(True)

    def start_cam(self):
        self.thread.start()

    def stop_cam(self):
        self.thread.threadActive = False

    def update_holder(self, frame):
        try:
            # keep updating the label according to the new frame
            self.parent.i_cam_feed.setPixmap(QPixmap.fromImage(frame))
        except Exception as e:
            print(e)

