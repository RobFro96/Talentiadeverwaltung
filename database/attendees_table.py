from database.database import Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector, ErrorType
from util.table import Table

ERROR_OPENING = "Meldungsdatei %s kann nicht geöffnet werden."


class AttendeesTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, errors: ErrorCollector):
        self.settings = settings
        self.errors = errors
        Table.__init__(self, competition_folder,
                       self.settings["attendees_file"])

    def open(self):
        if not Table.open(self):
            self.errors.append(ErrorType.ERROR, ERROR_OPENING % self.filename)
            return

    def read_to_database(self, database: Database, errors: ErrorCollector):
        table_reader = TableReader(self, errors).from_settings(
            self.settings, "attendees")
        database.read_attendees_table(table_reader, errors)
