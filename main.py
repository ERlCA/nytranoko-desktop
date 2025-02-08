import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.login_ui import Ui_loginWindow
from ui.home_ui import Ui_homeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("resources/icons/new-house.png"))
        self.loginWindow = None
        self.homeWindow = None

        self.loginInit()  # use this for production
        # self.homeInit()  # use this in development

    def loginInit(self):
        # delete homeWindow (homepage)
        if (
            hasattr(self, "homeWindow")
            and self.homeWindow
            and self.homeWindow.isVisible()
        ):
            self.homeWindow.deleteLater()
            self.homeWindow = None

        self.showNormal()
        self.setWindowTitle("Login | nyTranoko")

        # delete the central widget
        if self.centralWidget():
            self.centralWidget().deleteLater()
            self.takeCentralWidget()

        # creating a container, for a border
        self.loginWindowContainer = QtWidgets.QFrame(self)
        self.loginWindowContainer.setObjectName("loginWindowContainer")
        self.loginWindowContainer.setStyleSheet(
            """
            QFrame#loginWindowContainer {
                border: 2px solid rgb(255, 159, 3);  
            }
            """
        )
        self.loginWindowContainerLayout = QtWidgets.QVBoxLayout(
            self.loginWindowContainer
        )
        self.loginWindow = Ui_loginWindow()

        self.loginWindowContainerLayout.addWidget(self.loginWindow)
        self.loginWindowContainerLayout.setContentsMargins(0, 0, 0, 0)

        self.loginWindow.login_successful.connect(self.homeInit)
        self.setCentralWidget(self.loginWindowContainer)
        self.loginWindow.show()

    def homeInit(self):
        # delete login page
        if (
            hasattr(self, "loginWindowContainer")
            and self.loginWindow
            and self.loginWindow.isVisible()
        ):
            self.centralWidget().deleteLater()
            self.loginWindow = None

        # delete central widget
        if self.centralWidget():
            self.centralWidget().deleteLater()
            self.takeCentralWidget()

        self.showFullScreen()  # show window in fullscreen
        self.setWindowTitle("Home | nyTranoko")
        self.homeWindow = Ui_homeWindow()
        self.homeWindow.logout_requested.connect(self.logout)

        self.setCentralWidget(self.homeWindow)
        self.homeWindow.show()

    def logout(self):
        self.loginInit()


if __name__ == "__main__":
    from qasync import QEventLoop
    import asyncio

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  # there's a http request who needs event loop
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
