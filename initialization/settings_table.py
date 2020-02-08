import logging

from data.database import Database
from data.table_reader import TableReader
from util.column_range import ColumnRange
from util.table import Table, ValueType

FILENAME = "Einstellungen.xlsx"
WORKSHEET = 0
SETTINGS = {
    "competition_name": {"cell": "B2", "type": ValueType.STRING},
    "competition_date": {"cell": "B3", "type": ValueType.STRING},
    "attendees_file": {"cell": "B6", "type": ValueType.STRING},
    "attendees_worksheet": {"cell": "B7", "type": ValueType.NUMBER},
    "attendees_header": {"cell": "B8", "type": ValueType.NUMBER},
    "attendees_columns": {"cell": "B9", "type": ValueType.COLUMN_RANGE},
    "attendees_required": {"cell": "B10", "type": ValueType.STRING_LIST},
    "clubs_template": {"cell": "B13", "type": ValueType.STRING},
    "clubs_output": {"cell": "B14", "type": ValueType.STRING},
    "clubs_header": {"cell": "B15", "type": ValueType.NUMBER},
    "clubs_columns": {"cell": "B16", "type": ValueType.COLUMN_RANGE},
    "clubs_date_columns": {"cell": "B17", "type": ValueType.STRING_LIST},
    "clubs_cell_clubname": {"cell": "B18", "type": ValueType.CELL},
    "age_classifier": {"cell": "B21", "type": ValueType.STRING},
    "group_sort_before": {"cell": "B22", "type": ValueType.STRING_LIST},
    "group_sort_after": {"cell": "B23", "type": ValueType.STRING_LIST},
    "groups_template": {"cell": "B26", "type": ValueType.STRING},
    "groups_output": {"cell": "B27", "type": ValueType.STRING},
    "groups_header": {"cell": "B28", "type": ValueType.NUMBER},
    "groups_columns": {"cell": "B29", "type": ValueType.COLUMN_RANGE},
    "groups_cell_groupname": {"cell": "B30", "type": ValueType.CELL},
    "stations_template": {"cell": "B33", "type": ValueType.STRING},
    "stations_output": {"cell": "B34", "type": ValueType.STRING},
    "stations_header": {"cell": "B35", "type": ValueType.NUMBER},
    "stations_columns": {"cell": "B36", "type": ValueType.COLUMN_RANGE},
    "stations_cell_groupname": {"cell": "B37", "type": ValueType.STRING},
    "values_template": {"cell": "B40", "type": ValueType.STRING},
    "values_output": {"cell": "B41", "type": ValueType.STRING},
    "values_header": {"cell": "B42", "type": ValueType.NUMBER},
    "values_columns": {"cell": "B43", "type": ValueType.COLUMN_RANGE},
    "values_cell_groupname": {"cell": "B44", "type": ValueType.STRING},
}

GROUP_WORKSHEET = 1
GROUP_HEADER = 2
GROUP_COLUMNS = ColumnRange.from_string("A-C")
GROUP_REQUIRED = ["Riegenname", "Altersklassen"]

STATION_WORKSHEET = 2
STATION_HEADER = 2
STATION_COLUMNS = ColumnRange.from_string("A-B")
STATION_REQUIRED = ["Station", "Kürzel"]


class SettingsTable(Table):
    def __init__(self, competition_folder: str):
        Table.__init__(self, competition_folder, FILENAME)
        self.settings = {}

    def open(self):
        try:
            self.settings = {}
            if not Table.open(self):
                return

            self.__read_settings()
        except:
            logging.exception("Fehler beim Lesen der Einstellungsdatei.")

    def __read_settings(self):
        self.worksheet = self.workbook.worksheets[WORKSHEET]

        for value_name, value_property in SETTINGS.items():
            self.settings[value_name] = self.get_value(
                value_property["cell"], value_property["type"])

    def __getitem__(self, key):
        if key in self.settings:
            return self.settings[key]
        return None

    def read_groups(self, database: Database):
        try:
            self.set_worksheet(GROUP_WORKSHEET)
            reader = TableReader(self, GROUP_HEADER, GROUP_COLUMNS, GROUP_REQUIRED)
            database.clear_groups()
            reader.read(lambda row, row_data: database.append_group(row_data))
        except:
            logging.exception("Fehler beim Lesen der Gruppen aus der Einstellungsdatei.")

    def read_stations(self, database: Database):
        try:
            self.set_worksheet(STATION_WORKSHEET)
            reader = TableReader(self, STATION_HEADER, STATION_COLUMNS, STATION_REQUIRED)
            database.clear_stations()
            reader.read(lambda row, row_data: database.append_station(row_data))
        except:
            logging.exception("Fehler beim Lesen der Gruppen aus der Einstellungsdatei.")
