from PyQt5.QtWidgets import QApplication
import sys
from gui.admin.AdminDashboard import AdminDashboard
from gui.admin.OfflineAttendance import OfflineAttendance

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainwindow = AdminDashboard()
        # mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
