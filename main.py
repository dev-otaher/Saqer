from PyQt5.QtWidgets import QApplication
import sys
from gui.Login import Login
from gui.admin.AdminDashboard import AdminDashboard
from gui.instructor.InstructorDashboard import InstructorDashboard

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # mainwindow = Login()
        # mainwindow = AdminDashboard()
        mainwindow = InstructorDashboard("2gno0wZNp2apUdtyz3YOJNb4GFl1")
        # mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
