from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QTimer
from PyQt5.QtNetwork import QAbstractSocket
import json


class Websockets(QThread):
    websocket_received_message = pyqtSignal(dict)
    websocket_disconnected = pyqtSignal()
    websoket_connected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.socket = QWebSocket()
        self.socket.error.connect(self.on_error)
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.textMessageReceived.connect(self.on_message_received)
        self.reconnectTimer = QTimer()
        self.reconnectTimer.setInterval(5000)
        self.reconnectTimer.timeout.connect(self.connect)
        self.connectingState = False

    def connect(self):
        if self.connectingState:
            return
        url = "ws://192.168.1.100:4000/api"
        self.connectingState = True
        self.socket.open(QUrl(url))

    def close_(self):
        self.connectingState = False
        print("closing websockets connection...")
        self.socket.close(1000, "connection closed")

    def on_connected(self):
        self.connectingState = False
        self.reconnectTimer.stop()
        print("Websocket : connected to the server")
        self.websoket_connected.emit()

    def on_error(self, error):
        print(f"WebSocket error: {error}")

    def on_disconnected(self):
        self.connectingState = False
        if not self.reconnectTimer.isActive():
            self.reconnectTimer.start()
        print("Disconnected from WebSocket server.")

        try:
            self.connect()
            self.websocket_disconnected.emit()
        except:
            return

    def on_message_received(self, message):
        try:
            data = json.loads(message)
            self.websocket_received_message.emit(data)
        except:
            return

    def send_message_json(self, jsonData):
        self.socket.sendTextMessage(jsonData)
