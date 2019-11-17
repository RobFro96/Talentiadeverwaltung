import typing

from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector, ErrorType
from util.table import ColumnRange, Table, Worksheet

ERROR_1 = "Angegebes Tabellenblatt %d exisitert nicht in der Tabelle %s."
ERROR_2 = "Pflichtspalte %s existiert nicht in der Tabelle %s."


class TableReader:
    def __init__(self, table: Table, errors: ErrorCollector):
        self.table = table
        self.errors = errors
        self.header_row: int = 1
        self.columns: ColumnRange = None
        self.required_columns = []

        self.worksheet: Worksheet = self.table.workbook.worksheets[0]
        self.headers = []

    def from_settings(self, settings: SettingsTable, prefix: str, set_required=True):
        self.set_worksheet_number(settings[prefix + "_worksheet"])
        self.set_header_row(settings[prefix + "_header"])
        self.set_columns(settings[prefix + "_columns"])

        if set_required:
            self.set_required_columns(settings[prefix + "_required"])

        return self

    def set_worksheet_number(self, number: int):
        if number > len(self.table.workbook.worksheets):
            self.errors.append(ErrorType.ERROR, ERROR_1 %
                               (number, self.table.filename))
        else:
            self.worksheet = self.table.workbook.worksheets[number - 1]
        return self
    
    def set_worksheet(self, worksheet: Worksheet):
        self.worksheet = worksheet

    def set_header_row(self, header_row: int):
        self.header_row = header_row
        return self

    def set_columns(self, columns: ColumnRange):
        self.columns = columns
        return self

    def set_required_columns(self, required_columns):
        self.required_columns = required_columns
        return self

    def read(self, line_callback: typing.Callable[[int, typing.Dict], None]):
        self.headers = self.__read_header()

        if not self.__required_columns_existing():
            return

        row = self.header_row + 1
        success = True

        while success:
            row_data, success = self.__read_row(row)

            if success:
                line_callback(row, row_data)

            row += 1

    def __read_header(self):
        return [str(self.worksheet.cell(self.header_row, col).value).strip()
                for col in self.columns.range()]

    def __read_row(self, row: int):
        row_data = {}
        success = True
        for i, col in enumerate(self.columns.range()):
            value = self.worksheet.cell(row, col).value
            header = self.headers[i]

            if isinstance(value, str):
                value = value.strip()

            row_data[header] = value
            if header in self.required_columns and value is None:
                success = False

        return row_data, success

    def __required_columns_existing(self):
        for header in self.required_columns:
            if not header in self.headers:
                self.errors.append(ErrorType.ERROR, ERROR_2 %
                                   (header, self.table.filename))
                return False
        return True

    def write(self, data: typing.List[typing.Dict[str, typing.Any]]):
        self.headers = self.__read_header()

        row = self.header_row + 1

        for row_data in data:
            self.__write_row(row, row_data)
            row += 1

    def __write_row(self, row, row_data):
        for i, header in enumerate(self.headers):
            col = self.columns.id(i)

            if header in row_data:
                self.worksheet.cell(row, col).value = row_data[header]
                if header == "Geburtstag":
                    self.worksheet.cell(row, col).number_format = "DD.MM.YYYY"
