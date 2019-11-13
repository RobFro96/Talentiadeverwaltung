import os
import enum
from util.table import Table
from util.error_collector import ErrorCollector, ErrorType
import openpyxl
import numbers

class ValueType(enum.IntEnum):
    STRING = 0
    NUMBER = 1
    COLUMN_RANGE = 2

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
ERROR_3 = "Fehler beim Lesen der Einstellungstabelle. Leere Zeichenkette in Zelle %s."

class ColumnRange:
    def __init__(self, start:str , end:str):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return "%s-%s" % (self.start, self.end)

def create_column_range(string: str) -> ColumnRange:
    splitted = string.split("-")

    if len(splitted) != 2:
        return None
    
    return ColumnRange(splitted[0], splitted[1])

class SettingsTable(Table):
    def __init__(self, competition_folder: str):
        Table.__init__(self, competition_folder, FILENAME)
        self.settings = {}
        self.worksheet: openpyxl.worksheet.worksheet.Worksheet = None

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
            value = self.worksheet[value_property["cell"]].value
            
            if value_property["type"] == ValueType.NUMBER:
                if not isinstance(value, numbers.Number):
                    errors.append(ErrorType.WARNING, ERROR_1 % value_property["cell"])
                    self.settings[value_name] = 1
                else:
                    self.settings[value_name] = value
            
            elif value_property["type"] == ValueType.COLUMN_RANGE:
                cr = create_column_range(value)
                if not cr:
                    errors.append(ErrorType.WARNING, ERROR_2 % value_property["cell"])
                    self.settings[value_name] = ColumnRange("A", "A")
                else:
                    self.settings[value_name] = cr
            
            elif value_property["type"] == ValueType.STRING:
                if not value:
                    errors.append(ErrorType.WARNING, ERROR_3 % value_property["cell"])
                    self.settings[value_name] = ""
                else:
                    self.settings[value_name] = value