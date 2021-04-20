import sys

from PyQt5.QtWidgets import QApplication

from gui.Login import Login
from gui.Warning import Warning

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        Warning(str(e))
        print(e)
