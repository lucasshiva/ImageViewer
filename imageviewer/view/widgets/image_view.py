from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class ImageView(QGraphicsView):
    """
    A customized QGraphicsView to display images.
    """

    # Targets only the image background.
    STYLESHEET = """
    QGraphicsView {
        background: #111;
        border: none;
    }
    """

    def __init__(self):
        super(ImageView, self).__init__()

        self.setStyleSheet(self.STYLESHEET)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scene = QGraphicsScene()
        self.setScene(scene)

    @staticmethod
    def convertToPixmap(filePath: str) -> QPixmap:
        """
        Return an instance of QPixmap from a given path.
        """
        image = QImage(filePath)
        if image.isNull():
            raise ValueError("{} is not a valid image!".format(filePath))

        return QPixmap.fromImage(image)

    def setImage(self, filePath: str) -> None:
        """
        Convert `filaPath` to an instance of QPixmap and add
        it to the scene.
        """
        pixmap = self.convertToPixmap(filePath)

        item = QGraphicsPixmapItem()
        item.setPixmap(pixmap)
        item.setTransformationMode(Qt.SmoothTransformation)
        self._update_scene(item, item.boundingRect())

    def _update_scene(self, item, rect) -> None:
        self.scene().clear()
        self.scene().addItem(item)
        self.scene().setSceneRect(rect)

    def center(self) -> None:
        """
        Center the current image being displayed.
        """
        rect = self.scene().sceneRect()
        self.centerOn(rect.width() / 2, rect.height() / 2)

    def fitToWindow(self) -> None:
        """
        Fit the current image to the window.
        """
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)

    def showNormal(self) -> None:
        """
        Show normal sized image.
        """
        # self.scene().update(self.sceneRect())

        # Reset all transformations.
        self.resetTransform()

        # Align image to the left.
        self.centerOn(0, 0)
