from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QSizePolicy, QWidget,
                             QAction)
from PyQt5.QtGui import QGuiApplication, QPalette
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupMenuBar()
        self.setupUi()

    def setupUi(self):
        self.resize(QGuiApplication.primaryScreen().availableSize() * 2 / 3)

        # Create a label to display the images.
        self.imageLabel = QLabel(
            "Press Ctrl+O or click on 'File' to select an image!")
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setAlignment(Qt.AlignCenter)

        # Create the index area.
        # Button - Text - Button

        # A frame to draw a line around the layout.
        frame = QFrame()
        frame.setFrameShadow(QFrame.Raised)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.buttonPrevious = QPushButton("Previous")
        self.buttonPrevious.setMinimumSize(100, 40)
        self.buttonPrevious.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.labelIndex = QLabel()
        self.labelIndex.setAlignment(Qt.AlignCenter)

        self.buttonNext = QPushButton("Next")
        self.buttonNext.setMinimumSize(100, 40)
        self.buttonNext.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        frameLayout = QHBoxLayout()
        frameLayout.addWidget(self.buttonPrevious)
        frameLayout.addWidget(self.labelIndex)
        frameLayout.addWidget(self.buttonNext)

        frame.setLayout(frameLayout)

        # Create and add widgets to the main layout.
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.imageLabel)
        mainLayout.addWidget(frame)

        # Create central widget.
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def setupMenuBar(self):
        openFileAct = QAction("&Open file..", self)
        openFileAct.setShortcut("Ctrl+O")
        openFileAct.setToolTip("Select an image")

        openDirAct = QAction("&Choose directory..", self)
        openDirAct.setShortcut("Ctrl+D")
        openDirAct.setToolTip("Choose a directory instead of a file")

        exitAct = QAction("&Exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setToolTip("Close the application..")

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(openFileAct)
        fileMenu.addAction(openDirAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
