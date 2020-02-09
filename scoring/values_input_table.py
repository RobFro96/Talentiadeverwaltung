"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging
import typing

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_COLUMNS, STATION_SHORT
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class ValuesInputTable(Table):
    """Klasse zum Einlesen der Wertetabellen
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 station, group):
        """Konstruktor.

        Args:
            competition_folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
            station (typing.Dict): Station
            group (typing.Dict): Riege
        """
        self.settings = settings
        self.database = database
        self.station = station
        self.group = group
        self.table_reader: TableReader = None
        self.status = logging.INFO

        filename = self.settings["values_input_file"] % {
            "station": self.station[STATION_SHORT], "riege": self.group[GROUP_NAME]}
        Table.__init__(self, competition_folder, filename)

    def open(self) -> bool:
        """Öffnen der Tabelle und Auslesen der Werte

        Returns:
            bool: True, wenn erfolgreich
        """
        if not Table.open(self):
            self.status = logging.ERROR
            return False

        try:
            reader = TableReader.from_settings(self, self.settings, "values_input")
            if not reader.read(self.process_row):
                self.status = logging.ERROR
        except:
            logging.exception("Fehler beim Auslesen der Daten aus der Tabelle %s", self.filename)
            self.status = logging.ERROR
            return False
        return True

    def process_row(self, row: int, row_data: typing.Dict[str, typing.Any]):
        """Methode zum Auslesen einer Zeile

        Args:
            row (int): Zeilennummer
            row_data (typing.Dict[str, typing.Any]): Daten der Zeile
        """
        attendee = self.database.filter_attendee(row_data, self.settings["values_input_required"])
        if not attendee:
            logging.warning("Zeile %d der Datei %s konnte nicht eindeutig zugewiesen werden.",
                            row, self.filename)
            self.status = logging.WARNING
            return

        for key, value in row_data.items():
            if key in self.station[STATION_COLUMNS]:
                attendee[key] = value
