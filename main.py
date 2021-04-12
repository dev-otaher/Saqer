import sys

from PyQt5.QtWidgets import QApplication

from gui.admin.AdminDashboard import AdminDashboard
from gui.instructor.InstructorDashboard import InstructorDashboard

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # mainwindow = Login()
        # mainwindow = AdminDashboard()
        mainwindow = InstructorDashboard("8z8VnJr5acOIFBsJWcZV1DDH7hW2")
        # mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
