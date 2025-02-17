from PyQt5 import QtCore, QtWidgets as qtw
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QDateTime


class DashboardPage(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup()

        self.tempChart = {}
        self.tempCuisine = []
        self.tempCoucher = []
        self.pirData = list()
        self.flameData = list()
        self.gasData = list()

        self.temperatureChart()

        # connection signal

    def setup(self):
        pass
        self.mainLayout = qtw.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setObjectName("mainLayout")

        # setting scrollArea
        self.scrollArea = qtw.QScrollArea(self)
        self.scrollArea.setFrameShape(qtw.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaContainer = qtw.QWidget()
        self.scrollAreaContainer.setObjectName("scrollAreaContainer")
        self.scrollAreaContainerLayout = qtw.QVBoxLayout(self.scrollAreaContainer)
        self.scrollAreaContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaContainerLayout.setSpacing(0)
        self.scrollAreaContainerLayout.setObjectName("scrollAreaContainerLayout")

        # scrollArea needs a widget as container to its elements
        self.container = qtw.QWidget(self.scrollAreaContainer)
        self.container.setObjectName("container")
        self.containerLayout = qtw.QVBoxLayout(self.container)
        self.containerLayout.setContentsMargins(0, 0, 0, 0)
        self.containerLayout.setSpacing(10)
        self.containerLayout.setObjectName("containerLayout")

        self.scrollAreaContainerLayout.addWidget(self.container)
        self.scrollArea.setWidget(self.scrollAreaContainer)
        self.mainLayout.addWidget(self.scrollArea)

    def temperatureDataUpdate(self, data):
        if len(data["cuisine"]) != len(self.tempCuisine):
            if len(self.tempCuisine) >= 30:
                self.tempCuisine[0]
            self.tempCuisine.append(data["cuisine"][-1])

        elif len(data["chambre_à_coucher"]) != len(self.tempCoucher):
            if len(self.tempCoucher) >= 30:
                self.tempCoucher[0]
            self.tempCoucher.append(data["chambre_à_coucher"][-1])

        self.tempChartUpdate()

    def pirDataUpdate(self, data):
        if len(data) != len(self.pirData):
            self.pirData = data

    def flameDataUpdate(self, data):
        if len(data) != len(self.flameData):
            self.flameData = data

    def gasDataUpdate(self, data):
        if len(data) != len(self.gasData):
            self.gasData = data

    def temperatureChart(self):
        # chart container
        self.temperatureChartWidget = qtw.QWidget(self.container)
        self.temperatureChartWidget.setFixedHeight(500)
        self.temperatureChartLayout = qtw.QVBoxLayout(self.temperatureChartWidget)
        self.temperatureChartLayout.setContentsMargins(0, 0, 0, 0)
        self.temperatureChartLayout.setSpacing(0)
        self.containerLayout.addWidget(self.temperatureChartWidget)
        # Create a QChart
        self.chartTemperature = QChart()
        self.chartTemperature.setTitle("Données des capteurs de température.")

        # Create a QLineSeries
        self.seriesTemperatureCuisine = QLineSeries()
        self.seriesTemperatureCuisine.setName("Cuisine")
        for temp, timestamp in self.tempCuisine:
            dt = QDateTime(timestamp)
            self.seriesTemperatureCuisine.append(dt.toMSecsSinceEpoch(), temp)
        self.chartTemperature.addSeries(self.seriesTemperatureCuisine)

        self.seriesTemperatureCoucher = QLineSeries()
        self.seriesTemperatureCoucher.setName("Chambre à coucher")
        for temp, timestamp in self.tempCoucher:
            dt = QDateTime(timestamp)
            self.seriesTemperatureCoucher.append(dt.toMSecsSinceEpoch(), temp)
        self.chartTemperature.addSeries(self.seriesTemperatureCoucher)

        # Create X-Axis (time)
        self.tempAxisX = QDateTimeAxis()
        self.tempAxisX.setFormat("hh:mm:ss")
        self.tempAxisX.setTitleText("Temps")
        self.tempAxisX.setTickCount(10)
        # Create Y-Axis (temperature)
        self.tempAxisY = QValueAxis()
        self.tempAxisY.setTitleText("Temperature (°C)")
        self.tempAxisY.setLabelFormat("%.1f")  # Format to 1 decimal place
        self.tempAxisY.setTickCount(10)  # Number of labels on Y-axis
        # Attach axes to chart
        self.chartTemperature.addAxis(self.tempAxisX, QtCore.Qt.AlignBottom)
        self.chartTemperature.addAxis(self.tempAxisY, QtCore.Qt.AlignLeft)

        # Attach axes to serires
        self.seriesTemperatureCoucher.attachAxis(self.tempAxisX)
        self.seriesTemperatureCoucher.attachAxis(self.tempAxisY)
        self.seriesTemperatureCuisine.attachAxis(self.tempAxisX)
        self.seriesTemperatureCuisine.attachAxis(self.tempAxisY)

        # Create a QChartView
        self.chartTemperatureView = QChartView(self.chartTemperature)
        self.chartTemperatureView.setRenderHint(QPainter.Antialiasing)

        self.tempChartUpdate()

        # Add the QChartView to the layout
        self.temperatureChartLayout.addWidget(self.chartTemperatureView)

    def tempChartUpdate(self):
        if not self.tempCuisine and not self.tempCoucher:
            return

        if self.tempCuisine:
            min_time_cuisine = min(self.tempCuisine, key=lambda x: x[1])[1]
            max_time_cuisine = max(self.tempCuisine, key=lambda x: x[1])[1]
        else:
            min_time_cuisine = max_time_cuisine = None

        if self.tempCoucher:
            min_time_coucher = min(self.tempCoucher, key=lambda x: x[1])[1]
            max_time_coucher = max(self.tempCoucher, key=lambda x: x[1])[1]
        else:
            min_time_coucher = max_time_coucher = None

        min_time = min(filter(None, [min_time_cuisine, min_time_coucher]))
        max_time = max(filter(None, [max_time_cuisine, max_time_coucher]))

        # Y axis
        if self.tempCuisine and self.tempCoucher:
            min_temp = min(
                min(self.tempCuisine, key=lambda x: x[0])[0],
                min(self.tempCoucher, key=lambda x: x[0])[0],
            )
            max_temp = max(
                max(self.tempCuisine, key=lambda x: x[0])[0],
                max(self.tempCoucher, key=lambda x: x[0])[0],
            )
        elif self.tempCuisine:
            min_temp = min(self.tempCuisine, key=lambda x: x[0])[0]
            max_temp = max(self.tempCuisine, key=lambda x: x[0])[0]
        elif self.tempCoucher:
            min_temp = min(self.tempCoucher, key=lambda x: x[0])[0]
            max_temp = max(self.tempCoucher, key=lambda x: x[0])[0]
        else:
            min_temp = max_temp = 0

        self.tempAxisY.setMin(min_temp - 1)  # Add some padding
        self.tempAxisY.setMax(max_temp + 1)

        self.tempAxisX.setMin(QDateTime(min_time))
        self.tempAxisX.setMax(QDateTime(max_time))

        self.chartTemperatureView.update()


if __name__ == "__main__":
    pass
