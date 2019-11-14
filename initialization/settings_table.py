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
    "login_file": {"cell": "B11", "type": ValueType.STRING},
    "login_worksheet": {"cell": "B12", "type": ValueType.NUMBER},
    "login_first_row": {"cell": "B13", "type": ValueType.NUMBER},
    "login_column_range": {"cell": "B14", "type": ValueType.COLUMN_RANGE},
}
ERROR_1 = "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird eine Zahl erwartet."
ERROR_2 = "Fehler beim Lesen der Einstellungstabelle. In Zelle %s wird ein Spaltenbereich erwartet."
ERROR_3 = "Fehler beim Lesen der Einstellungstabelle. Zelle %s ist leer."


class SettingsTable(Table):
    def __init__(self, competition_folder: str):
        Table.__init__(self, competition_folder, FILENAME)
        self.settings = {}

    def open(self, errors: ErrorCollector):
        self.settings = {}
        if not Table.open(self):
            errors.append(ErrorType.ERROR,
                          "Einstellungsdatei kann nicht geöffnet werden.")
            return

        self.__read_settings(errors)

    def __read_settings(self, errors: ErrorCollector):
        self.worksheet = self.workbook.worksheets[WORKSHEET]

        for value_name, value_property in SETTINGS.items():
            self.settings[value_name], success = self.get_value(
                value_property["cell"], value_property["type"])

            if not success:
                if value_property["type"] == ValueType.NUMBER:
                    errors.append(ErrorType.WARNING, ERROR_1 %
                                  value_property["cell"])
                elif value_property["type"] == ValueType.COLUMN_RANGE:
                    errors.append(ErrorType.WARNING, ERROR_2 %
                                  value_property["cell"])
                elif value_property["type"] == ValueType.STRING:
                    errors.append(ErrorType.WARNING, ERROR_3 %
                                  value_property["cell"])
