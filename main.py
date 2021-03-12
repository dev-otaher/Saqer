from PyQt5.QtWidgets import QApplication
import sys
from gui import Loading, InstructorDashboard, AdminDashboard



try:
    app = QApplication(sys.argv)
    mainwindow = AdminDashboard.AdminDashboard()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
