from PyQt5.QtWidgets import QFrame, QPushButton, QSizePolicy


class IndexBox(QFrame):
    def __init__(self, *args, **kwargs):
        super(IndexBox, self).__init__(*args, **kwargs)

        self.setFrameShadow(QFrame.Raised)
        self.setFrameShape(QFrame.Box)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)


class IndexButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(IndexButton, self).__init__(*args, **kwargs)

        # Set the button minimum size. Width / Height.
        self.setMinimumSize(100, 40)

        # Set size policy.
        # The button's size will not be changed if the
        # window is resized.
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
