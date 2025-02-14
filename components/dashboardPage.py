from PyQt5 import QtGui, QtCore, QtWidgets as qtw
from components.noRoomMessage import NoRoomMessageWidget


class DashboardPage(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()
        self.maintenance_on()

    def setup(self):
        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setStretch(0, 0)
        self.mainLayout.setStretch(0, 2)

        # title
        self.title = qtw.QLabel("Dahsboard", self)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.mainLayout.addWidget(self.title, 0, QtCore.Qt.AlignTop)

        # container
        self.container = qtw.QWidget(self)
        self.container.setObjectName("container")
        self.containerLayout = qtw.QGridLayout(self.container)

        self.mainLayout.addWidget(self.container, 1)

    def maintenance_on(self):
        for i in reversed(range(self.container.layout().count())):
            child = self.container.layout().itemAt(i).widget()
            if child:
                child.deleteLater()
                self.container.layout().removeWidget(child)
        self.noMessageWidget = qtw.QFrame()
        self.noMessageWidget.resize(380, 200)
        self.noMessageWidget.setMaximumSize(380, 200)
        self.noMessageWidget.setMinimumSize(380, 200)
        self.noMessageWidget.setObjectName("noMessageWidget")
        self.noMessageWidget.setStyleSheet(
            """
                    QFrame#noMessageWidget {
                        background-color: #0e273c; 
                        border-radius: 20px;
                        border: 2px solid rgba(0,0,0,0)
                    } 
                    QFrame#noMessageWidget:hover {
                        border: 2px solid rgb(255, 159, 3)
                    }
                """
        )
        self.noMessageWidgetLayout = qtw.QVBoxLayout(self.noMessageWidget)
        self.noMessageWidgetLayout.addWidget(
            NoRoomMessageWidget(
                message="Cette fonctionnalité n'est pas encore disponible.",
            ),
            0,
        )
        self.containerLayout.addWidget(
            self.noMessageWidget, 0, 0, QtCore.Qt.AlignCenter
        )


if __name__ == "__main__":
    pass
