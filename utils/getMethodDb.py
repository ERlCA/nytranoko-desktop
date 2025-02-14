import httpx
from PyQt5.QtCore import QThread, pyqtSignal


class GetRooms(QThread):
    room_data_received = pyqtSignal(dict)

    def run(self):
        url = "http://192.168.1.100:4000/api/rooms"

        try:
            with httpx.Client() as client:
                res = client.get(url, timeout=5)
                if res.status_code != 200:
                    raise Exception("Erreur lors de la requête.")

                data = res.json()

                if data["success"]:
                    self.room_data_received.emit(
                        {"success": True, "data": data["body"]}
                    )
                else:
                    raise Exception("Aucune chambre/salle trouvée.")
        except Exception as err:
            self.room_data_received.emit({"success": False, "data": err})
        except httpx.TimeoutException:
            self.room_data_received.emit(
                {"success": False, "data": "Request timed out."}
            )
        except httpx.RequestError as req_err:
            self.room_data_received.emit(
                {"success": False, "data": f"Request error: {req_err}"}
            )


class GetDevices(QThread):
    device_data_received = pyqtSignal(dict)

    def run(self):
        url = "http://192.168.1.100:4000/api/devices"

        try:
            with httpx.Client() as client:
                res = client.get(url, timeout=5)

                if res.status_code != 200:
                    raise Exception("Erreur lors de la requête.")
                data = res.json()

                if data["success"]:
                    self.device_data_received.emit(
                        {"success": True, "data": data["body"]}
                    )
                else:
                    raise Exception("Aucun appareil trouvé.")
        except Exception as err:
            self.device_data_received.emit({"success": False, "data": err})
        except httpx.TimeoutException:
            self.room_data_received.emit(
                {"success": False, "data": "Request timed out."}
            )
        except httpx.RequestError as req_err:
            self.room_data_received.emit(
                {"success": False, "data": f"Request error: {req_err}"}
            )
