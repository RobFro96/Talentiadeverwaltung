import logging

from data.database import Database
from util.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table

TEMPLATE_SHEET_NAME = "Vorlage"


class ClubReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database):
        self.settings = settings
        self.database = database
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["clubs_template"])

    def write(self, folder=None, filename=None) -> bool:
        filename = filename or self.settings["clubs_output"]

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "clubs")
            for club in self.database.get_clubs():
                self.__create_worksheet(club)

            self.remove_worksheet(TEMPLATE_SHEET_NAME)

            return Table.write(self, folder, filename)
        except:
            logging.exception("Fehler beim Erstellen der Vereinsübersicht.")
            return False

    def __create_worksheet(self, club: str):
        self.copy_worksheet(TEMPLATE_SHEET_NAME)
        self.worksheet.title = club

        data = self.database.get_club_overview(club)
        self.table_reader.write(data)

        self.set_value(self.settings["clubs_cell_clubname"], club)
