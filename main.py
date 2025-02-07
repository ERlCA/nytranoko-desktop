import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtGui
from ui.login_ui import Ui_loginWindow
from ui.home_ui import Ui_homeWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("resources/icons/new-house.png"))
        self.loginWindow = None
        self.homepage = None
        self.loginInit()
        # self.homeInit()

    def loginInit(self):
        if self.homepage and self.homepage.isVisible():
            self.homepage.close()
        self.showNormal()
        self.setWindowTitle("Login | nyTranoko")
        self.loginWindow = Ui_loginWindow()
        self.loginWindow.login_successful.connect(self.homeInit)
        self.setCentralWidget(self.loginWindow)
        self.loginWindow.show()

    def homeInit(self):
        if self.loginWindow and self.loginWindow.isVisible():
            self.loginWindow.close()
        self.showFullScreen()
        self.setWindowTitle("Home | nyTranoko")
        self.homepage = Ui_homeWindow()
        self.homepage.logout_requested.connect(self.logout)

        self.setCentralWidget(self.homepage)
        self.homepage.show()

    def logout(self):
        if self.homepage and self.homepage.isVisible():
            self.homepage.close()
        self.loginInit()


if __name__ == "__main__":
    from qasync import QEventLoop
    import asyncio

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    with loop:
        loop.run_forever()
