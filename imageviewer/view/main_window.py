from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QGuiApplication

from imageviewer import __app_name__


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(__app_name__)
        self.resize(QGuiApplication.primaryScreen().availableSize() * 2 / 3)
