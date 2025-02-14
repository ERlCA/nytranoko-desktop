from PyQt5 import QtCore, QtGui, QtWidgets as qtw
from utils.loginHandle import loginHandle
import os
from components.popUp import CloseAppWidget
import asyncio


class Ui_loginWindow(qtw.QWidget):
    login_successful = QtCore.pyqtSignal()

    def __init__(self):
        super(Ui_loginWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, loginWindow):
        loginWindow.setObjectName("loginWindow")
        # resizing
        loginWindow.resize(650, 500)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loginWindow.sizePolicy().hasHeightForWidth())
        loginWindow.setSizePolicy(sizePolicy)
        loginWindow.setMinimumSize(QtCore.QSize(650, 500))
        loginWindow.setMaximumSize(QtCore.QSize(650, 500))

        font = QtGui.QFont()
        font.setPointSize(11)
        loginWindow.setFont(font)
        loginWindow.setStyleSheet(
            "#leftWidget {\n"
            "    background-color: #0e273c\n"
            "}\n"
            "\n"
            "#formWidget {\n"
            "    background-color: rgb(252, 252, 252)\n"
            "}\n"
            "\n"
            "QLineEdit {\n"
            "background: #00000000;\n"
            "border: 2px solid rgba(0, 0, 0, 0);\n"
            "border-bottom-color: rgba(0, 0, 0, 200);\n"
            "color: #000;\n"
            "padding: 10px 0;\n"
            "}\n"
            "\n"
            "QLineEdit:hover {\n"
            "    border-bottom-color: #fa8334;\n"
            "}\n"
            "\n"
            "QLineEdit:focus {\n"
            "    border-bottom-color: rgb(255, 159, 3);\n"
            "}\n"
            "\n"
            "QPushButton#loginButton {\n"
            "  color: rgba(0, 0, 0, 200)\n"
            "}\n"
            "\n"
            "QPushButton#quitButton {\n"
            "    padding: 0 5px;\n"
            "    border-radius: 50px;\n"
            "    background-color: rgba(0, 0, 0, 0);\n"
            "}\n"
            "\n"
            "\n"
            "QPushButton#loginButton:hover, QPushButton#quitButton:hover {\n"
            "    background-color: rgb(255, 159, 3);\n"
            "    color: #fff;\n"
            "    border: none\n"
            "}\n"
            "\n"
            "QPushButton#loginButton:disabled, QPushButton#quitButton:disabled{\n"
            "    background-color: #eee;\n"
            "    color: #0e273c;\n"
            "    border: none\n;"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "    background-color: #fa8334;\n"
            "    color: rgb(231, 231, 231);\n"
            "    border: 2px solid rgba(0, 0, 0, 0);\n"
            "}\n"
            "\n"
            ""
        )
        self.loginWindowLayout = qtw.QGridLayout(loginWindow)
        self.loginWindowLayout.setContentsMargins(0, 0, 0, 0)
        self.loginWindowLayout.setSpacing(0)
        self.loginWindowLayout.setObjectName("loginWindowLayout")

        # creating left widget of login
        self.leftWidget = qtw.QWidget(loginWindow)
        self.leftWidget.setStyleSheet("color: #fff")
        self.leftWidget.setObjectName("leftWidget")
        self.leftWidgetLayout = qtw.QVBoxLayout(self.leftWidget)
        self.leftWidgetLayout.setContentsMargins(10, 40, 10, 0)
        self.leftWidgetLayout.setSpacing(20)
        self.leftWidgetLayout.setObjectName("leftWidgetLayout")
        # title nyTranoko
        self.titleLabel = qtw.QLabel(self.leftWidget)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(40)
        self.titleLabel.setFont(font)
        self.titleLabel.setStyleSheet("")
        self.titleLabel.setScaledContents(True)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setObjectName("titleLabel")
        self.leftWidgetLayout.addWidget(self.titleLabel)
        # description of nyTranoko
        self.descLabel = qtw.QLabel(self.leftWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.descLabel.setFont(font)
        self.descLabel.setFrameShape(qtw.QFrame.NoFrame)
        self.descLabel.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.descLabel.setWordWrap(True)
        self.descLabel.setIndent(-1)
        self.descLabel.setObjectName("descLabel")
        self.leftWidgetLayout.addWidget(self.descLabel, 0, QtCore.Qt.AlignHCenter)
        self.label = qtw.QLabel(self.leftWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.leftWidgetLayout.addWidget(self.label)
        self.leftWidgetLayout.setStretch(2, 1)
        self.loginWindowLayout.addWidget(self.leftWidget, 0, 0, 1, 1)

        # creating form widget (right side)
        self.formWidget = qtw.QWidget(loginWindow)
        self.formWidget.setObjectName("formWidget")
        self.formWidgetLayout = qtw.QVBoxLayout(self.formWidget)
        self.formWidgetLayout.setContentsMargins(25, 70, 25, 15)
        self.formWidgetLayout.setSpacing(10)
        self.formWidgetLayout.setObjectName("formWidgetLayout")
        self.loginLabel = qtw.QLabel(self.formWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        # login label
        self.loginLabel.setFont(font)
        self.loginLabel.setStyleSheet("color: rbg(0, 0, 0, 200)")
        self.loginLabel.setObjectName("loginLabel")
        self.loginLabel.setStyleSheet("color: black")
        self.formWidgetLayout.addWidget(self.loginLabel, 0, QtCore.Qt.AlignTop)
        self.entryWidget = qtw.QWidget(self.formWidget)
        self.entryWidget.setObjectName("entryWidget")
        self.entryWidgetLayout = qtw.QVBoxLayout(self.entryWidget)
        self.entryWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.entryWidgetLayout.setSpacing(30)
        self.entryWidgetLayout.setObjectName("entryWidgetLayout")

        self.usernameEntry = qtw.QLineEdit(self.entryWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameEntry.setFont(font)
        self.usernameEntry.setStyleSheet("margin-left: 25px")
        self.usernameEntry.setObjectName("usernameEntry")
        self.entryWidgetLayout.addWidget(self.usernameEntry)

        self.passwordEntry = qtw.QLineEdit(self.entryWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordEntry.setFont(font)
        self.passwordEntry.setObjectName("passwordEntry")
        self.passwordEntry.setEchoMode(qtw.QLineEdit.Password)

        self.passwordWidget = qtw.QWidget(self.entryWidget)
        self.passwordWidgetLayout = qtw.QHBoxLayout(self.passwordWidget)
        self.passwordWidgetLayout.setContentsMargins(0, 0, 0, 0)

        self.openEyeIcon = QtGui.QIcon()
        self.openEyeIcon.addPixmap(
            QtGui.QPixmap(os.path.abspath("resources/icons/open-eye.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.closeEyeIcon = QtGui.QIcon()
        self.closeEyeIcon.addPixmap(
            QtGui.QPixmap(os.path.abspath("resources/icons/close-eye.png")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.eyeButton = qtw.QPushButton(self.passwordWidget)
        self.eyeButton.setIcon(self.openEyeIcon)
        self.eyeButton.setIconSize(QtCore.QSize(16, 16))
        self.eyeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.eyeButton.setCheckable(True)
        self.eyeButton.toggled.connect(self.togglePasswordVisibility)
        self.eyeButton.setStyleSheet(
            """
            background-color: rgba(0,0,0,0);
            border: none;
            """
        )
        self.passwordWidgetLayout.addWidget(self.eyeButton)
        self.passwordWidgetLayout.addWidget(self.passwordEntry)

        self.entryWidgetLayout.addWidget(self.passwordWidget)
        self.formWidgetLayout.addWidget(self.entryWidget, 0, QtCore.Qt.AlignBottom)
        self.errorLabel = qtw.QLabel(self.formWidget)
        self.errorLabel.setObjectName("errorLabel")
        self.errorLabel.setStyleSheet("color: rgb(252,252,252);")
        self.formWidgetLayout.addWidget(self.errorLabel, 0, QtCore.Qt.AlignTop)

        # buttons
        self.buttonWidget = qtw.QWidget(self.formWidget)
        self.buttonWidget.setObjectName("buttonWidget")
        self.buttonWidgetLayout = qtw.QVBoxLayout(self.buttonWidget)
        self.buttonWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonWidgetLayout.setSpacing(20)
        self.buttonWidgetLayout.setObjectName("buttonWidgetLayout")
        # login
        self.loginButton = qtw.QPushButton(self.buttonWidget)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginButton.sizePolicy().hasHeightForWidth())
        self.loginButton.setSizePolicy(sizePolicy)
        self.loginButton.setMinimumSize(QtCore.QSize(0, 60))
        self.loginButton.setMaximumSize(QtCore.QSize(16777215, 60))
        self.loginButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.loginButton.setFont(font)
        self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginButton.setStyleSheet("")
        self.loginButton.setObjectName("loginButton")
        self.loginButton.clicked.connect(self.performLogin)  # login button event
        self.buttonWidgetLayout.addWidget(self.loginButton)
        # quit
        self.quitButton = qtw.QPushButton(self.buttonWidget)
        self.quitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quitButton.setStyleSheet(
            "QPushButton {\n"
            "    border: none;\n"
            "    height: 50px;\n"
            "    width: 40px;\n"
            "    border-radius: 20px;\n"
            "}\n"
            "\n"
            "QPushButton:hover{\n"
            "}"
        )
        self.quitButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(".\\ui\\login\\../../resources/icons/power-button.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.quitButton.setIcon(icon)
        self.quitButton.setIconSize(QtCore.QSize(36, 36))
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(self.showCloseAppWidget)  # ===============
        self.buttonWidgetLayout.addWidget(self.quitButton, 0, QtCore.Qt.AlignRight)
        self.formWidgetLayout.addWidget(self.buttonWidget, 0, QtCore.Qt.AlignBottom)
        self.formWidgetLayout.setStretch(1, 1)
        self.formWidgetLayout.setStretch(3, 1)
        self.loginWindowLayout.addWidget(self.formWidget, 0, 1, 1, 1)

        self.retranslateUi(loginWindow)
        QtCore.QMetaObject.connectSlotsByName(loginWindow)
        self.usernameEntry.setFocus()

    def performLogin(self):
        username = self.usernameEntry.text()
        password = self.passwordEntry.text()
        asyncio.create_task(self.asyncLoginHandle(username, password))

    async def asyncLoginHandle(self, username, password):
        self.loginButton.setDisabled(True)
        self.quitButton.setDisabled(True)
        self.loginButton.setText("En attente...")
        self.usernameEntry.setDisabled(True)
        self.passwordEntry.setDisabled(True)
        if await loginHandle(username, password):
            self.errorLabel.setStyleSheet("color: rgb(252,252,252)")
            self.loginButton.setText("Réussie.")
            self.login_successful.emit()

        else:
            self.errorLabel.setStyleSheet("color: red")
            self.loginButton.setText("Connexion")
            self.loginButton.setDisabled(False)
        self.quitButton.setDisabled(False)
        self.usernameEntry.setDisabled(False)
        self.usernameEntry.setFocus()
        self.passwordEntry.setDisabled(False)

    def togglePasswordVisibility(self, checked):
        if checked:
            self.passwordEntry.setEchoMode(qtw.QLineEdit.Normal)
            self.eyeButton.setIcon(self.openEyeIcon)
        else:
            self.eyeButton.setIcon(self.closeEyeIcon)
            self.passwordEntry.setEchoMode(qtw.QLineEdit.Password)

    def retranslateUi(self, loginWindow):
        _translate = QtCore.QCoreApplication.translate
        loginWindow.setWindowTitle(_translate("loginWindow", "Se connecter"))
        self.titleLabel.setText(_translate("loginWindow", "nyTranoko"))
        self.descLabel.setText(
            _translate(
                "loginWindow",
                '"Faites confiance à nytranoko pour la sécurité de votre maison."',
            )
        )
        self.loginLabel.setText(_translate("loginWindow", "Se connecter"))
        self.passwordEntry.setPlaceholderText(_translate("loginWindow", "Mot de passe"))
        self.usernameEntry.setPlaceholderText(
            _translate("loginWindow", "Nom d'utilisateur")
        )
        self.errorLabel.setText(
            _translate("loginWindow", "Nom d'utilisateur ou mot de passe incorrect")
        )
        self.loginButton.setText(_translate("loginWindow", "Connexion"))
        self.loginButton.setShortcut(_translate("loginWindow", "Return"))
        self.quitButton.setShortcut(_translate("loginWindow", "Escape"))

    def showCloseAppWidget(self):
        closeAppWidget = CloseAppWidget()
        result = closeAppWidget.exec_()
        if result == qtw.QDialog.Accepted:
            qtw.qApp.quit()


if __name__ == "__main__":
    import sys
    from qasync import QEventLoop

    app = qtw.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    loginWindow = qtw.QWidget()
    ui = Ui_loginWindow()
    ui.setupUi(loginWindow)
    loginWindow.show()
    with loop:
        loop.run_forever()
