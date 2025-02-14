import PyQt5.QtWidgets as qtw
from PyQt5 import QtCore, QtGui


class Header(qtw.QFrame):
    def __init__(self, title="Header", error=None, parent=None):
        super().__init__(parent)

        self.circleRedIcon = self.loadIcon("circle-red")
        self.circleGreenIcon = self.loadIcon("circle-green")
        self.refreshIcon = self.loadIcon("refresh")

        self.setup(title)
        self.updateHeader(error)

    def setup(self, title):
        self.setStyleSheet(
            """
            QFrame,QWidget, QPushButton {
              border: none;
              background-color: none
            }
            """
            # QFrame{background-color: red}
        )
        self.mainLayout = qtw.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 0, 10, 0)

        # title
        self.title = qtw.QLabel(title, self)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.title.setStyleSheet("color: #0e273c")
        self.mainLayout.addWidget(self.title, 0, QtCore.Qt.AlignLeft)

        # message box
        self.messageBox = qtw.QWidget(self)
        self.messageBox.setObjectName("messageBoxWidget")
        self.messageBox.setStyleSheet(
            """
              background-color: #0e273c;
              padding: 5px 10px;
              border-radius: 20px
            """
        )
        self.messageBoxLayout = qtw.QHBoxLayout(self.messageBox)
        self.messageBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.messageBoxLayout.setSpacing(0)
        self.messageBoxLayout.setObjectName("messageBoxLayout")
        self.mainLayout.addWidget(self.messageBox, 1, QtCore.Qt.AlignRight)

        self.iconNotif = qtw.QPushButton(self.messageBox)
        self.iconNotif.setText("")
        self.iconNotif.setIconSize(QtCore.QSize(38, 38))
        self.messageBoxLayout.addWidget(self.iconNotif)

        # message
        self.messageLabel = qtw.QLabel("", self.messageBox)
        font.setPointSize(16)
        font.setBold(False)
        self.messageLabel.setFont(font)
        self.messageLabel.setStyleSheet("color: #fff")
        self.messageBoxLayout.addWidget(self.messageLabel)

        # refresh button
        self.refreshButton = qtw.QPushButton(self.messageBox)
        self.refreshButton.setText("")
        self.refreshButton.setIcon(self.refreshIcon)
        self.refreshButton.setIconSize(QtCore.QSize(38, 38))
        self.messageBoxLayout.addWidget(self.refreshButton)

    def loadIcon(self, iconName):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(f"resources/icons/{iconName}.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        return icon

    def updateHeader(self, error):
        if error:
            self.iconNotif.setIcon(self.circleRedIcon)
            self.messageLabel.setText("La connexion a été interrompue.")
            self.refreshButton.setVisible(True)
            self.refreshButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        else:
            self.iconNotif.setIcon(self.circleGreenIcon)
            self.messageLabel.setText("Le système fonctionne très bien.")
            self.refreshButton.setVisible(False)
