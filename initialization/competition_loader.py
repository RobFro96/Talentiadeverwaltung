import logging
import os
import tkinter

from data.attendees_table import AttendeesTable
from data.database import Database
from initialization.competition import Competition
from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector

LAST_COMP_FILE = ".last_competition"
FOLDER_DIALOG_TITLE = "Ordner der Veranstaltung auswählen"


class CompetitionLoader:
    def read_last_path(self) -> str:
        if not os.path.exists(LAST_COMP_FILE):
            logging.warning("Datei .last_competition exisitiert nicht.")
            return None

        try:
            with open(LAST_COMP_FILE, "r", encoding="utf-8") as file:
                return file.readline()
        except IOError:
            logging.exception("Fehler beim Lesen der Datei .last_competition.")
            return None

    def open_dialog(self, initial_dir: str) -> str:
        return tkinter.filedialog.askdirectory(
            initialdir=initial_dir,
            title=FOLDER_DIALOG_TITLE)

    def load(self, folder: str) -> Competition:
        errors = ErrorCollector()

        # Ordner überprüfen
        if not os.path.isdir(folder):
            logging.error("Angegebner Ordner %s existiert nicht.", folder)
            return None

        # Einstellungen lesen
        settings = SettingsTable(folder)
        settings.open()
        if errors.has_error():
            errors.remove()
            return None

        # Datenbank erstellen, Gruppen und Stationen auslesen
        database = Database(settings)
        settings.read_groups(database)
        settings.read_stations(database)
        if errors.has_error():
            errors.remove()
            return None

        # Meldung auslesen
        attendees_table = AttendeesTable(folder, settings, database)
        attendees_table.open()
        if errors.has_error():
            errors.remove()
            return None

        database.do_grouping()
        if errors.has_error():
            errors.remove()
            return None

        return Competition(folder, settings, database)
