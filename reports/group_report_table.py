import logging

from data.database import GROUP_NAME, Database
from util.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table

WORKSHEET_TITLE = "Riege %s"
TEMPLATE_SHEET_NAME = "Vorlage"


class GroupReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database):
        self.settings = settings
        self.database = database
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["groups_template"])

    def write(self, folder=None, filename=None) -> bool:
        filename = filename or self.settings["groups_output"]

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "groups")
            for group in self.database.get_groups():
                self.__create_worksheet(group)

            self.remove_worksheet(TEMPLATE_SHEET_NAME)

            return Table.write(self, folder, filename)
        except:
            logging.exception("Fehler beim Erstellen der Riegenübersicht.")
            return False

    def __create_worksheet(self, group):
        self.copy_worksheet(TEMPLATE_SHEET_NAME)
        self.worksheet.title = WORKSHEET_TITLE % str(group[GROUP_NAME])

        data = self.database.get_group_overview(group)
        self.table_reader.write(data)

        self.set_value(self.settings["groups_cell_groupname"], str(group[GROUP_NAME]))
