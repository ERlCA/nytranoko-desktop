from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from components.sidebarButton import Button


class Sidebar(QWidget):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        self.setup()

        if callback:
            self.dashboardButton.clicked.connect(lambda: callback(0))
            self.controlButton.clicked.connect(lambda: callback(1))

    def setup(self):
        self.setObjectName("sidebar")

        # sidebar layout
        self.sidebarLayout = QVBoxLayout(self)
        self.sidebarLayout.setContentsMargins(15, 0, 15, 0)
        self.sidebarLayout.setSpacing(15)
        self.sidebarLayout.setObjectName("sidebarLayout")

        # title
        self.title = QLabel("nyTranoko", self)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet(
            "QLabel {\n"
            "    padding:10px;\n"
            "    border: 4px solid rgba(0, 0, 0, 0);\n"
            "    border-bottom-color: #fff;\n"
            "    border-radius: 0px;\n"
            "    text-align: center\n"
            "}"
        )
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.sidebarLayout.addWidget(
            self.title, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop
        )

        # settings widget
        self.settingsWidget = QWidget(self)
        self.settingsWidget.setStyleSheet(
            "QWidget{    \n"
            "    background-color: rgba(0, 0, 0, 0);\n"
            "    border-radius: 20px;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    border: 2px solid rgba(0, 0, 0, 0);\n"
            "    background-color: rbga(0, 0, 0, 0);\n"
            "    border-radius: none;\n"
            "    outline: none;\n"
            "    text-align: left\n"
            "}\n"
            "QPushButton:hover {\n"
            "    border: 2px solid rgba(0, 0, 0, 0);\n"
            "    outline: none;\n"
            "    border-bottom-color: rgb(255, 159, 3);\n"
            "    color:  rgb(255, 159, 3);\n"
            "\n"
            "}"
        )
        self.settingsWidget.setObjectName("settingsWidget")

        self.settingsWidgetLayout = QVBoxLayout(self.settingsWidget)
        self.settingsWidgetLayout.setContentsMargins(5, 10, 5, 10)
        self.settingsWidgetLayout.setSpacing(6)
        self.settingsWidgetLayout.setObjectName("settingsWidgetLayout")

        # dashboard and control button
        self.dashboardButton = Button("Dashboard", "dashboard")
        self.controlButton = Button("Control", "control")

        self.settingsWidgetLayout.addWidget(self.dashboardButton)
        self.settingsWidgetLayout.addWidget(self.controlButton)

        # empty label for layout
        self.emptyLabel = QLabel(self.settingsWidget)
        self.emptyLabel.setText("")
        self.emptyLabel.setObjectName("emptyLabel")
        self.settingsWidgetLayout.addWidget(self.emptyLabel)

        self.sidebarLayout.addWidget(self.settingsWidget)

        # quit widget
        self.quitWidget = QWidget(self)
        self.quitWidget.setStyleSheet(
            "QWidget {\n"
            "    background-color: rgba(0, 0, 0, 0);\n"
            "    border-radius: 20px;\n"
            "    color: #fff;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
            "    border: 2px solid rgba(0, 0, 0, 0);\n"
            "    background-color: rbga(0, 0, 0, 0);\n"
            "    border-radius: none;\n"
            "    outline: none;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    \n"
            "    color: rgb(255, 159, 3);\n"
            "}"
        )
        self.quitWidget.setObjectName("quitWidget")
        self.quitWidgetLayout = QVBoxLayout(self.quitWidget)
        self.quitWidgetLayout.setContentsMargins(0, 10, 0, 10)
        self.quitWidgetLayout.setSpacing(10)
        self.quitWidgetLayout.setObjectName("quitWidgetLayout")

        # logout and quit button
        logoutButton = Button("Déconnexion", "logout")
        quitButton = Button(
            "Quitter", "quit", callback=QtCore.QCoreApplication.instance().quit
        )

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        logoutButton.setFont(font)
        quitButton.setFont(font)

        self.quitWidgetLayout.addWidget(logoutButton, 0, QtCore.Qt.AlignLeft)
        self.quitWidgetLayout.addWidget(quitButton, 0, QtCore.Qt.AlignLeft)

        self.sidebarLayout.addWidget(self.quitWidget, 0, QtCore.Qt.AlignBottom)
        self.sidebarLayout.setStretch(1, 1)


if __name__ == "__main__":
    pass
