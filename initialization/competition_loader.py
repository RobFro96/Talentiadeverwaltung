import os
import tkinter

from util.error_collector import (ErrorCollector, ErrorType, print_error,
                                  print_warning)
from util.json_settings import JSONSettings

LAST_COMP_FILE = ".last_competition"
ERROR_1 = "Datei .last_competition exisitiert nicht."
ERROR_2 = "Fehler beim Lesen der Datei .last_competition."
FOLDER_DIALOG_TITLE = "Ordner der Veranstaltung auswählen"
ERROR_3 = "Angegebner Ordner %s existiert nicht."


class CompetitionLoader:
    def __init__(self, settings: JSONSettings):
        self.settings = settings

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

    def load(self, folder: str, errors: ErrorCollector):
        if not os.path.isdir(folder):
            errors.append(ErrorType.ERROR, ERROR_3 % folder)
            return None
