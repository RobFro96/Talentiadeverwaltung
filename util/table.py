import enum
import logging
import numbers
import os
import tkinter.messagebox

import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from util.cell import Cell
from util.column_range import ColumnRange

CLOSE_WARNING = "Die Datei %s ist gerade von einem anderen Programm geöffnet. Jetzt schließen?"


class ValueType(enum.Enum):
    STRING = 0
    NUMBER = 1
    COLUMN_RANGE = 2
    STRING_LIST = 3
    CELL = 4


class Table:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename

        self.workbook: Workbook = None
        self.worksheet: Worksheet = None

    def get_path(self):
        return os.path.join(self.folder, self.filename)

    def file_exists(self):
        return os.path.isfile(self.get_path())

    def open(self) -> bool:
        try:
            self.workbook = openpyxl.open(self.get_path())
            self.set_worksheet(0)
        except:
            logging.exception("Fehler beim Öffnen der Tabelle %s.", self.filename)
            return False
        return True

    def get_worksheet(self, index):
        if isinstance(index, int):
            if index >= 0 and index < len(self.workbook.worksheets):
                return self.workbook.worksheets[index]
            else:
                logging.error("Arbeitsblatt %d existiert nicht in der Tabelle %s",
                              index, self.filename)
        elif isinstance(index, str):
            if index in self.workbook.sheetnames:
                return self.workbook[index]
            else:
                logging.error("Arbeitsblatt %s existiert nicht in der Tabelle %s",
                              index, self.filename)
        else:
            logging.error("Unbekannter Datentyp in set_worksheet(%r) der Tabelle %s",
                          index, self.filename)
        return None

    def set_worksheet(self, index):
        self.worksheet = self.get_worksheet(index)

    def remove_worksheet(self, index):
        ws = self.get_worksheet(index)
        if ws:
            self.workbook.remove(ws)
        else:
            logging.error("Arbeitsblatt %s der Tabelle %s konnte nicht entfernt werden.",
                          index, self.filename)

    def copy_worksheet(self, index):
        ws = self.get_worksheet(index)
        if ws:
            self.worksheet = self.workbook.copy_worksheet(ws)
        else:
            logging.error("Arbeitsblatt %s der Tabelle %s konnte nicht kopiert werden.",
                          index, self.filename)

    def write(self, folder=None, filename=None) -> bool:
        folder = folder or self.folder
        filename = filename or self.filename
        path = os.path.join(folder, filename)

        self.check_lock(folder, filename)

        try:
            self.workbook.save(path)
        except:
            logging.exception("Fehler beim Speichern der Tabelle %s.", filename)
            return False
        return True

    def check_lock(self, folder, filename):
        path1 = os.path.join(folder, ".~lock." + filename + "#")
        path2 = os.path.join(folder, "~$" + filename)

        if os.path.exists(path1) or os.path.exists(path2):
            tkinter.messagebox.showwarning("Warnung", CLOSE_WARNING % filename)

    def get_value(self, cell, val_type: ValueType, default=None, log_errors=True):
        if val_type == ValueType.NUMBER:
            return self.get_number(cell, default, log_errors)
        if val_type == ValueType.COLUMN_RANGE:
            return self.get_col_range(cell, default, log_errors)
        if val_type == ValueType.STRING:
            return self.get_string(cell, default, log_errors)
        if val_type == ValueType.STRING_LIST:
            return self.get_string_list(cell, default, log_errors)
        if val_type == ValueType.CELL:
            return self.get_cell(cell, default, log_errors)

    @classmethod
    def convert_cell(cls, cell, log_errors=True):
        if isinstance(cell, str):
            return Cell.from_string(cell)
        if isinstance(cell, tuple):
            return Cell.from_row_col(*cell)
        if isinstance(cell, Cell):
            return cell

        if log_errors:
            logging.error("Angegebenes Objekt ist keine gültige Zelle: %r.", cell)
        return None

    def get_number(self, cell, default=None, log_errors=True):
        if default is None:
            default = 0

        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return default

        value = self.worksheet.cell(*cell.get()).value

        if isinstance(value, numbers.Number):
            return value
        if log_errors:
            logging.error("Zelle %s der Tabelle %s enthält keine Zahl.", cell, self.filename)
        return default

    def get_col_range(self, cell, default=None, log_errors=True):
        if default is None:
            default = ColumnRange.from_string("A-A")

        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return default

        value = self.worksheet.cell(*cell.get()).value
        value = ColumnRange.from_string(value)

        if value is not None:
            return value
        if log_errors:
            logging.error("Zelle %s der Tabelle %s enthält keinen Spaltenbereich.",
                          cell, self.filename)
        return default

    def get_string(self, cell, default=None, log_errors=True):
        if default is None:
            default = ""

        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return default

        value = self.worksheet.cell(*cell.get()).value

        if value is not None:
            return str(value)
        if log_errors:
            logging.error("Zelle %s der Tabelle %s enthält keine Zeichenkette.",
                          cell, self.filename)
        return default

    def get_string_list(self, cell, default=None, log_errors=True):
        if default is None:
            default = []

        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return default

        value = self.worksheet.cell(*cell.get()).value

        if value is not None:
            str_list = [element.strip() for element in str(value).split(',')]
            return str_list
        if log_errors:
            logging.error("Zelle %s der Tabelle %s enthält keine Liste.", cell, self.filename)
        return default

    def get_cell(self, cell, default=None, log_errors=True):
        if default is None:
            default = Cell.from_string("A1")

        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return default

        value = self.worksheet.cell(*cell.get()).value
        value = Cell.from_string(value)

        if value is not None:
            return value
        if log_errors:
            logging.error("Zelle %s der Tabelle %s enthält keine Zelle.", cell, self.filename)
        return default

    def set_value(self, cell, value, log_errors=True):
        cell = self.convert_cell(cell, log_errors)
        if cell is None:
            return

        self.worksheet.cell(*cell.get(), value)
