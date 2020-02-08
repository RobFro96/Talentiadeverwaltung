import logging

from data.database import Database
from data.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table


class AttendeesTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database):
        self.settings = settings
        self.database = database

        Table.__init__(self, competition_folder, self.settings["attendees_file"])

    def open(self) -> bool:
        if not Table.open(self):
            return False

        try:
            reader = TableReader.from_settings(self, self.settings, "attendees")

            self.database.clear_attendees()
            reader.read(lambda row, row_data: self.database.append_attendee(row_data))
            self.database.refresh_ages()
            self.database.refresh_clubs()
        except:
            logging.exception("Fehler beim Auslesen der Meldungen.")
            return False
        return True
