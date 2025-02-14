from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
import json


class Websockets(QThread):
    websocket_received_message = pyqtSignal(dict)
    websocket_disconnected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.socket = QWebSocket()
        self.socket.error.connect(self.on_error)
        self.socket.connected.connect(self.on_connected)
        self.socket.disconnected.connect(self.on_disconnected)
        self.socket.textMessageReceived.connect(self.on_message_received)

    def connect(self):
        url = "ws://192.168.1.100:4000/api"
        self.socket.open(QUrl(url))

    def close_(self):
        print("closing websockets connection...")
        self.socket.close(1000, "connection closed")

    def on_connected(self):
        print("Websocket : connected to the server")

    def on_error(self, error):
        print(f"WebSocket error: {error}")

    def on_disconnected(self):
        print("Disconnected from WebSocket server.")
        self.websocket_disconnected.emit()

    def on_message_received(self, message):
        try:
            data = json.loads(message)
            self.websocket_received_message.emit(data)
        except:
            return

    def send_message_json(self, jsonData):
        self.socket.sendTextMessage(jsonData)
