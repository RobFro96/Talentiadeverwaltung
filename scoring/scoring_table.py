"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging
import time

from data.database import Database
from data.database_sclasses import SCLASS_WORKSHEET
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class ScoringTable(Table):
    """Auswertungstabelle
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 progress: ProgressTask = None):
        """Konstruktor

        Args:
            competition_folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.
        """
        self.settings = settings
        self.database = database
        self.progress = progress
        self.table_reader: TableReader = None

        Table.__init__(self, competition_folder, self.settings["scoring_template"])

    def write(self, folder=None, filename=None) -> bool:
        """Schreiben der Tabelle

        Args:
            folder (str, optional): Ordner. Defaults to None.
            filename (str, optional): Dateiname. Defaults to None.

        Returns:
            bool: True, wenn erfolgreich
        """
        generated_filename = self.settings["scoring_output"] % {"time": time.strftime("%H%M")}
        filename = filename or generated_filename

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "scoring")
            for sclass in self.database.get_sclasses():
                self.__fill_worksheet(sclass)

                if self.progress:
                    self.progress.inc_value()

            return Table.write(self, folder, filename)
        except:
            logging.exception("Fehler beim Erstellen der Auswertung.")
            return False

    def __fill_worksheet(self, sclass):
        """Ausfüllen des entsprechenden Arbeitsblattes

        Args:
            sclass (typing.Dict): Wertungsklasse
        """
        self.set_worksheet(sclass[SCLASS_WORKSHEET])

        data = self.database.get_attendees_in_sclass(sclass)
        self.table_reader.write(data)
        self.set_footer(settings=self.settings, center="Auswertung")
