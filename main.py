from PyQt5.QtWidgets import QApplication
import sys
from gui import Splash

try:
    app = QApplication(sys.argv)
    mainwindow = Splash.Loading()
    sys.exit(app.exec_())
except Exception as e:
    print(e)
