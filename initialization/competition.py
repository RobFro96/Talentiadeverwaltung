import tkinter

from database.database import Database
from gui.main_form import ExitReason, MainForm
from initialization.settings_table import SettingsTable


class Competition:
    def __init__(self, settings: SettingsTable, database: Database):
        self.settings = settings
        self.database = database
        self.main_form: MainForm = None

    def open_gui(self, root: tkinter.Tk) -> ExitReason:
        self.main_form = MainForm(self)
        return self.main_form.open(root)

    def get_name(self):
        return self.settings["competition_name"]
