import os

from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QSizePolicy, QWidget,
                             QAction, QFileDialog)
from PyQt5.QtGui import QGuiApplication, QPalette, QPixmap
from PyQt5.QtCore import Qt, QDir


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Stores all images inside the current image's directory.
        self.dirImages = []

        self.setupMenuBar()
        self.setupUi()

    def setupUi(self):
        """
        Setup the application UI.
        """
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
        """
        Setup the application menu bar.
        """
        openFileAct = QAction("&Open file..", self)
        openFileAct.setShortcut("Ctrl+O")
        openFileAct.setToolTip("Select an image")
        openFileAct.triggered.connect(self.showFileDialog)

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

    def showFileDialog(self):
        """
        Open a file dialog that only allows the user to choose image files.
        Only supports .jpg and .png files for now.
        """
        filePath = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an image file.",
            directory="/home/lucas",
            filter="Image Files (*.jpg *.png)",
        )[0]

        if not filePath:
            return

        self.loadImage(filePath)

    def loadImage(self, imagePath: str):
        """
        Display image from `imagePath`.
        """

        # Load pixmap
        pixmap = QPixmap(imagePath)

        # Scale to the label's size.
        pixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)

        # Display image.
        self.imageLabel.setPixmap(pixmap)

        # Scan image's directory.
        self.scanDir(imagePath)

    def scanDir(self, path: str):
        """
        Scan the image's directory.
        """

        # Stores all files inside the directory.
        imageDir = QDir(os.path.dirname(path))
        imageDir.setFilter(QDir.Files | QDir.NoSymLinks | QDir.Readable)

        # Add files' absolute path to list.
        self.dirImages = [
            file.absoluteFilePath() for file in imageDir.entryInfoList()
        ]
