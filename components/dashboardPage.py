from PyQt5 import QtCore, QtWidgets as qtw
from components.noRoomMessage import NoRoomMessageWidget
from components.notificationBox import NotificationBox


class DashboardPage(qtw.QWidget):
    dashboard_websocket_message = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setup()
        # self.maintenance_on()

        # connection signal
        # self.dashboard_websocket_message.connect(self.websocketMessageHandler)

    def setup(self):
        pass
        # self.mainLayout = qtw.QVBoxLayout(self)
        # self.mainLayout.setContentsMargins(0, 40, 0, 0)
        # self.mainLayout.setSpacing(20)
        # self.mainLayout.setObjectName("mainLayout")
        # self.mainLayout.setStretch(0, 0)
        # self.mainLayout.setStretch(1, 2)

        # # container
        # self.container = qtw.QWidget(self)
        # self.container.setStyleSheet("background-color:red")
        # self.container.setObjectName("container")
        # # self.containerLayout = qtw.QGridLayout(self.container) # used in maintenance

        # # used when the dashboard is functionning
        # self.containerLayout = qtw.QVBoxLayout(self.container)
        # self.containerLayout.setContentsMargins(0, 0, 0, 0)
        # self.containerLayout.setSpacing(0)

        # # notification box
        # self.notificationBox = NotificationBox(self)
        # # self.notificationBox.setStyleSheet("background-color: blue")
        # # self.notificationBoxLayout = qtw.QHBoxLayout(self.notificationBox)
        # # self.containerLayout.addWidget(self.notificationBox, 0, QtCore.Qt.AlignTop)

        # # # Icon box
        # # self.iconBox = qtw.QWidget(self.notificationBox)
        # # self.iconBox.setStyleSheet("background-color: green")
        # # self.iconBoxLayout = qtw.QHBoxLayout(self.iconBox)
        # # self.notificationBoxLayout.addWidget(self.iconBox, 0, QtCore.Qt.AlignLeft)

        # # # icon for different notification
        # # self.flame = qtw.QPushButton(self.iconBox)
        # # self.flame.setText("")
        # # self.flame.setIcon(self.flameIcon)
        # # self.flame.setIconSize(QtCore.QSize(56, 56))
        # # self.iconBoxLayout.addWidget(self.flame)
        # # #
        # # self.gas = qtw.QPushButton(self.iconBox)
        # # self.gas.setText("")
        # # self.gas.setIcon(self.gasIcon)
        # # self.gas.setIconSize(QtCore.QSize(56, 56))
        # # self.iconBoxLayout.addWidget(self.gas)
        # # #
        # # self.pirSensor = qtw.QPushButton(self.iconBox)
        # # self.pirSensor.setText("")
        # # self.pirSensor.setIcon(self.personIcon)
        # # self.pirSensor.setIconSize(QtCore.QSize(56, 56))
        # # self.iconBoxLayout.addWidget(self.pirSensor)

        # # # notification message box
        # # self.messageBox = qtw.QWidget(self.notificationBox)
        # # self.messageBox.setStyleSheet("background-color: orange")
        # # self.messageBoxLayout = qtw.QWidget(self.messageBox)
        # # self.notificationBoxLayout.addWidget(self.messageBox, 0)

        # self.mainLayout.addWidget(self.container, 1)

    # def maintenance_on(self):
    #     for i in reversed(range(self.container.layout().count())):
    #         child = self.container.layout().itemAt(i).widget()
    #         if child:
    #             child.deleteLater()
    #             self.container.layout().removeWidget(child)
    #     self.noMessageWidget = qtw.QFrame()
    #     self.noMessageWidget.resize(380, 200)
    #     self.noMessageWidget.setMaximumSize(380, 200)
    #     self.noMessageWidget.setMinimumSize(380, 200)
    #     self.noMessageWidget.setObjectName("noMessageWidget")
    #     self.noMessageWidget.setStyleSheet(
    #         """
    #                 QFrame#noMessageWidget {
    #                     background-color: #0e273c;
    #                     border-radius: 20px;
    #                     border: 2px solid rgba(0,0,0,0)
    #                 }
    #                 QFrame#noMessageWidget:hover {
    #                     border: 2px solid rgb(255, 159, 3)
    #                 }
    #             """
    #     )
    #     self.noMessageWidgetLayout = qtw.QVBoxLayout(self.noMessageWidget)
    #     self.noMessageWidgetLayout.addWidget(
    #         NoRoomMessageWidget(
    #             message="Cette fonctionnalité n'est pas encore disponible.",
    #         ),
    #         0,
    #     )
    #     self.containerLayout.addWidget(
    #         self.noMessageWidget, 0, 0, QtCore.Qt.AlignCenter
    #     )

    # def websocketMessageHandler(self, data):
    #     print(data)


# if __name__ == "__main__":
# pass
