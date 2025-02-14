from PyQt5 import QtCore, QtWidgets
from components.sidebar import Sidebar
from components.controlPage import ControlPage
from components.dashboardPage import DashboardPage
from utils.websockets import Websockets


class Ui_homeWindow(QtWidgets.QWidget):
    logout_requested_from_home = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ws = Websockets()
        self.ws.connect()

        self.temperatureData = {}

        self.setupUi()
        self.websocketLastState = None

        # connection pyqtSignals
        self.ws.websoket_connected.connect(self.websocketConnectedHandler)
        self.ws.websocket_disconnected.connect(self.websocketDisconnectedHandler)
        self.ws.websocket_received_message.connect(self.websocketMessageHandler)

        self.sidebar.logout_requested.connect(self.logout_requested_from_home.emit)
        self.sidebar.control_page_requested.connect(self.controlPageRequesting)
        self.sidebar.dashboard_page_requested.connect(self.dashboardPageRequesting)

    def setupUi(self):
        self.setObjectName("self")
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        self.setWindowTitle("Home")

        self.homeWindowLayout = QtWidgets.QHBoxLayout(self)
        self.homeWindowLayout.setContentsMargins(10, 10, 10, 10)
        self.homeWindowLayout.setSpacing(10)
        self.homeWindowLayout.setObjectName("homeWindowLayout")
        # self.resize(900, 600)
        # self.setMinimumSize(900, 600)
        # self.setMaximumSize(900, 600)

        # adding sidebar
        self.sidebarContainer = QtWidgets.QWidget(self)
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
        self.sidebarContainerLayout = QtWidgets.QGridLayout(self.sidebarContainer)
        self.sidebar = Sidebar()
        self.sidebarContainerLayout.addWidget(self.sidebar)
        self.homeWindowLayout.addWidget(self.sidebarContainer)

        # ========================================================
        # adding main page
        self.mainWidget = QtWidgets.QStackedWidget(self)
        self.mainWidget.setStyleSheet(
            "QStackedWidget > QWidget > QLabel {\n"
            "    background-color: rgba(0, 0, 0, 0);\n"
            "    color: #0e273c;\n"
            "}\n"
            ""
        )
        self.mainWidget.setObjectName("mainWidget")

        self.dashboardPage = DashboardPage()
        self.mainWidget.addWidget(self.dashboardPage)  # add dashboard page
        self.controlPage = ControlPage(callback=self.ws.send_message_json)
        self.mainWidget.addWidget(self.controlPage)  # add control page

        self.homeWindowLayout.addWidget(self.mainWidget)

        self.mainWidget.setCurrentIndex(0)

    def dashboardPageRequesting(self):
        if self.mainWidget.currentIndex() != 0:
            self.changePage(0)
            self.controlPage.quitting_control_page.emit()

    def controlPageRequesting(self):
        if self.mainWidget.currentIndex() != 1:
            self.changePage(1)
            self.controlPage.control_page_requested.emit()

    def changePage(self, index):
        if self.mainWidget:
            self.mainWidget.setCurrentIndex(index)

    def homepage_requested_handler(self):
        pass

    # websocket event handler
    def websocketDisconnectedHandler(self):
        if self.websocketLastState == "disconnected":
            return
        self.controlPage.header.updateHeader(True)
        self.dashboardPage.header.updateHeader(True)
        self.websocketLastState = "disconnected"

    def websocketConnectedHandler(self):
        if self.websocketLastState == "connected":
            return
        self.controlPage.header.updateHeader(False)
        self.dashboardPage.header.updateHeader(False)
        self.websocketLastState = "connected"

    def websocketMessageHandler(self, data):
        room, device = data["room"], data["device"]
        if device == "light" or device == "temperature":
            if self.mainWidget.currentIndex() == 0:
                self.dashboardPage.dashboard_websocket_message.emit(data)
            elif self.mainWidget.currentIndex() == 1:
                self.controlPage.control_page_websocket_message.emit(data)


if __name__ == "__main__":
    pass
