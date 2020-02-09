"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging

from data.database import Database
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class AttendeesTable(Table):
    """Tabelle der Meldungen. Einlesen der Datenbank der Teilnehmer
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database):
        """Konstruktor

        Args:
            competition_folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
        """
        self.settings = settings
        self.database = database

        Table.__init__(self, competition_folder, self.settings["attendees_file"])

    def open(self) -> bool:
        """Öffnen der Tabelle
        Eintragen der Teilnehmer in die Datenbank
        Erstellen der Listen für Alter und Vereine in der Datenbank

        Returns:
            bool: True, wenn das Öffnen und Lesen der Daten erfolgreich war.
        """
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
