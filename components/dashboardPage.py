from PyQt5 import QtGui, QtCore, QtWidgets as qtw


class DashboardPage(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

    def setup(self):
        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")

        # title
        self.title = qtw.QLabel("Dahsboard", self)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.mainLayout.addWidget(self.title)

        # container
        self.container = qtw.QWidget(self)
        self.container.setObjectName("container")

        self.mainLayout.addWidget(self.container, 1)
