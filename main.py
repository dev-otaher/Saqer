from PyQt5.QtWidgets import QApplication
import sys
from gui import Splash


app = QApplication(sys.argv)
mainwindow = Splash.Loading()
sys.exit(app.exec_())