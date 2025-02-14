from PyQt5 import QtGui, QtCore, QtWidgets as qtw
from components.controlContent import ControlContent
from components.noRoomMessage import NoRoomMessageWidget
from utils.getMethodDb import GetRooms, GetDevices
from utils.websockets import Websockets

# fake json
items = ["cuisine", "chambre", "sdf", "wer", "fdbd"]


class ControlPage(qtw.QWidget):
    quitting_control_page = QtCore.pyqtSignal()
    control_page_requested = QtCore.pyqtSignal()
    rooms_verified = QtCore.pyqtSignal()
    devices_verified = QtCore.pyqtSignal()

    requesting_devices_per_room = QtCore.pyqtSignal(dict)

    # connect signals

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()
        self.ws = Websockets()
        self.devices = None
        self.rooms = None
        self.devicesRoom = None  # devices per room
        self.controlContentList = None
        self.websocketsData = {}
        self.new = True

        # connecting pyqtSignals
        self.rooms_verified.connect(self.performGetDevices)
        self.devices_verified.connect(self.getDevicesPerRoom)
        self.control_page_requested.connect(self.controlContentHandler)
        self.quitting_control_page.connect(self.ws.close_)
        self.ws.websocket_disconnected.connect(self.websocket_disconnected_handler)
        self.ws.websocket_received_message.connect(self.websocket_message_handler)

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

        self.noMessageWidget = None

    def controlContentHandler(self):
        self.new = True
        self.showMessageBox(
            message="En attente pour trouver toutes les salles/chambres."
        )
        # print(f"control content handler : {self.new}")
        if self.new:
            self.ws.connect()

            if self.devicesRoom:
                self.updateControlContent()
            self.performGetRooms()

    def performGetRooms(self):
        self.getRoomsWorker = GetRooms()
        self.getRoomsWorker.room_data_received.connect(self.verifyRooms)
        self.getRoomsWorker.start()

    def performGetDevices(self):
        self.getDevicesWorker = GetDevices()
        self.getDevicesWorker.device_data_received.connect(self.verifyDevices)
        self.getDevicesWorker.start()

    def getDevicesPerRoom(self):
        self.devicesRoom = {}
        for room in self.rooms:
            name = room["name"]
            self.devicesRoom[name] = [
                device
                for device in self.devices
                if device["room_id"] == room["room_id"]
            ]
        self.updateControlContent()

    def updateControlContent(self):
        self.controlContentList = {}
        for i in reversed(range(self.container.layout().count())):
            child = self.container.layout().itemAt(i).widget()
            if child:
                child.deleteLater()
                self.container.layout().removeWidget(child)

        if len(self.devicesRoom) <= 3:
            self.containerLayout.setColumnStretch(1, 2)
            self.containerLayout.setColumnStretch(2, 3)

        index = 0
        for room, devices in self.devicesRoom.items():
            row = index // 3
            column = index % 3

            wrapper = qtw.QWidget()
            wrapper.resize(320, 300)
            wrapper.setMinimumSize(QtCore.QSize(320, 300))
            wrapper.setMaximumSize(QtCore.QSize(320, 300))
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

            widget = ControlContent(
                room=room,
                state=self.websocketsData[room]["state"],
                callback=self.ws.send_message_json,
            )
            self.controlContentList[room] = widget
            wrapperLayout.addWidget(widget)

            self.containerLayout.addWidget(
                wrapper, row, column, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
            )
            index += 1
        self.new = False

    def websocket_disconnected_handler(self):
        self.showMessageBox(button="Actualiser", callback=self.controlContentHandler)

    def verifyRooms(self, res):
        self.rooms = None
        success, data = res["success"], res["data"]
        if not success:
            self.showMessageBox(
                button="Actualiser",
                callback=self.controlContentHandler,
            )
        else:
            self.rooms = data
            self.rooms_verified.emit()

    def verifyDevices(self, res):
        self.devices = None
        success, data = res["success"], res["data"]
        if not success:
            self.showMessageBox(
                button="Actualiser",
                callback=self.controlContentHandler,
            )
        else:
            self.devices = data
            self.devices_verified.emit()

    def showMessageBox(
        self,
        message="Une erreur s'est produite, Veuillez réessayer.",
        button="",
        callback=None,
    ):
        self.containerLayout.setColumnStretch(1, 0)
        self.containerLayout.setColumnStretch(2, 0)
        for i in reversed(range(self.container.layout().count())):
            child = self.container.layout().itemAt(i).widget()
            if child:
                child.deleteLater()
                self.container.layout().removeWidget(child)

        self.noMessageWidget = qtw.QFrame()
        self.noMessageWidget.resize(380, 200)
        self.noMessageWidget.setMaximumSize(380, 200)
        self.noMessageWidget.setMinimumSize(380, 200)
        self.noMessageWidget.setObjectName("noMessageWidget")
        self.noMessageWidget.setStyleSheet(
            """
                    QFrame#noMessageWidget {
                        background-color: #0e273c; 
                        border-radius: 20px;
                        border: 2px solid rgba(0,0,0,0)
                    } 
                    QFrame#noMessageWidget:hover {
                        border: 2px solid rgb(255, 159, 3)
                    }
                """
        )
        self.noMessageWidgetLayout = qtw.QVBoxLayout(self.noMessageWidget)
        self.noMessageWidgetLayout.addWidget(
            NoRoomMessageWidget(message, button, callback), 0
        )
        self.containerLayout.addWidget(
            self.noMessageWidget, 0, 0, QtCore.Qt.AlignCenter
        )

    def websocket_message_handler(self, data):
        room = data["room"]
        if data["device"] == "light":
            state = data["state"]
            self.websocketsData[room] = data
            if not self.new:
                if state == "ON":
                    self.controlContentList[room].lightSwitchToggle(True)
                elif state == "OFF":
                    self.controlContentList[room].lightSwitchToggle(False)
        elif data["device"] == "temperature" and not self.new:
            self.controlContentList[room].temperatureValue.setText(
                f"{str(data["value"])}° C"
            )


if __name__ == "__main__":
    pass
    # if len(items) <= 3:
    #     self.containerLayout.setColumnStretch(1, 2)
    #     self.containerLayout.setColumnStretch(2, 3)

    # for index, item in enumerate(items):
    #     row = index // 3
    #     column = index % 3

    #     wrapper = qtw.QWidget()
    #     wrapper.resize(300, 300)
    #     wrapper.setMinimumSize(QtCore.QSize(300, 300))
    #     wrapper.setMaximumSize(QtCore.QSize(300, 300))
    #     wrapperLayout = qtw.QVBoxLayout(wrapper)
    #     wrapperLayout.setContentsMargins(0, 0, 0, 0)
    #     wrapper.setStyleSheet(
    #         "QWidget {\n"
    #         "    border-radius: 20px;\n"
    #         "    background-color: rgb(48, 108, 149);\n"
    #         "    color: #fff;\n"
    #         "    border: none;\n"
    #         "}\n"
    #         "\n"
    #     )
    #     widget = ControlContent(item)
    #     wrapperLayout.addWidget(widget)

    #     self.containerLayout.addWidget(
    #         wrapper, row, column, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
    #     )
