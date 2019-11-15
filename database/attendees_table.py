from util.table import Table
from util.error_collector import ErrorCollector, ErrorType
from initialization.settings_table import SettingsTable
from database.table_reader import TableReader

ERROR_OPENING = "Meldungsdatei %s kann nicht geöffnet werden."

class AttendeesTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable):
        self.settings = settings
        Table.__init__(self, competition_folder, self.settings["attendees_file"])
    
    def open(self, errors: ErrorCollector):
        if not Table.open(self):
            errors.append(ErrorType.ERROR, ERROR_OPENING % self.filename)
            return
        
        self.__read_database(errors)
    
    def __read_database(self, errors: ErrorCollector):
        table_reader = TableReader(self, errors).from_settings(self.settings, "attendees")
        table_reader.read()
        
