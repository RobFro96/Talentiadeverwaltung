import logging
import typing

from util.column_range import ColumnRange
from util.table import Table


class TableReader:
    @classmethod
    def from_settings(cls, table: Table, settings, prefix: str):
        header_row = settings[prefix + "_header"]
        columns = settings[prefix + "_columns"]
        required_columns = settings[prefix + "_required"] or []
        date_columns = settings[prefix + "_date_columns"] or []

        return cls(table, header_row, columns, required_columns, date_columns)

    def __init__(self, table: Table, header_row: int, columns: ColumnRange,
                 required_columns: typing.List[str] = None, date_columns: typing.List[str] = None):
        self.table = table
        self.header_row = header_row
        self.columns: ColumnRange = columns
        self.required_columns = required_columns or []
        self.date_columns = date_columns or []

        self.headers = []

    def read(self, line_callback: typing.Callable[[int, typing.Dict], None]):
        self.headers = self.get_header()

        if not self.check_required_columns():
            return False

        row = self.header_row + 1
        success = True

        while success:
            row_data, success = self.read_row(row)

            if success:
                line_callback(row, row_data)

            row += 1

        return True

    def get_header(self):
        return [str(self.table.worksheet.cell(self.header_row, col).value).strip()
                for col in self.columns.range()]

    def read_row(self, row: int):
        row_data = {}
        success = True
        for i, col in enumerate(self.columns.range()):
            value = self.table.worksheet.cell(row, col).value
            header = self.headers[i]

            if header == str(None):
                continue

            if isinstance(value, str):
                value = value.strip()

            row_data[header] = value
            if header in self.required_columns and value is None:
                success = False

        return row_data, success

    def check_required_columns(self):
        for header in self.required_columns:
            if not header in self.headers:
                logging.error("Pflichtspalte %s existiert nicht in der Tabelle %s.",
                              header, self.table.filename)
                return False
        return True

    def write(self, data: typing.List[typing.Dict[str, typing.Any]]):
        self.headers = self.get_header()

        row = self.header_row + 1

        for row_data in data:
            self.write_row(row, row_data)
            row += 1

    def write_row(self, row, row_data):
        for i, header in enumerate(self.headers):
            col = self.columns.id(i)

            if header in row_data:
                self.table.worksheet.cell(row, col).value = row_data[header]
                if header in self.date_columns:
                    self.table.worksheet.cell(row, col).number_format = "DD.MM.YYYY"
