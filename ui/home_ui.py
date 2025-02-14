from PyQt5 import QtCore, QtWidgets
from components.sidebar import Sidebar
from components.controlPage import ControlPage
from components.dashboardPage import DashboardPage


class Ui_homeWindow(QtWidgets.QWidget):
    logout_requested_from_home = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_homeWindow, self).__init__()
        self.setupUi(self)

        # connection pyqtSignals
        self.sidebar.logout_requested.connect(self.logout_requested_from_home.emit)
        self.sidebar.control_page_requested.connect(self.controlPageRequesting)
        self.sidebar.dashboard_page_requested.connect(self.dashboardPageRequesting)

    def setupUi(self, homeWindow):
        homeWindow.setObjectName("homeWindow")
        homeWindow.setStyleSheet("background-color: rgb(250, 250, 250)")
        self.homeWindowLayout = QtWidgets.QHBoxLayout(homeWindow)
        self.homeWindowLayout.setContentsMargins(15, 15, 0, 15)
        self.homeWindowLayout.setSpacing(10)
        self.homeWindowLayout.setObjectName("homeWindowLayout")
        # self.resize(900, 600)
        # self.setMinimumSize(900, 600)
        # self.setMaximumSize(900, 600)

        # adding sidebar
        self.sidebarContainer = QtWidgets.QWidget(homeWindow)
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
        self.mainWidget = QtWidgets.QStackedWidget(homeWindow)
        self.mainWidget.setStyleSheet(
            "QStackedWidget > QWidget > QLabel {\n"
            "    padding-top: 40px;\n"
            "    background-color: rgba(0, 0, 0, 0);\n"
            "    color: #0e273c;\n"
            "}\n"
            ""
        )
        self.mainWidget.setObjectName("mainWidget")

        self.mainWidget.addWidget(DashboardPage())  # add dashboard page
        self.controlPage = ControlPage()
        self.mainWidget.addWidget(self.controlPage)  # add control page

        self.homeWindowLayout.addWidget(self.mainWidget)

        self.retranslateUi(homeWindow)
        self.mainWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(homeWindow)

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

    def retranslateUi(self, homeWindow):
        _translate = QtCore.QCoreApplication.translate
        homeWindow.setWindowTitle(_translate("homeWindow", "Home"))


if __name__ == "__main__":
    pass
