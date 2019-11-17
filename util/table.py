import enum
import numbers
import os
import tkinter.messagebox

import openpyxl
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def column_letter_to_number(col_letter):
    if len(col_letter) == 1:
        return ALPHABET.index(col_letter.upper()) + 1
    else:
        first_digit = ALPHABET.index(col_letter[0].upper()) + 1
        second_digit = ALPHABET.index(col_letter[1].upper()) + 1
        return first_digit * 26 + second_digit


def column_number_to_letter(col_number):
    return ALPHABET[col_number - 1]


class ValueType(enum.IntEnum):
    STRING = 0
    NUMBER = 1
    COLUMN_RANGE = 2
    STRING_LIST = 3


class ColumnRange:
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

    def __repr__(self):
        return "%s-%s" % (self.start, self.end)

    def range(self):
        return range(column_letter_to_number(self.start), column_letter_to_number(self.end) + 1)


def create_column_range(string: str) -> ColumnRange:
    splitted = string.split("-")

    if len(splitted) != 2:
        return None

    return ColumnRange(splitted[0], splitted[1])


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
            tkinter.messagebox.showwarning(
                "Warnung", "Die Datei " + filename + " ist gerade von einem anderen Programm geöffnet.")

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
        else:
            return default, False

    def get_col_range(self, cell: str, default=None):
        if default is None:
            default = ColumnRange("A", "A")
        value = create_column_range(self.worksheet[cell].value)

        if value is not None:
            return value, True
        else:
            return default, False

    def get_string(self, cell: str, default=None):
        if default is None:
            default = ""
        value = self.worksheet[cell].value

        if value is not None:
            return str(value), True
        else:
            return default, False

    def get_string_list(self, cell: str, default=None):
        if default is None:
            default = []
        value = self.worksheet[cell].value

        if value is not None:
            str_list = [element.strip() for element in str(value).split(',')]
            return str_list, True
        else:
            return default, False
