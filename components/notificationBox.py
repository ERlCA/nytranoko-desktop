from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QTimer


class NotificationBox(qtw.QFrame):
    update_light_count = pyqtSignal(int)

    def __init__(self, parent=None):
        self.flameIcon = self.loadIcon("fire")
        self.gasIcon = self.loadIcon("gas")
        self.dangerIcon = self.loadIcon("danger")
        self.personIcon = self.loadIcon("motion-sensor")
        self.lightIcon = self.loadIcon("lamp")
        self.homeIcon = self.loadIcon("home-safe")
        self.circle = self.loadIcon("circle-red")
        self.homeRedIcon = self.loadIcon("home-not-safe")
        super().__init__(parent)

        self.messageList = {
            "safe": (
                self.homeIcon,
                'Vous êtes en sécurité avec l\'application "nyTranoko".',
            ),
            "unsafe": (
                self.homeRedIcon,
                "Vous n'êtes pas protégé, le système d'alarme est désactivé.",
            ),
            "flame": (self.dangerIcon, "Attention, risque d'incendie."),
            "gas": (self.dangerIcon, "Attention, risque d'une fuite de gaz."),
            "pir": (self.circle, "Une présence a été détectée."),
        }

        self.pirMessageTimer = QTimer()
        self.pirMessageTimer.setInterval(1000)
        self.pirMessageTimer.timeout.connect(self.pirMessageHandler)
        self.pirIconTimer = QTimer()
        self.pirIconTimer.setInterval(7000)
        self.pirIconBlink = 1
        self.maxBlink = 10
        self.pirIconTimer.timeout.connect(self.pirIconHandler)

        self.dangerTimer = QTimer()
        self.dangerTimer.setInterval(1000)
        self.dangerTimer.timeout.connect(self.dangerHandler)

        self.activeSensor = set()
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
        self.messageLabel = qtw.QLabel(self.messageList["safe"][1], self.messageBox)
        self.messageLabel.setObjectName("safe")
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

    def alarmActivate(self, isAlarmOn):
        mode = self.messageLabel.objectName()
        if not mode in ["flame", "gas", "pir"]:
            self.updateMessageNotification("safe")
        if not isAlarmOn:
            self.pirMessageTimer.stop()
            self.dangerTimer.stop()
            self.updateMessageNotification("unsafe")

    def updateSensorNotification(
        self, device, sensorValue, isAlarmOn=True
    ):  # NOTE - alarm is on

        mode = self.messageLabel.objectName()
        if device == "pir":
            if self.pirIconTimer.isActive():
                self.pirIconTimer.stop()
            if self.pirMessageTimer.isActive():
                self.pirMessageTimer.stop()

            if sensorValue == 0:
                self.pirSensor.setDisabled(True)
            else:
                self.pirSensor.setDisabled(False)
                self.pirIconTimer.start()
                if mode in ["safe", "pir"]:
                    self.updateMessageNotification("pir")
                    self.pirMessageTimer.start()

        elif device == "flame" or device == "gas":
            if sensorValue == 0:
                if device in self.activeSensor:
                    self.activeSensor.remove(device)

                if device == "flame":
                    self.flame.setDisabled(True)
                elif device == "gas":
                    self.gas.setDisabled(True)
            else:
                if device not in self.activeSensor:
                    self.activeSensor.add(device)

                if device == "flame":
                    self.flame.setDisabled(False)
                elif device == "gas":
                    self.gas.setDisabled(False)

            if not isAlarmOn:
                return

            if len(self.activeSensor) == 2:
                self.pirMessageTimer.stop()
                if not self.dangerTimer.isActive():
                    self.dangerTimer.start()
            elif len(self.activeSensor) == 1:
                self.pirMessageTimer.stop()
                if self.dangerTimer.isActive():
                    self.dangerTimer.stop()
                if "flame" in self.activeSensor:
                    self.updateMessageNotification("flame")
                elif "gas" in self.activeSensor:
                    self.updateMessageNotification("gas")

            elif len(self.activeSensor) == 0:
                if not self.pirIconTimer.isActive():
                    self.updateMessageNotification("safe")
                if self.dangerTimer.isActive():
                    self.dangerTimer.stop()

    def dangerHandler(self):
        if self.messageLabel.objectName() != "flame":
            self.updateMessageNotification("flame")
        elif self.messageLabel.objectName() != "gas":
            self.updateMessageNotification("gas")

    def updateMessageNotification(self, name):
        self.messageLabel.setObjectName(name)
        self.messageLabel.setText(self.messageList[name][1])
        self.messageIcon.setIcon(self.messageList[name][0])

    def pirIconHandler(self):
        self.pirIconBlink += 1
        if self.pirIconBlink >= 1:
            self.pirSensor.setDisabled(True)
            self.pirIconTimer.stop()

    def pirMessageHandler(self):
        # print("maxBlink : ", self.maxBlink)  # NOTE - debugging
        self.maxBlink -= 1
        mode = self.messageLabel.objectName()
        if mode in ["flame", "gas", "unsafe"] or self.maxBlink <= 0:
            self.pirMessageTimer.stop()
            return
        if not self.pirMessageTimer.isActive() and self.maxBlink > 0:
            self.pirMessageTimer.start()

        if mode == "safe":
            self.updateMessageNotification("pir")
        elif mode == "pir":
            self.updateMessageNotification("safe")

    def loadIcon(self, iconName):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f"resources/icons/{iconName}.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        return icon
