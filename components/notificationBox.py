from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal


class NotificationBox(qtw.QFrame):
    update_light_count = pyqtSignal(int)

    def __init__(self, parent=None):
        self.flameIcon = self.loadIcon("fire")
        self.gasIcon = self.loadIcon("gas")
        self.dangerIcon = self.loadIcon("danger")
        self.personIcon = self.loadIcon("motion-sensor")
        self.lightIcon = self.loadIcon("lamp")
        self.homeIcon = self.loadIcon("home-safe")
        super().__init__(parent)

        self.setup()

        # connectiong signal
        self.update_light_count.connect(self.updateLightCountHandler)

    def setup(self):
        self.notificationBoxLayout = qtw.QHBoxLayout(self)
        self.notificationBoxLayout.setContentsMargins(0, 0, 50, 0)
        self.notificationBoxLayout.setSpacing(0)
        self.setStyleSheet(
            """
            """
        )
        # Icon box
        self.iconBox = qtw.QWidget(self)
        self.iconBox.setStyleSheet("background-color: rbga(0,0,0,0)")
        self.iconBoxLayout = qtw.QHBoxLayout(self.iconBox)
        self.iconBoxLayout.setContentsMargins(10, 10, 0, 10)
        self.iconBoxLayout.setSpacing(10)
        self.notificationBoxLayout.addWidget(self.iconBox, 0, QtCore.Qt.AlignLeft)

        # icon for different notification
        self.flame = qtw.QPushButton(self.iconBox)
        self.flame.setText("")
        self.flame.setDisabled(True)
        self.flame.setIcon(self.flameIcon)
        self.flame.setIconSize(QtCore.QSize(56, 56))
        self.flame.setStyleSheet("background-color: rgba(0,0,0,0)")
        self.iconBoxLayout.addWidget(self.flame)
        #
        self.gas = qtw.QPushButton(self.iconBox)
        self.gas.setText("")
        self.gas.setDisabled(True)
        self.gas.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.gas.setIcon(self.gasIcon)
        self.gas.setIconSize(QtCore.QSize(56, 56))
        self.iconBoxLayout.addWidget(self.gas)
        #
        self.pirSensor = qtw.QPushButton(self.iconBox)
        self.pirSensor.setText("")
        self.pirSensor.setDisabled(True)
        self.pirSensor.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.pirSensor.setIcon(self.personIcon)
        self.pirSensor.setIconSize(QtCore.QSize(56, 56))
        self.iconBoxLayout.addWidget(self.pirSensor)
        # light icon
        self.lightBox = qtw.QWidget(self.iconBox)
        self.lightBox.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.lightBoxLayout = qtw.QHBoxLayout(self.lightBox)
        self.lightBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.lightBoxLayout.setSpacing(0)
        self.iconBoxLayout.addWidget(self.lightBox)
        self.light = qtw.QPushButton(self.lightBox)
        self.light.setText("")
        self.light.setDisabled(True)
        self.light.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.light.setIcon(self.lightIcon)
        self.light.setIconSize(QtCore.QSize(56, 56))
        self.lightBoxLayout.addWidget(self.light)
        self.lightCount = qtw.QLabel("0", self.lightBox)
        fontLight = QtGui.QFont()
        fontLight.setPointSize(20)
        fontLight.setBold(True)
        self.lightCount.setStyleSheet("color: #FFC107")
        self.lightCount.setFont(fontLight)
        self.lightBoxLayout.addWidget(self.lightCount, alignment=QtCore.Qt.AlignTop)

        # notification message box
        self.messageBox = qtw.QWidget(self)
        self.messageBox.setStyleSheet("background-color: rbga(0,0,0,0)")
        self.messageBoxLayout = qtw.QHBoxLayout(self.messageBox)
        self.messageBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.messageBoxLayout.setSpacing(0)
        self.notificationBoxLayout.addWidget(self.messageBox)

        # message with icon
        self.messageIcon = qtw.QPushButton(self.messageBox)
        self.messageIcon.setText("")
        self.messageIcon.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
        self.messageIcon.setIcon(self.homeIcon)
        self.messageIcon.setIconSize(QtCore.QSize(56, 56))
        self.messageBoxLayout.addWidget(self.messageIcon, 0, QtCore.Qt.AlignRight)
        #
        self.messageLabel = qtw.QLabel(
            "Ceci est une notisafjlkasjflasjfasfication", self.messageBox
        )
        self.messageLabel.setStyleSheet("color: #fff")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.messageLabel.setFont(font)
        self.messageBoxLayout.addWidget(self.messageLabel)

    def updateLightCountHandler(self, count):
        if count <= 0:
            self.light.setDisabled(True)
        else:
            self.light.setDisabled(False)
        self.lightCount.setText(str(count))

    def loadIcon(self, iconName):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f"resources/icons/{iconName}.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        return icon
