from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QImage


class ImageView(QGraphicsView):
    """
    A customized QGraphicsView to display images.
    """

    styleshet = """
    border: none;
    """

    def __init__(self):
        super(ImageView, self).__init__()

        self.setStyleSheet(self.styleshet)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.Box)

        scene = QGraphicsScene()
        self.setScene(scene)

    @staticmethod
    def convertToPixmap(filePath: str) -> QPixmap:
        """
        Return a QPixmap from a given path.
        """
        image = QImage(filePath)
        if image.isNull():
            raise ValueError("{} is not a valid image!".format(filePath))

        return QPixmap.fromImage(image)

    def setImage(self, filePath: str) -> None:
        pixmap = self.convertToPixmap(filePath)

        item = QGraphicsPixmapItem()
        item.setPixmap(pixmap)
        item.setTransformationMode(Qt.SmoothTransformation)
        self._update_scene(item, item.boundingRect())

    def _update_scene(self, item, rect):
        self.scene().clear()
        self.scene().addItem(item)
        self.scene().setSceneRect(rect)

        # Center image.
        self.center()

    def center(self):
        """
        Center the current image being displayed.
        """
        rect = self.scene().sceneRect()
        self.centerOn(rect.width() / 2, rect.height() / 2)

    def fitToWindow(self):
        """
        Fit the current image to the window.
        """
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def showNormal(self):
        """
        Show normal sized image.
        """
        # Reset all transformations.
        self.resetTransform()

    def fullscreen(self):
        self.showFullScreen()
