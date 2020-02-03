import enum
import numbers
import os
import tkinter.messagebox

import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from util.column_range import ColumnRange

CLOSE_WARNING = "Die Datei %s ist gerade von einem anderen Programm geöffnet. Jetzt schließen?"


class ValueType(enum.IntEnum):
    STRING = 0
    NUMBER = 1
    COLUMN_RANGE = 2
    STRING_LIST = 3
    CELL = 4


class Table:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.path = os.path.join(folder, filename)
        self.workbook: Workbook = []
        self.worksheet: Worksheet = []

    def open(self) -> str:
        try:
            self.workbook = openpyxl.open(self.path)
        except:
            return False
        return True

    def write(self, folder=None, filename=None) -> str:
        if not folder:
            folder = self.folder
        if not filename:
            filename = self.filename
        path = os.path.join(folder, filename)

        self.check_lock(folder, filename)

        try:
            self.workbook.save(path)
        except:
            return False
        return True

    def check_lock(self, folder, filename):
        path1 = os.path.join(folder, ".~lock." + filename + "#")
        path2 = os.path.join(folder, "~$" + filename)

        if os.path.exists(path1) or os.path.exists(path2):
            tkinter.messagebox.showwarning("Warnung", CLOSE_WARNING % filename)

    def get_value(self, cell: str, val_type: ValueType, default=None):
        if val_type == ValueType.NUMBER:
            return self.get_number(cell, default)
        if val_type == ValueType.COLUMN_RANGE:
            return self.get_col_range(cell, default)
        if val_type == ValueType.STRING:
            return self.get_string(cell, default)
        if val_type == ValueType.STRING_LIST:
            return self.get_string_list(cell, default)

    def get_number(self, cell: str, default=None):
        if default is None:
            default = 0
        value = self.worksheet[cell].value

        if isinstance(value, numbers.Number):
            return value, True
        return default, False

    def get_col_range(self, cell: str, default=None):
        if default is None:
            default = ColumnRange.from_string("A-A")
        value = ColumnRange.from_string(self.worksheet[cell].value)

        if value is not None:
            return value, True
        return default, False

    def get_string(self, cell: str, default=None):
        if default is None:
            default = ""
        value = self.worksheet[cell].value

        if value is not None:
            return str(value), True
        return default, False

    def get_string_list(self, cell: str, default=None):
        if default is None:
            default = []
        value = self.worksheet[cell].value

        if value is not None:
            str_list = [element.strip() for element in str(value).split(',')]
            return str_list, True
        return default, False
