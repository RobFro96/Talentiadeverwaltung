import tkinter

from database.database import Database
from gui.main_form import ExitReason, MainForm
from initialization.settings_table import SettingsTable
from reports.club_report_table import ClubReportTable
from util.error_collector import ErrorCollector, ErrorType

CLUBS_SAVED = "Vereinsübersicht wurde erfolgreich erstellt."

class Competition:
    def __init__(self, folder: str, settings: SettingsTable, database: Database):
        self.folder = folder
        self.settings = settings
        self.database = database
        self.main_form: MainForm = None

    def open_gui(self, root: tkinter.Tk) -> ExitReason:
        self.main_form = MainForm(self)
        return self.main_form.open(root)

    def get_name(self):
        return self.settings["competition_name"]
    
    def on_report_club(self) -> ErrorCollector:
        errors = ErrorCollector()
        
        table = ClubReportTable(self.folder, self.settings, errors)
        table.open()
        if errors.has_error():
            return errors

        table.create(self.database, errors)
        if errors.has_error():
            return errors
        
        table.write()
        if not errors.has_error():
            errors.append(ErrorType.NONE, CLUBS_SAVED)


        return errors
