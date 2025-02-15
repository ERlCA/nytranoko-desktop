from PyQt5 import QtGui, QtCore, QtWidgets as qtw
from utils.getMethodDb import GetRooms, GetDevices
from utils.websockets import Websockets
from components.controlContent import ControlContent
from components.noRoomMessage import NoRoomMessageWidget
from components.header import Header

# fake json
items = ["cuisine", "chambre", "sdf", "wer", "fdbd"]


class ControlPage(qtw.QWidget):
    quitting_control_page = QtCore.pyqtSignal()
    control_page_requested = QtCore.pyqtSignal()
    rooms_verified = QtCore.pyqtSignal()
    devices_verified = QtCore.pyqtSignal()
    retrieving_database_complete = QtCore.pyqtSignal()
    control_page_websocket_message = QtCore.pyqtSignal(dict)

    requesting_devices_per_room = QtCore.pyqtSignal(dict)

    # connect signals

    def __init__(self, callback=None, parent=None):
        super().__init__(parent)
        self.websocketSendMessage = callback if callback else None

        self.setup()
        # self.maintenance_on()

        self.devices = None
        self.rooms = None
        self.devicesRoom = None  # devices per room
        self.controlContentList = None  # stores all instances of control content
        self.websocketsData = {}
        self.new = True

        # # connecting pyqtSignals
        self.control_page_requested.connect(self.controlContentHandler)
        self.control_page_websocket_message.connect(self.websocketMessageHandler)
        self.rooms_verified.connect(self.performGetDevices)
        self.devices_verified.connect(self.getDevicesPerRoom)
        self.retrieving_database_complete.connect(self.updateControlContent)

    def setup(self):
        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 40, 0, 0)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setObjectName("mainLayout")

        # NOTE - The code below may not work, need update
        # container // used in maintenance mode
        # self.container = qtw.QWidget(self)
        # self.container.setStyleSheet("background-color: red")
        # self.container.setObjectName("container")
        # self.containerLayout = qtw.QGridLayout(self.container)
        # self.mainLayout.addWidget(self.container, 1)

        # comment all code below in maintenance mode
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
        # self.container.setStyleSheet("background-color: red")
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
        self.showMessageBox(message="Veuillez patienter pendant la configuration.")

        if self.new and self.devicesRoom:

            self.updateControlContent()
        self.performGetRooms()

    def performGetRooms(self):
        self.getRoomsWorker = GetRooms()
        self.getRoomsWorker.room_data_received.connect(self.verifyRooms)
        self.getRoomsWorker.start()

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

    def performGetDevices(self):
        self.getDevicesWorker = GetDevices()
        self.getDevicesWorker.device_data_received.connect(self.verifyDevices)
        self.getDevicesWorker.start()

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

    def getDevicesPerRoom(self):
        self.devicesRoom = {}
        for room in self.rooms:
            name = room["name"]
            self.devicesRoom[name] = [
                device
                for device in self.devices
                if device["room_id"] == room["room_id"]
            ]
        self.retrieving_database_complete.emit()

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
                callback=self.websocketSendMessage,
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

    def websocketMessageHandler(self, data):
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

    def maintenance_on(self):
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
            NoRoomMessageWidget(
                message="Cette fonctionnalité n'est pas encore disponible.",
            ),
            0,
        )
        self.containerLayout.addWidget(
            self.noMessageWidget, 0, 0, QtCore.Qt.AlignCenter
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
