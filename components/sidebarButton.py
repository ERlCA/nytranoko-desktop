from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui, QtCore


class Button(QPushButton):
    def __init__(self, name="Button", iconName="new-house", parent=None, callback=None):
        super().__init__(parent)
        self.setup(name, iconName)
        if callback:
            self.clicked.connect(callback)

    def setup(self, name, iconName):
        self.setText(f" {name}")
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()

        icon.addPixmap(
            QtGui.QPixmap(f"resources/icons/{iconName}.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(32, 32))
