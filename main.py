from PyQt5.QtWidgets import QApplication
import sys
from gui import Loading, InstructorDashboard



try:
    app = QApplication(sys.argv)
    mainwindow = Loading.Loading()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
