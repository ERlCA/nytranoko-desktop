from PyQt5 import QtCore, QtGui, QtWidgets


class NoRoomMessageWidget(QtWidgets.QWidget):
    def __init__(self, message, button="", callback=None, parent=None):
        super().__init__(parent)
        self.setup(message, button)
        if callback:
            self.refreshButton.clicked.connect(callback)

    def setup(self, message, button):
        self.setObjectName("noRoomMessageWidget")
        self.resize(380, 200)
        self.setMaximumSize(380, 200)
        self.setMinimumSize(380, 200)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.setStyleSheet(
            "QLabel {\n"
            "    background-color: rgba(0,0,0,0);\n"
            "    color: #fff;\n"
            "    border: none\n;"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    color: #000;\n"
            "    padding: 20px 50px;\n"
            "    background-color: rgb(252,252,252);\n"
            "    border: 2px solid rgba(0,0,0,0);\n"
            "    letter-spacing: 2px;\n"
            "    border-radius: 20px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(255, 159, 3);\n"
            "    color: #fff;\n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: #fa8334;\n"
            "    color: #fff;\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    background-color: #eee;\n"
            "    color: #0e273c;\n"
            "}"
        )
        self.noRoomWidgetLayout = QtWidgets.QVBoxLayout(self)
        self.noRoomWidgetLayout.setContentsMargins(-1, -1, -1, 40)
        self.noRoomWidgetLayout.setObjectName("noRoomWidgetLayout")
        self.message = QtWidgets.QLabel(message, self)
        self.message.setWordWrap(True)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.message.setFont(font)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setObjectName("message")
        self.noRoomWidgetLayout.addWidget(self.message)
        if button != "":
            self.refreshButton = QtWidgets.QPushButton(self)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.refreshButton.setFont(font)
            self.refreshButton.setText(button)
            self.refreshButton.setObjectName("refreshButton")
            self.refreshButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.noRoomWidgetLayout.addWidget(
                self.refreshButton, 0, QtCore.Qt.AlignHCenter
            )
            self.noRoomWidgetLayout.setStretch(1, 1)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, noRoomMessageWidget):
        _translate = QtCore.QCoreApplication.translate
        noRoomMessageWidget.setWindowTitle(_translate("noRoomMessageWidget", "Form"))


if __name__ == "__main__":
    pass
