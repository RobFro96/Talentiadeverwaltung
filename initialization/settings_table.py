import os
import enum
from util.table import Table, ValueType
from util.error_collector import ErrorCollector, ErrorType
import openpyxl
import numbers

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
    "attendees_required": {"cell": "B15", "type": ValueType.STRING_LIST}
}

ERROR_OPENING = "Einstellungsdatei kann nicht geöffnet werden."

VALUE_ERRORS = {
    ValueType.NUMBER: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird eine Zahl erwartet.",
    ValueType.COLUMN_RANGE: "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird ein Spaltenbereich erwartet.",
    ValueType.STRING: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer.",
    ValueType.STRING_LIST: "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer."
}

class SettingsTable(Table):
    def __init__(self, competition_folder: str):
        Table.__init__(self, competition_folder, FILENAME)
        self.settings = {}

    def open(self, errors: ErrorCollector):
        self.settings = {}
        if not Table.open(self):
            errors.append(ErrorType.ERROR, ERROR_OPENING)
            return

        self.__read_settings(errors)

    def __read_settings(self, errors: ErrorCollector):
        self.worksheet = self.workbook.worksheets[WORKSHEET]

        for value_name, value_property in SETTINGS.items():
            self.settings[value_name], success = self.get_value(
                value_property["cell"], value_property["type"])

            if not success:
                errors.append(ErrorType.WARNING, VALUE_ERRORS[value_property["type"]] % value_property["cell"])
    
    def __getitem__(self, key):
        if key in self.settings:
            return self.settings[key]
        return None
