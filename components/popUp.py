from PyQt5 import QtCore, QtGui, QtWidgets


class CloseAppWidget(QtWidgets.QDialog):
    def __init__(self, message="Voulez-vous fermer l'application", parent=None):
        super(CloseAppWidget, self).__init__(parent)
        self.message = message
        self.setup(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def setup(self, closeAppWidget):
        closeAppWidget.setObjectName("closeAppWidget")
        closeAppWidget.resize(360, 140)
        closeAppWidget.setStyleSheet(
            "#closeAppWidget {\n"
            "    background-color: #0e273c;\n"
            "    border: 2px solid rgb(255, 159, 3); \n"
            "}\n"
            "\n"
            "QLabel {\n"
            "    color: #fff\n"
            "}\n"
            "QPushButton {\n"
            "    padding: 10px 0;\n"
            "    border-radius: 10px;\n"
            "    background-color: rgb(252,252,252);\n"
            "    color: #0e273c\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color:rgb(255, 159, 3);\n"
            "    color: #fff;\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            ""
        )
        self.closeAppWidgetLayout = QtWidgets.QVBoxLayout(closeAppWidget)
        self.closeAppWidgetLayout.setObjectName("closeAppWidgetLayout")
        self.text = QtWidgets.QLabel(closeAppWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.text.setFont(font)
        self.text.setStyleSheet("")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setObjectName("text")
        self.closeAppWidgetLayout.addWidget(self.text)
        self.buttonWidget = QtWidgets.QWidget(closeAppWidget)
        self.buttonWidget.setObjectName("buttonWidget")
        self.buttonWidgetLayout = QtWidgets.QHBoxLayout(self.buttonWidget)
        self.buttonWidgetLayout.setObjectName("buttonWidgetLayout")
        self.yesButton = QtWidgets.QPushButton(self.buttonWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.yesButton.setFont(font)
        self.yesButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.yesButton.setObjectName("yesButton")
        self.buttonWidgetLayout.addWidget(self.yesButton)
        self.cancelButton = QtWidgets.QPushButton(self.buttonWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cancelButton.setFont(font)
        self.cancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cancelButton.setObjectName("cancelButton")
        self.buttonWidgetLayout.addWidget(self.cancelButton)
        self.closeAppWidgetLayout.addWidget(self.buttonWidget)

        self.retranslateUi(closeAppWidget)
        QtCore.QMetaObject.connectSlotsByName(closeAppWidget)
        self.yesButton.clicked.connect(closeAppWidget.accept)
        self.cancelButton.clicked.connect(closeAppWidget.reject)

    def retranslateUi(self, closeAppWidget):
        _translate = QtCore.QCoreApplication.translate
        closeAppWidget.setWindowTitle(_translate("closeAppWidget", "Form"))
        self.text.setText(_translate("closeAppWidget", self.message))
        self.yesButton.setText(_translate("closeAppWidget", "Oui"))
        self.cancelButton.setText(_translate("closeAppWidget", "Annuler"))


if __name__ == "__main__":
    pass
