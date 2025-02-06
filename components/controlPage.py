from PyQt5 import QtGui, QtCore, QtWidgets as qtw
from components.controlContent import ControlContent

# fake json
items = ["cuisine", "chambre", "sdf", "wer", "fdbd"]


class ControlPage(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

        self.addRooms()

    def setup(self):
        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")

        # title
        self.title = qtw.QLabel("Control", self)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.mainLayout.addWidget(self.title)

        # setting scrollArea
        self.scrollArea = qtw.QScrollArea(self)
        self.scrollArea.setFrameShape(qtw.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaContainer = qtw.QWidget()
        self.scrollAreaContainer.setObjectName("scrollAreaContainer")
        self.scrollAreaContainerLayout = qtw.QGridLayout(self.scrollAreaContainer)
        self.scrollAreaContainerLayout.setObjectName("scrollAreaContainerLayout")

        # scrollArea needs a widget as container to its elements
        self.container = qtw.QWidget(self.scrollAreaContainer)
        self.container.setObjectName("container")
        self.containerLayout = qtw.QGridLayout(self.container)
        self.containerLayout.setContentsMargins(0, 0, 0, 0)
        self.containerLayout.setSpacing(10)
        self.containerLayout.setObjectName("containerLayout")

        self.scrollAreaContainerLayout.addWidget(self.container, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaContainer)
        self.mainLayout.addWidget(self.scrollArea)

    def addRooms(self):
        if len(items) <= 3:
            self.containerLayout.setColumnStretch(1, 2)
            self.containerLayout.setColumnStretch(2, 3)

        for index, item in enumerate(items):
            row = index // 3
            column = index % 3

            wrapper = qtw.QWidget()
            wrapper.resize(300, 300)
            wrapper.setMinimumSize(QtCore.QSize(300, 300))
            wrapper.setMaximumSize(QtCore.QSize(300, 300))
            wrapperLayout = qtw.QVBoxLayout(wrapper)
            wrapperLayout.setContentsMargins(0, 0, 0, 0)
            wrapper.setStyleSheet(
                "QWidget {\n"
                "    border-radius: 20px;\n"
                "    background-color: rgb(48, 108, 149);\n"
                "    color: #fff;\n"
                "    border: none;\n"
                "}\n"
                "\n"
            )
            widget = ControlContent(item)
            wrapperLayout.addWidget(widget)

            self.containerLayout.addWidget(
                wrapper, row, column, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
            )
