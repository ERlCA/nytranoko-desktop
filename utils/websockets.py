from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtCore import QUrl, QThread, pyqtSignal, QTimer
import json
import socket


class Websockets(QThread):
    websocket_received_message = pyqtSignal(dict)
    websocket_disconnected = pyqtSignal()
    websoket_connected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ws = QWebSocket()
        self.ws.ping()
        self.ws.error.connect(self.on_error)
        self.ws.connected.connect(self.on_connected)
        self.ws.disconnected.connect(self.on_disconnected)
        self.ws.textMessageReceived.connect(self.on_message_received)

        # to automatically reconnect  when connection is lost
        self.reconnectTimer = QTimer()
        self.reconnectTimer.setInterval(5000)
        self.reconnectTimer.timeout.connect(self.connect)

        # prevent calling connect() function if it is already running
        self.connectingTimeout = QTimer()
        self.connectingTimeout.setSingleShot(True)
        self.connectingTimeout.timeout.connect(self.ws.abort)
        self.connectingState = False

    def connect(self):
        if (
            not self.is_connected_to_wifi("192.168.1.1")
            and not self.reconnectTimer.isActive()
        ):
            self.reconnectTimer.start()
            return

        if self.connectingState:
            return

        url = "ws://192.168.1.100:4000/api"
        self.connectingState = True
        self.ws.open(QUrl(url))
        self.connectingTimeout.start(5000)

    def close_(self):
        self.connectingState = False
        print("closing websockets connection...")
        self.ws.close(1000, "connection closed")

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

    def wifi_checking(self):
        # NOTE - checking wifi function
        print("checking wifi.....")
        if not self.wifiCheckTimer.isActive():
            self.wifiCheckTimer.start()
        self.connect()

    def on_message_received(self, message):
        try:
            data = json.loads(message)
            self.websocket_received_message.emit(data)
        except:
            return

    def send_message_json(self, jsonData):
        self.ws.sendTextMessage(jsonData)

    def is_connected_to_wifi(self, ip):
        try:
            # Attempt to connect to the gateway IP on port 80
            sock = socket.create_connection((ip, 80), timeout=5)
            sock.close()
            return True
        except (socket.timeout, socket.error):
            return False
