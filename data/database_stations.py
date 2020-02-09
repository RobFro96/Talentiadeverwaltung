import typing

STATION_NAME = "Station"
STATION_SHORT = "Kürzel"
STATION_COLUMNS = "Spalten"


class DatabaseStations:
    def __init__(self):
        self.stations: typing.List[typing.Dict[str, typing.Any]] = []

    def clear_stations(self):
        self.stations = []

    def append_station(self, station):
        self.stations.append(station)

    def get_stations(self):
        return self.stations

    def get_all_station_scoring_columns(self):
        result = []
        for station in self.stations:
            columns_list = [element.strip() for element in str(station[STATION_COLUMNS]).split(',')]
            result += columns_list

        return result
