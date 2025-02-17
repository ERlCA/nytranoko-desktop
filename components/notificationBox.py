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

        iconTimer = 7000
        self.pirMessageTimer = QTimer()
        self.pirMessageTimer.setInterval(1000)
        self.pirMessageTimer.timeout.connect(self.pirMessageHandler)
        self.pirIconTimer = QTimer()
        self.pirIconTimer.setInterval(iconTimer)
        self.pirMaxBlink = 10
        self.pirIconTimer.timeout.connect(self.pirIconHandler)

        self.flameMessageTimer = QTimer()
        self.flameMessageTimer.setInterval(1000)
        self.flameMessageTimer.timeout.connect(self.flameMessageHandler)
        self.flameIconTimer = QTimer()
        self.flameIconTimer.setInterval(iconTimer)
        self.flameIconTimer.timeout.connect(self.flameIconHandler)
        self.flameMaxBlink = 10

        self.gasMessageTimer = QTimer()
        self.gasMessageTimer.setInterval(1000)
        self.gasMessageTimer.timeout.connect(self.gasMessageHandler)
        self.gasIconTimer = QTimer()
        self.gasIconTimer.setInterval(iconTimer)
        self.gasIconTimer.timeout.connect(self.gasIconHandler)
        self.gasMaxBlink = 10

        self.dangerMessageTimer = QTimer()
        self.dangerMessageTimer.setInterval(1000)
        self.dangerMessageTimer.timeout.connect(self.dangerMessageHandler)
        self.dangerBlink = 10

        self.activeSensor = dict()
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
            self.dangerMessageTimer.stop()
            self.updateMessageNotification("unsafe")

    def updateSensorNotification(
        self, device, sensorValue, isAlarmOn=True
    ):  # NOTE - alarm is on, and only dealing with values > 0

        mode = self.messageLabel.objectName()
        if sensorValue > 0:
            self.activeSensor[device] = sensorValue

            if device == "pir":
                self.pirState = sensorValue
                if self.pirIconTimer.isActive():
                    self.pirIconTimer.stop()
                if self.pirMessageTimer.isActive():
                    self.pirMessageTimer.stop()

                self.pirSensor.setDisabled(False)
                self.pirIconTimer.start()
                if mode == "safe":
                    self.updateMessageNotification("pir")

            elif device == "flame":
                self.flameState = sensorValue
                if self.flameIconTimer.isActive():
                    self.flameIconTimer.stop()
                if self.flameMessageTimer.isActive():
                    self.flameMessageTimer.stop()

                if mode == "safe":
                    self.updateMessageNotification("flame")
                self.flame.setDisabled(False)
                self.flameIconTimer.start()
            if device == "gas":
                self.gasState = sensorValue
                if self.gasIconTimer.isActive():
                    self.gasIconTimer.stop()
                if self.gasMessageTimer.isActive():
                    self.gasMessageTimer.stop()
                if mode == "safe":
                    self.updateMessageNotification("gas")
                self.gas.setDisabled(False)
                self.gasIconTimer.start()

            if not isAlarmOn:
                self.updateMessageNotification("unsafe")
                return

            self.dangerMessageTimer.start()

    def dangerMessageHandler(self):
        mode = self.messageLabel.objectName()
        pir = 0
        flame = 0
        gas = 0
        count = len([x for x in self.activeSensor.values() if x == 1])
        if "pir" in self.activeSensor:
            pir = self.activeSensor["pir"]
        if "flame" in self.activeSensor:
            flame = self.activeSensor["flame"]
        if "gas" in self.activeSensor:
            gas = self.activeSensor["gas"]
        # print(f"pir : {pir} | flame : {flame} | gas : {gas} | count : {count}")

        if count == 1:
            if mode != "safe":
                self.updateMessageNotification("safe")
            if mode == "safe":
                if pir == 1:
                    self.updateMessageNotification("pir")
                elif flame == 1:
                    self.updateMessageNotification("flame")
                elif gas == 1:
                    self.updateMessageNotification("gas")
                else:
                    self.updateMessageNotification("safe")
        elif count == 2:
            if pir == 0:
                if mode != "gas":
                    self.updateMessageNotification("gas")
                elif mode != "flame":
                    self.updateMessageNotification("flame")
            elif flame == 0:
                if mode != "gas":
                    self.updateMessageNotification("gas")
                elif mode != "pir":
                    self.updateMessageNotification("pir")
            elif gas == 0:
                if mode != "flame":
                    self.updateMessageNotification("flame")
                elif mode != "pir":
                    self.updateMessageNotification("pir")
            else:
                self.updateMessageNotification("safe")
        elif count == 3:
            if mode != "gas":
                self.updateMessageNotification("gas")
            elif mode != "flame":
                self.updateMessageNotification("flame")

    def flameIconHandler(self):
        self.flame.setDisabled(True)
        self.flameIconTimer.stop()
        self.activeSensor["flame"] = 0
        if self.messageLabel.objectName() == "unsafe":
            return
        if not (self.pirIconTimer.isActive() and self.gasIconTimer.isActive()):
            self.updateMessageNotification("safe")

    def gasIconHandler(self):
        self.gas.setDisabled(True)
        self.gasIconTimer.stop()
        self.activeSensor["gas"] = 0
        if self.messageLabel.objectName() == "unsafe":
            return
        if not (self.pirIconTimer.isActive() and self.flameIconTimer.isActive()):
            self.updateMessageNotification("safe")

    def pirIconHandler(self):
        self.pirSensor.setDisabled(True)
        self.pirIconTimer.stop()
        self.activeSensor["pir"] = 0
        if self.messageLabel.objectName() == "unsafe":
            return
        if not (self.gasIconTimer.isActive() and self.flameIconTimer.isActive()):
            self.updateMessageNotification("safe")

    def updateMessageNotification(self, name):
        self.messageLabel.setObjectName(name)
        self.messageLabel.setText(self.messageList[name][1])
        self.messageIcon.setIcon(self.messageList[name][0])

    def loadIcon(self, iconName):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f"resources/icons/{iconName}.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        return icon
