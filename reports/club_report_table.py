from database.database import Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector, ErrorType
from util.table import Table

ERROR_OPENING = "Vorlage der Vereinsübersicht %s kann nicht geöffnet werden."
ERROR_SAVING = "Vereinsübersicht %s konnte nicht gespeichert werden."

class ClubReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, errors: ErrorCollector):
        self.settings = settings
        self.errors = errors
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["clubs_template"])
    
    def open(self):
        if not Table.open(self):
            self.errors.append(ErrorType.ERROR, ERROR_OPENING % self.filename)
            return
    
    def write(self):
        if not Table.write(self, None, self.settings["clubs_output"]):
            self.errors.append(ErrorType.ERROR, ERROR_SAVING % self.filename)
            return
    
    def create(self, database: Database, errors: ErrorCollector):
        self.table_reader = TableReader(self, errors).from_settings(self.settings, "clubs", False)

        for club in database.get_clubs():
            self.__create_worksheet(club, database)
        
        self.workbook.remove_sheet(self.__get_template_sheet())

    def __create_worksheet(self, club: str, database: Database):
        self.worksheet = self.workbook.copy_worksheet(self.__get_template_sheet())
        self.worksheet.title = club
        self.table_reader.set_worksheet(self.worksheet)

        data = database.get_club_overview(club)
        self.table_reader.write(data)

        self.worksheet[self.settings["clubs_cell_clubname"]].value = club

    def __get_template_sheet(self):
        return self.workbook.worksheets[self.settings["clubs_worksheet"] - 1]
