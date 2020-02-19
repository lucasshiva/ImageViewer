import sys

from PyQt5.QtWidgets import QApplication

from imageviewer.view import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
