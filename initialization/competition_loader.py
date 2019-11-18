import os
import tkinter

from database.attendees_table import AttendeesTable
from database.database import Database
from initialization.competition import Competition
from initialization.settings_table import SettingsTable
from util.error_collector import (ErrorCollector, ErrorType, print_error,
                                  print_warning)

LAST_COMP_FILE = ".last_competition"
ERROR_1 = "Datei .last_competition exisitiert nicht."
ERROR_2 = "Fehler beim Lesen der Datei .last_competition."
FOLDER_DIALOG_TITLE = "Ordner der Veranstaltung auswählen"
ERROR_3 = "Angegebner Ordner %s existiert nicht."


class CompetitionLoader:
    def read_last_path(self) -> str:
        if not os.path.exists(LAST_COMP_FILE):
            print_warning(ERROR_1)
            return None

        try:
            with open(LAST_COMP_FILE, "r", encoding="utf-8") as file:
                return file.readline()
        except IOError:
            print_error(ERROR_2)
            return None

    def open_dialog(self, initial_dir: str) -> str:
        return tkinter.filedialog.askdirectory(
            initialdir=initial_dir,
            title=FOLDER_DIALOG_TITLE)

    def load(self, folder: str, errors: ErrorCollector) -> Competition:
        if not os.path.isdir(folder):
            errors.append(ErrorType.ERROR, ERROR_3 % folder)
            return None

        settings = SettingsTable(folder, errors)
        settings.open()
        if errors.has_error():
            return None

        database = Database(settings)
        settings.read_groups(database, errors)
        if errors.has_error():
            return None

        attendees_table = AttendeesTable(folder, settings, errors)
        attendees_table.open()
        if errors.has_error():
            return None

        attendees_table.read_to_database(database, errors)
        if errors.has_error():
            return None

        database.do_grouping(errors)
        if errors.has_error():
            return None

        return Competition(folder, settings, database)
