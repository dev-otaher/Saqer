from PyQt5.QtWidgets import QApplication
import sys
from gui import Loading, InstructorDashboard, AdminDashboard

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainwindow = AdminDashboard.AdminDashboard()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
