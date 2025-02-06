from PyQt5 import QtCore, QtWidgets
from components.sidebar import Sidebar
from components.controlPage import ControlPage
from components.dashboardPage import DashboardPage


class Ui_homeWindow(object):
    def setupUi(self, homeWindow):
        homeWindow.setObjectName("homeWindow")
        homeWindow.setStyleSheet("background-color: rgb(250, 250, 250)")
        self.homeWindowLayout = QtWidgets.QHBoxLayout(homeWindow)
        self.homeWindowLayout.setContentsMargins(15, 15, 0, 15)
        self.homeWindowLayout.setSpacing(10)
        self.homeWindowLayout.setObjectName("homeWindowLayout")

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
        self.sidebarContainerLayout.addWidget(Sidebar(callback=self.changePage))
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
        self.mainWidget.addWidget(ControlPage())  # add control page

        self.homeWindowLayout.addWidget(self.mainWidget)

        self.retranslateUi(homeWindow)
        self.mainWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(homeWindow)

    def changePage(self, index):
        if self.mainWidget:
            self.mainWidget.setCurrentIndex(index)

    def retranslateUi(self, homeWindow):
        _translate = QtCore.QCoreApplication.translate
        homeWindow.setWindowTitle(_translate("homeWindow", "Home"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    homeWindow = QtWidgets.QWidget()
    ui = Ui_homeWindow()
    ui.setupUi(homeWindow)
    homeWindow.show()
    sys.exit(app.exec_())
