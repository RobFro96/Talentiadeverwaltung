import logging

from database.database import Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table


class AttendeesTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable):
        self.settings = settings
        Table.__init__(self, competition_folder,
                       self.settings["attendees_file"])

    def open(self):
        if not Table.open(self):
            logging.error("Meldungsdatei %s kann nicht geöffnet werden.",
                          self.filename)
            return

    def read_to_database(self, database: Database):
        table_reader = TableReader(self).from_settings(
            self.settings, "attendees")
        database.read_attendees_table(table_reader)
