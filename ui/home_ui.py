from PyQt5 import QtCore, QtWidgets as qtw
from components.sidebar import Sidebar
from components.controlPage import ControlPage
from components.dashboardPage import DashboardPage
from components.header import Header
from components.notificationBox import NotificationBox
from utils.websockets import Websockets


class Ui_homeWindow(qtw.QWidget):
    logout_requested_from_home = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ws = Websockets()
        self.ws.connect()

        self.temperatureData = {}
        self.lightData = {}
        self.lightOnList = []

        self.setupUi()

        # connection pyqtSignals
        self.ws.websoket_connected.connect(self.websocketConnectedHandler)
        self.ws.websocket_disconnected.connect(self.websocketDisconnectedHandler)
        self.ws.websocket_received_message.connect(self.websocketMessageHandler)

        self.sidebar.logout_requested.connect(self.logout_requested_from_home.emit)
        self.sidebar.control_page_requested.connect(self.controlPageRequesting)
        self.sidebar.dashboard_page_requested.connect(self.dashboardPageRequesting)
        self.controlPage.control_content_rendered.connect(self.controlContentUpdate)
        self.controlPage.control_page_switch_toggled.connect(
            self.lightSwitchToggledHandler
        )

    def setupUi(self):
        self.setObjectName("self")
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        self.setWindowTitle("Home")

        self.homeWindowLayout = qtw.QHBoxLayout(self)
        self.homeWindowLayout.setContentsMargins(10, 10, 10, 10)
        self.homeWindowLayout.setSpacing(10)
        self.homeWindowLayout.setObjectName("homeWindowLayout")
        # self.resize(900, 600)
        # self.setMinimumSize(900, 600)
        # self.setMaximumSize(900, 600)

        # adding sidebar
        self.sidebarContainer = qtw.QWidget(self)
        self.sidebarContainer.setStyleSheet(
            "QWidget {\n"
            "    background-color: #0e273c;\n"
            "    color: #fff;\n"
            "    border-radius: 20px;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    padding: 5px;\n"
            "}\n"
            "\n"
            ""
        )
        self.sidebarContainerLayout = qtw.QGridLayout(self.sidebarContainer)
        self.sidebar = Sidebar()
        self.sidebarContainerLayout.addWidget(self.sidebar)
        self.homeWindowLayout.addWidget(self.sidebarContainer, 0, QtCore.Qt.AlignLeft)

        # ========================================================
        # adding main page
        self.mainWidget = qtw.QFrame(self)
        self.mainWidget.setObjectName("mainWidget")
        # self.mainWidget.setStyleSheet("QFrame{background-color: red};\n")
        self.mainWidgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.mainWidgetLayout.setContentsMargins(0, 40, 0, 0)
        self.mainWidgetLayout.setSpacing(5)
        self.homeWindowLayout.addWidget(self.mainWidget, 1)

        # header
        self.header = Header(title="Dashboard", error=True)
        self.mainWidgetLayout.addWidget(self.header, 0, QtCore.Qt.AlignTop)

        # notification box
        self.notificationBox = NotificationBox(self)
        self.notificationBox.setStyleSheet(
            """
            QFrame {
                background-color:#0e273c;
                border-radius: 20px;
            }
            """
        )
        self.mainWidgetLayout.addWidget(self.notificationBox, 0, QtCore.Qt.AlignTop)

        self.stackedWidget = qtw.QStackedWidget(self.mainWidget)
        # self.stackedWidget.setStyleSheet("background-color:red")
        self.mainWidgetLayout.addWidget(
            self.stackedWidget,
        )

        self.dashboardPage = DashboardPage()
        self.stackedWidget.addWidget(self.dashboardPage)  # add dashboard page
        self.controlPage = ControlPage(callback=self.ws.send_message_json)
        self.stackedWidget.addWidget(self.controlPage)  # add control page

        self.stackedWidget.setCurrentIndex(0)

    def dashboardPageRequesting(self):
        if self.stackedWidget.currentIndex() != 0:
            self.changePage(0)
            self.header.title.setText("Dashboard")

    def controlPageRequesting(self):
        if self.stackedWidget.currentIndex() != 1:
            self.header.title.setText("Control")
            self.changePage(1)
            self.controlPage.control_page_requested.emit()

    def changePage(self, index):
        if self.stackedWidget:
            self.stackedWidget.setCurrentIndex(index)

    # websocket event handler
    def websocketDisconnectedHandler(self):
        self.header.updateHeader(error=True)

    def websocketConnectedHandler(self):
        self.header.updateHeader(error=False)

    def websocketMessageHandler(self, data):
        room, device = data["room"], data["device"]
        if device == "light":
            self.lightData[room] = data
            if data["state"] == "ON":
                if not room in self.lightOnList:
                    self.lightOnList.append(room)
            else:
                if room in self.lightOnList:
                    self.lightOnList.pop(self.lightOnList.index(room))
            self.notificationBox.update_light_count.emit(len(self.lightOnList))

        if device == "light" or device == "temperature":
            if self.stackedWidget.currentIndex() == 0:
                self.dashboardPage.dashboard_websocket_message.emit(data)
            elif self.stackedWidget.currentIndex() == 1:

                self.controlPage.control_page_websocket_message.emit(data)

    def lightSwitchToggledHandler(self, data):
        room = data["room"]
        self.lightData[room] = data
        if data["state"] == "ON":
            if not room in self.lightOnList:
                self.lightOnList.append(room)
        else:
            if room in self.lightOnList:
                self.lightOnList.pop(self.lightOnList.index(room))
        self.notificationBox.update_light_count.emit(len(self.lightOnList))

    def controlContentUpdate(self, data):
        # NOTE - debugging
        for room, component in data.items():
            print(f"debugging {room}")
            if self.lightData[room]["state"] == "ON":
                component.lightSwitchToggle(True)
            else:
                component.lightSwitchToggle(False)


if __name__ == "__main__":
    pass
