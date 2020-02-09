"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import typing

STATION_NAME = "Station"
STATION_SHORT = "Kürzel"
STATION_COLUMNS = "Spalten"


class DatabaseStations:
    """Datenbank der Stationen
    """

    def __init__(self):
        self.stations: typing.List[typing.Dict[str, typing.Any]] = []  # : Stationen

    def clear_stations(self):
        """Löschen aller Stationen
        """
        self.stations = []

    def append_station(self, station: typing.Dict[str, typing.Any]):
        """Hinzufügen einer Station zur Datenbank

        Args:
            station (typing.Dict[str, typing.Any]): Station
        """
        self.stations.append(station)

    def get_stations(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt alle Stationen der Datenbank zurück.

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Liste der Stationen
        """
        return self.stations

    def get_all_station_scoring_columns(self) -> typing.List[str]:
        """Gibt eine Liste aller Wertungsspalten aller Stationen zurück

        Returns:
            typing.List[str]: Liste der Spalten
        """
        result = []
        for station in self.stations:
            columns_list = [element.strip() for element in str(station[STATION_COLUMNS]).split(',')]
            result += columns_list

        return result
