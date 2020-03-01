"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_SHORT
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class StationReportTable(Table):
    """Tabelle der Stationszettel
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 progress: ProgressTask = None):
        """Konstruktor.

        Args:
            competition_folder (str): Ordner
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.
        """
        self.settings = settings
        self.database = database
        self.progress = progress
        self.table_reader: TableReader = None

        Table.__init__(self, competition_folder, self.settings["stations_template"])

    def write(self, folder=None, filename=None) -> bool:
        """Schreiben der Tabelle

        Args:
            folder (str, optional): Ordner. Defaults to None.
            filename (str, optional): Dateiname. Defaults to None.

        Returns:
            bool: True, wenn erfolgreich
        """
        filename = filename or self.settings["stations_output"]

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "groups")
            for station in self.database.get_stations():
                for group in self.database.get_groups():
                    self.__create_worksheet(station, group)

                    if self.progress:
                        self.progress.inc_value()

            for station in self.database.get_stations():
                self.remove_worksheet(station[STATION_SHORT])
                if self.progress:
                    self.progress.inc_value()

            return Table.write(self, folder, filename)
        except:
            logging.exception("Fehler beim Erstellen der Stationsübersicht.")
            return False

    def __create_worksheet(self, station, group):
        """Erstellen des Tabellenblattes der entsprechenden Riege und Station

        Args:
            station (typing.Dict): Station
            group (typing.Dict): Gruppe
        """
        self.copy_worksheet(station[STATION_SHORT])
        self.worksheet.title = "%s-%s" % (station[STATION_SHORT], str(group[GROUP_NAME]))

        data = self.database.get_group_overview(group)
        self.table_reader.write(data)

        self.set_value(self.settings["stations_cell_groupname"], str(group[GROUP_NAME]))
        self.set_footer(settings=self.settings, center="Stationszettel")
