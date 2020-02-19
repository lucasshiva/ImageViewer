import sys

from PyQt5.QtWidgets import QApplication

from imageviewer import __app_name__, __version__
from imageviewer.view import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(__app_name__)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
