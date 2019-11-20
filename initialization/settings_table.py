from database.database import Database
from database.table_reader import TableReader
from util.error_collector import ErrorCollector, ErrorType
from util.table import Table, ValueType, create_column_range

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
    "clubs_worksheet": {"cell": "B15", "type": ValueType.NUMBER},
    "clubs_header": {"cell": "B16", "type": ValueType.NUMBER},
    "clubs_columns": {"cell": "B17", "type": ValueType.COLUMN_RANGE},
    "clubs_cell_clubname": {"cell": "B18", "type": ValueType.STRING},
    "age_classifier": {"cell": "B21", "type": ValueType.STRING},
    "group_sort_before": {"cell": "B22", "type": ValueType.STRING_LIST},
    "group_sort_after": {"cell": "B23", "type": ValueType.STRING_LIST},
    "groups_template": {"cell": "B26", "type": ValueType.STRING},
    "groups_output": {"cell": "B27", "type": ValueType.STRING},
    "groups_worksheet": {"cell": "B28", "type": ValueType.NUMBER},
    "groups_header": {"cell": "B29", "type": ValueType.NUMBER},
    "groups_columns": {"cell": "B30", "type": ValueType.COLUMN_RANGE},
    "groups_cell_groupname": {"cell": "B31", "type": ValueType.STRING},
    "stations_template": {"cell": "B34", "type": ValueType.STRING},
    "stations_output": {"cell": "B35", "type": ValueType.STRING},
    "stations_header": {"cell": "B36", "type": ValueType.NUMBER},
    "stations_columns": {"cell": "B37", "type": ValueType.COLUMN_RANGE},
    "stations_cell_groupname": {"cell": "B38", "type": ValueType.STRING},
}

ERROR_OPENING = "Einstellungsdatei kann nicht geöffnet werden."

VALUE_ERRORS = {
    ValueType.NUMBER: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird eine Zahl erwartet.",
    ValueType.COLUMN_RANGE: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird ein Spaltenbereich erwartet.",
    ValueType.STRING: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer.",
    ValueType.STRING_LIST: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer."
}

GROUP_WORKSHEET = 2
GROUP_HEADER = 2
GROUP_COLUMNS = "A-C"
GROUP_REQUIRED = ["Riegenname", "Altersklassen"]

STATION_WORKSHEET = 3
STATION_HEADER = 2
STATION_COLUMNS = "A-B"
STATION_REQUIRED = ["Station", "Kürzel"]


class SettingsTable(Table):
    def __init__(self, competition_folder: str, errors: ErrorCollector):
        Table.__init__(self, competition_folder, FILENAME)
        self.settings = {}
        self.errors = errors

    def open(self):
        self.settings = {}
        if not Table.open(self):
            self.errors.append(ErrorType.ERROR, ERROR_OPENING)
            return

        self.__read_settings()

    def __read_settings(self):
        self.worksheet = self.workbook.worksheets[WORKSHEET]

        for value_name, value_property in SETTINGS.items():
            self.settings[value_name], success = self.get_value(
                value_property["cell"], value_property["type"])

            if not success:
                self.errors.append(
                    ErrorType.WARNING, VALUE_ERRORS[value_property["type"]] % value_property["cell"])

    def __getitem__(self, key):
        if key in self.settings:
            return self.settings[key]
        return None

    def read_groups(self, database: Database, errors: ErrorCollector):
        reader = TableReader(self, errors) \
            .set_worksheet_number(GROUP_WORKSHEET) \
            .set_header_row(GROUP_HEADER) \
            .set_columns(create_column_range(GROUP_COLUMNS)) \
            .set_required_columns(GROUP_REQUIRED)

        database.read_group_table(reader, errors)

    def read_stations(self, database: Database, errors: ErrorCollector):
        reader = TableReader(self, errors) \
            .set_worksheet_number(STATION_WORKSHEET) \
            .set_header_row(STATION_HEADER) \
            .set_columns(create_column_range(STATION_COLUMNS)) \
            .set_required_columns(STATION_REQUIRED)

        database.read_station_table(reader, errors)
