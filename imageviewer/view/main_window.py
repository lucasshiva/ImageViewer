import os

from PyQt5.QtWidgets import (QMainWindow, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QSizePolicy, QWidget,
                             QAction, QFileDialog, QMessageBox)
from PyQt5.QtGui import QGuiApplication, QPalette, QPixmap, QFont
from PyQt5.QtCore import Qt, QDir

from imageviewer.core import SUPPORTED_EXTENSIONS


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Stores all images inside the current image's directory.
        self.dirImages = []

        # Store the current image being displayed.
        self.currentImage = None

        self.setupMenuBar()
        self.setupUi()

    def setupUi(self):
        """
        Setup the application UI.
        """
        self.resize(QGuiApplication.primaryScreen().availableSize() * 2 / 3)

        # Get the system font size
        font = QFont()
        size = font.pointSize()

        # Increase size.
        font.setPointSize(size + 4)

        # Create a label to display the images.
        self.imageLabel = QLabel(
            "Press Ctrl+O to select an image"
            "\nOr choose a directory by pressing Ctrl+D")
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setFont(font)

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
        self.buttonPrevious.setEnabled(False)
        self.buttonPrevious.clicked.connect(self.previousImage)

        self.labelIndex = QLabel()
        self.labelIndex.setAlignment(Qt.AlignCenter)

        self.buttonNext = QPushButton("Next")
        self.buttonNext.setMinimumSize(100, 40)
        self.buttonNext.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.buttonNext.setEnabled(False)
        self.buttonNext.clicked.connect(self.nextImage)

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
        
        # Create the menu bar actions.
        self.createActions()
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.openFileAct)
        fileMenu.addAction(self.openDirAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)
        
        viewMenu = menuBar.addMenu("&View")
        viewMenu.addAction(self.zoomInAct)
        viewMenu.addAction(self.zoomOutAct)
        viewMenu.addSeparator()
        viewMenu.addAction(self.normalSizeAct)
        viewMenu.addAction(self.fitToWindowAct)

    def createActions(self):
        self.openFileAct = QAction("&Open file..", self, shortcut="Ctrl+O")
        self.openFileAct.setToolTip("Select an image")
        self.openFileAct.triggered.connect(self.showFileDialog)

        self.openDirAct = QAction("&Choose directory..", self, shortcut="Ctrl+D")
        self.openDirAct.setToolTip("Choose a directory instead of a file")
        self.openDirAct.triggered.connect(self.showDirDialog)

        self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q")
        self.exitAct.setToolTip("Close the application..")
        self.exitAct.triggered.connect(self.close)
        
        #TODO View actions are disabled for now. 
        # Implement the functionalities later.
        self.zoomInAct = QAction("&Zoom In", self, shortcut="Ctrl++")
        self.zoomInAct.setToolTip("Zoom in")
        
        self.zoomOutAct = QAction("&Zoom Out", self, shortcut="Ctrl+-")
        self.zoomOutAct.setToolTip("Zoom out")
        
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S")
        self.normalSizeAct.setToolTip("Reset zoom level")
        self.normalSizeAct.setEnabled(False)
        
        self.fitToWindowAct = QAction("&Fit Window", self, shortcut="Ctrl+F")
        self.fitToWindowAct.setToolTip("Resize image to fit the current window")
        
        # Disable actions
        self.zoomInAct.setEnabled(False)
        self.zoomOutAct.setEnabled(False)
        self.normalSizeAct.setEnabled(False)
        self.fitToWindowAct.setEnabled(False)

    def showFileDialog(self):
        """
        Open a file dialog that only allows the user to choose image files.
        Only supports .jpg and .png files for now.
        """

        # Transforms the list of extensions in a string
        # Something like: *.jpg *.png
        extensions = "*." + " *.".join(SUPPORTED_EXTENSIONS)

        # Open file dialog.
        # Returns a tuple, first element is the selected path.
        # Second element is the chosen filter.

        filePath = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an image file.",
            directory=os.path.expanduser("~"),
            filter="Image Files ({})".format(extensions),
        )[0]

        if not filePath:
            return

        self.loadImage(filePath)

    def showDirDialog(self):
        """
        Open a directory dialog.
        Also show files, but only directories can be selected.
        """
        path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Choose a directory",
            directory=os.path.expanduser("~"),
            options=QFileDialog.DontUseNativeDialog,
        )

        if not path:
            return

        # Scan the directory.
        self.scanDir(path)
        
        # Check if directory is empty.
        if not self.dirImages:
            QMessageBox.critical(self, "Error!", "No images were found!")
            return
            
        # Load the first image from the directory.
        self.loadImage(self.dirImages[0])

    def loadImage(self, imagePath: str):
        """
        Display image from `imagePath`.
        """

        # Load pixmap
        pixmap = QPixmap(imagePath)

        # Scale to the label's size.
        pixmap = pixmap.scaled(
            self.imageLabel.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # Display image.
        self.imageLabel.setPixmap(pixmap)

        # Store the current image.
        self.currentImage = imagePath

        # Scan the current image's directory.
        self.scanDir(os.path.dirname(self.currentImage))

        # Update the index
        self.updateIndex()

    def scanDir(self, path: str):
        """
        Scan the image's directory.
        """

        # Stores all files inside the directory.
        imageDir = QDir(path)
        imageDir.setFilter(QDir.Files | QDir.NoSymLinks | QDir.Readable)

        # Add files' absolute path to list.
        self.dirImages = [
            file.absoluteFilePath() for file in imageDir.entryInfoList()
            if file.suffix() in SUPPORTED_EXTENSIONS
        ]

    def updateIndex(self):
        index = self.dirImages.index(self.currentImage)
        total = len(self.dirImages)
        fileName = os.path.basename(self.currentImage)

        if index == 0:
            self.buttonPrevious.setEnabled(False)
            self.buttonNext.setEnabled(True)
        elif (index + 1) == total:
            self.buttonPrevious.setEnabled(True)
            self.buttonNext.setEnabled(False)
        else:
            self.buttonPrevious.setEnabled(True)
            self.buttonNext.setEnabled(True)

        text = f"{index + 1} of {total} - {fileName}"
        self.labelIndex.setText(text)

    def nextImage(self):
        index = self.dirImages.index(self.currentImage)
        self.loadImage(self.dirImages[index + 1])

    def previousImage(self):
        index = self.dirImages.index(self.currentImage)
        self.loadImage(self.dirImages[index - 1])
