import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import QtCore, QtGui
from ui.login.login_ui import Ui_loginWindow
from ui.home.home_ui import Ui_homeWindow
from ui.dashboardContent.dashboardContent import Ui_Form


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon("resources/icons/new-house.png"))
        # self.loginInit()
        self.homeInit()
        # self.dashInit()

    def loginInit(self):
        self.loginPage = Ui_loginWindow()
        self.central_widget = QWidget()

        self.loginPage.setupUi(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def homeInit(self):
        self.showFullScreen()
        self.homepage = Ui_homeWindow()
        self.central_widget = QWidget()

        self.homepage.setupUi(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def dashInit(self):
        self.dash = Ui_Form()
        self.central_widget = QWidget()

        self.dash.setupUi(self.central_widget)
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
