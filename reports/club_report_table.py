import logging

from database.database import Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table


class ClubReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable):
        self.settings = settings
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder,
                       self.settings["clubs_template"])

    def open(self):
        if not Table.open(self):
            logging.error("Vorlage der Vereinsübersicht %s kann nicht geöffnet werden.",
                          self.filename)
            return

    def write(self):
        if not Table.write(self, None, self.settings["clubs_output"]):
            logging.error("Die Vereinsübersicht %s kann nicht gespeichert werden.",
                          self.filename)
            return

    def create(self, database: Database,):
        self.table_reader = TableReader(self).from_settings(
            self.settings, "clubs", False)

        for club in database.get_clubs():
            self.__create_worksheet(club, database)

        self.workbook.remove_sheet(self.__get_template_sheet())

    def __create_worksheet(self, club: str, database: Database):
        self.worksheet = self.workbook.copy_worksheet(
            self.__get_template_sheet())
        self.worksheet.title = club
        self.table_reader.set_worksheet(self.worksheet)

        data = database.get_club_overview(club)
        self.table_reader.write(data)

        self.worksheet[self.settings["clubs_cell_clubname"]].value = club

    def __get_template_sheet(self):
        return self.workbook.worksheets[self.settings["clubs_worksheet"] - 1]
