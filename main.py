import sys

from PyQt5.QtWidgets import QApplication

from gui.Login import Login

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainwindow = Login()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
