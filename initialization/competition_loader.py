"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
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
    """Klasse zum Erstellen einer Anwendung
    """

    @classmethod
    def read_last_path(cls) -> str:
        """Lesen der verstecken Datei, die den Pfad zur zuletzt geöffneten Veranstaltung enthält

        Returns:
            str: Pfad der letzten Veranstaltung
        """
        if not os.path.exists(LAST_COMP_FILE):
            logging.warning("Datei .last_competition exisitiert nicht.")
            return None

        try:
            with open(LAST_COMP_FILE, "r", encoding="utf-8") as file:
                return file.readline()
        except IOError:
            logging.exception("Fehler beim Lesen der Datei .last_competition.")
            return None

    @classmethod
    def write_last_path(cls, path: str):
        try:
            with open(LAST_COMP_FILE, "w", encoding="utf-8") as file:
                file.write(path)
        except IOError:
            logging.exception("Fehler beim Schreiben der Datei .last_competition.")
            return None

    @classmethod
    def open_dialog(cls, initial_dir: str) -> str:
        """Öffnen des Dialogfensters zum Öffnen einer neuen Veranstaltung

        Args:
            initial_dir (str): Ordner mit dem das Dialogfenster startet

        Returns:
            str: Ausgewählter Ordner
        """
        return tkinter.filedialog.askdirectory(
            initialdir=initial_dir,
            title=FOLDER_DIALOG_TITLE)

    @classmethod
    def load(cls, folder: str) -> Competition:
        """Laden der Veranstaltung

        Args:
            folder (str): Ordner der Veranstaltung

        Returns:
            Competition: Veranstaltung
        """
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
        settings.read_sclasses(database)
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
