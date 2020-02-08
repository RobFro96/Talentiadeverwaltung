import typing

STATION_NAME = "Station"
STATION_SHORT = "Kürzel"


class DatabaseStations:
    def __init__(self):
        self.stations: typing.List[typing.Dict[str, typing.Any]] = []

    def clear_stations(self):
        self.stations = []

    def append_station(self, station):
        self.stations.append(station)

    def get_stations(self):
        return self.stations
