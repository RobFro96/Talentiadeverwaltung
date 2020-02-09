import logging
import typing

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_COLUMNS, STATION_SHORT
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class ValuesInputTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 station, group):
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
        attendee = self.database.filter_attendee(row_data, self.settings["values_input_required"])
        if not attendee:
            logging.warning("Zeile %d der Datei %s konnte nicht eindeutig zugewiesen werden.",
                            row, self.filename)
            self.status = logging.WARNING
            return

        for key, value in row_data.items():
            if key in self.station[STATION_COLUMNS]:
                attendee[key] = value
