from PyQt5.QtWidgets import QApplication
import sys
from gui.Login import Login
from gui.admin.AdminDashboard import AdminDashboard
from gui.instructor.InstructorDashboard import InstructorDashboard

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # mainwindow = Login()
        mainwindow = AdminDashboard()
        # mainwindow = InstructorDashboard("dYdPh9CTfxOsYvKR26Dc3bkQwB62")
        # mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
