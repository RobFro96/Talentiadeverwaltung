from util.error_collector import ErrorCollector, ErrorType
from util.table import Table, ValueType

FILENAME = "Einstellungen.xlsx"
WORKSHEET = 0
SETTINGS = {
    "competition_name": {"cell": "B2", "type": ValueType.STRING},
    "competition_date": {"cell": "B3", "type": ValueType.STRING},
    "gender_male": {"cell": "B6", "type": ValueType.STRING},
    "gender_female": {"cell": "B7", "type": ValueType.STRING},
    "gender_any": {"cell": "B8", "type": ValueType.STRING},
    "attendees_file": {"cell": "B11", "type": ValueType.STRING},
    "attendees_worksheet": {"cell": "B12", "type": ValueType.NUMBER},
    "attendees_header": {"cell": "B13", "type": ValueType.NUMBER},
    "attendees_columns": {"cell": "B14", "type": ValueType.COLUMN_RANGE},
    "attendees_required": {"cell": "B15", "type": ValueType.STRING_LIST},
    "clubs_template": {"cell": "B18", "type": ValueType.STRING},
    "clubs_output": {"cell": "B19", "type": ValueType.STRING},
    "clubs_worksheet": {"cell": "B20", "type": ValueType.NUMBER},
    "clubs_header": {"cell": "B21", "type": ValueType.NUMBER},
    "clubs_columns": {"cell": "B22", "type": ValueType.COLUMN_RANGE},
    "clubs_cell_clubname": {"cell": "B23", "type": ValueType.STRING}
}

ERROR_OPENING = "Einstellungsdatei kann nicht geöffnet werden."

VALUE_ERRORS = {
    ValueType.NUMBER: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird eine Zahl erwartet.",
    ValueType.COLUMN_RANGE: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird ein Spaltenbereich erwartet.",
    ValueType.STRING: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer.",
    ValueType.STRING_LIST: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer."
}

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
                self.errors.append(ErrorType.WARNING, VALUE_ERRORS[value_property["type"]] % value_property["cell"])
    
    def __getitem__(self, key):
        if key in self.settings:
            return self.settings[key]
        return None
