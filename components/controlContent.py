from PyQt5 import QtCore, QtGui, QtWidgets


class ControlContent(QtWidgets.QWidget):
    def __init__(self, title="Room", parent=None):
        super().__init__(parent)
        self.setup(title)

    def setup(self, title):
        self.setObjectName("controlContent")

        self.controlContentLayout = QtWidgets.QVBoxLayout(self)
        self.controlContentLayout.setSpacing(0)
        self.controlContentLayout.setObjectName("controlContentLayout")

        # title
        self.title = QtWidgets.QLabel(title, self)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.controlContentLayout.addWidget(self.title)

        # temperature
        self.temperatureWidget = QtWidgets.QWidget(self)
        self.temperatureWidget.setObjectName("temperatureWidget")

        self.temperatureWidgetLayout = QtWidgets.QHBoxLayout(self.temperatureWidget)
        self.temperatureWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.temperatureWidgetLayout.setSpacing(0)
        self.temperatureWidgetLayout.setObjectName("temperatureWidgetLayout")

        temperatureIcon = QtGui.QIcon()
        temperatureIcon.addPixmap(
            QtGui.QPixmap(
                ".\\ui\\controlContent\\..//../resources/icons/thermometer.png"
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )

        self.temperatureIcon = QtWidgets.QPushButton(self.temperatureWidget)
        self.temperatureIcon.setText("")
        self.temperatureIcon.setIcon(temperatureIcon)
        self.temperatureIcon.setIconSize(QtCore.QSize(56, 56))
        self.temperatureIcon.setObjectName("temperatureIcon")
        self.temperatureWidgetLayout.addWidget(self.temperatureIcon)

        self.temperatureLabel = QtWidgets.QLabel(
            "Temperature : ", self.temperatureWidget
        )
        font.setPointSize(16)
        font.setBold(True)
        self.temperatureLabel.setFont(font)
        self.temperatureLabel.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.temperatureWidgetLayout.addWidget(self.temperatureLabel)

        self.temperatureValue = QtWidgets.QLabel("29* C", self)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.temperatureValue.setFont(font)
        self.temperatureValue.setStyleSheet(
            "background-color: rgb(250, 250, 250);\n"
            "margin: 20px 0px;\n"
            "color: rgb(255, 0, 0);\n"
            "border-radius: 20px;\n"
        )
        self.temperatureValue.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.temperatureValue.setObjectName("temperatureValue")
        self.temperatureWidgetLayout.addWidget(self.temperatureValue)

        self.temperatureWidgetLayout.setStretch(1, 1)
        self.temperatureWidgetLayout.setStretch(2, 1)

        self.controlContentLayout.addWidget(self.temperatureWidget)

        # light widget
        self.lightWidget = QtWidgets.QWidget(self)
        self.lightWidget.setObjectName("lightWidget")

        self.lightWidgetLayout = QtWidgets.QHBoxLayout(self.lightWidget)
        self.lightWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.lightWidgetLayout.setObjectName("lightWidgetLayout")

        lightIcon = QtGui.QIcon()
        lightIcon.addPixmap(
            QtGui.QPixmap(".\\ui\\controlContent\\..//../resources/icons/lamp.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.lightIcon = QtWidgets.QPushButton(self.lightWidget)
        self.lightIcon.setText("")

        self.lightIcon.setIcon(lightIcon)
        self.lightIcon.setIconSize(QtCore.QSize(56, 56))
        self.lightIcon.setObjectName("lightIcon")
        self.lightWidgetLayout.addWidget(self.lightIcon)

        self.lightLabel = QtWidgets.QLabel("Lumière : ", self.lightWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lightLabel.setFont(font)
        self.lightLabel.setObjectName("lightLabel")

        self.lightWidgetLayout.addWidget(self.lightLabel, 0, QtCore.Qt.AlignLeft)

        lightSwitchIcon = QtGui.QIcon()
        lightSwitchIcon.addPixmap(
            QtGui.QPixmap(
                ".\\ui\\controlContent\\..//../resources/icons/switch-on.png"
            ),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.lightSwitch = QtWidgets.QPushButton(self.lightWidget)
        self.lightSwitch.setText("")
        self.lightSwitch.setIcon(lightSwitchIcon)
        self.lightSwitch.setIconSize(QtCore.QSize(64, 64))
        self.lightSwitch.setObjectName("lightSwitch")
        self.lightWidgetLayout.addWidget(self.lightSwitch)
        self.lightWidgetLayout.setStretch(1, 1)

        self.controlContentLayout.addWidget(self.lightWidget)


if __name__ == "__main__":
    pass
