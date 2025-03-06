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

TEMPLATE_SHEET_NAME = "Vorlage"


class ClubReportTable(Table):
    """Tabelle der Vereinsübersicht
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database):
        """Konstruktor.

        Args:
            competition_folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
        """
        self.settings = settings
        self.database = database
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["clubs_template"])

    def write(self, folder=None, filename=None) -> bool:
        """Schreiben der Tabelle

        Args:
            folder (str, optional): Ordner. Defaults to None.
            filename (str, optional): Dateiname. Defaults to None.

        Returns:
            bool: True, wenn erfolgreich
        """
        filename = filename or self.settings["clubs_output"]

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "clubs")
            for club in self.database.get_clubs():
                self.__create_worksheet(club)

            self.remove_worksheet(TEMPLATE_SHEET_NAME)

            return Table.write(self, folder, filename)
        except:
            logging.exception("Fehler beim Erstellen der Vereinsübersicht.")
            return False

    def __create_worksheet(self, club: str):
        """Erstellen des Arbeitsblatts des angegebenen Vereins

        Args:
            club (str): Verein
        """
        self.copy_worksheet(TEMPLATE_SHEET_NAME)
        self.worksheet.title = club

        self.database.sort_attendees(["ID"])
        data = self.database.get_club_overview(club)
        self.table_reader.write(data)

        self.set_value(self.settings["clubs_cell_clubname"], club)
        self.set_footer(settings=self.settings, center="Vereinsübersicht")
