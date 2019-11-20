from database.database import GROUP_NAME, Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector, ErrorType
from util.table import Table

ERROR_OPENING = "Vorlage der Riegenübersicht %s kann nicht geöffnet werden."
ERROR_SAVING = "Riegenübersicht %s konnte nicht gespeichert werden."
WORKSHEET_TITLE = "Riege %s"


class GroupReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, errors: ErrorCollector):
        self.settings = settings
        self.errors = errors
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder,
                       self.settings["groups_template"])

    def open(self):
        if not Table.open(self):
            self.errors.append(ErrorType.ERROR, ERROR_OPENING % self.filename)
            return

    def write(self):
        if not Table.write(self, None, self.settings["groups_output"]):
            self.errors.append(ErrorType.ERROR, ERROR_SAVING % self.filename)
            return

    def create(self, database: Database, errors: ErrorCollector):
        self.table_reader = TableReader(self, errors).from_settings(
            self.settings, "groups", False)

        for group in database.get_groups():
            self.__create_worksheet(group, database)

        self.workbook.remove_sheet(self.__get_template_sheet())

    def __get_template_sheet(self):
        return self.workbook.worksheets[self.settings["groups_worksheet"] - 1]

    def __create_worksheet(self, group, database: Database):
        self.worksheet = self.workbook.copy_worksheet(
            self.__get_template_sheet())
        self.worksheet.title = WORKSHEET_TITLE % str(group[GROUP_NAME])
        self.table_reader.set_worksheet(self.worksheet)

        data = database.get_group_overview(group)
        self.table_reader.write(data)

        self.worksheet[self.settings["groups_cell_groupname"]
                       ].value = str(group[GROUP_NAME])
