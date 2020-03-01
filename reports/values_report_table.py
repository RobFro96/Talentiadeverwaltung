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
from initialization.settings_table import SettingsTable
from util.table import Table
from util.table_reader import TableReader


class ValuesReportTable(Table):
    """Tabelle der Wertetabellen
    """

    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 station, group):
        """Konstruktor.

        Args:
            competition_folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
            station (typing.Dict): Station
            group (typing.Dict): Gruppe
        """
        self.settings = settings
        self.database = database
        self.station = station
        self.group = group
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["values_template"])

    def write(self, folder=None, filename=None) -> bool:
        """Schreiben der Tabelle

        Args:
            folder (str, optional): Ordner. Defaults to None.
            filename (str, optional): Dateiname. Defaults to None.

        Returns:
            bool: True, wenn erfolgreich
        """
        generated_filename = self.settings["values_output"] % {
            "station": self.station[STATION_SHORT], "riege": self.group[GROUP_NAME]}
        filename = filename or generated_filename

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "values")
            self.__create_worksheet()

            # Löschen aller anderen Arbeitsblätter
            for station in self.database.get_stations():
                if station[STATION_SHORT] in self.workbook.sheetnames:
                    self.remove_worksheet(station[STATION_SHORT])

            return Table.write(self, folder, filename)
        except:
            logging.exception("Wertetabelle %s konnte nicht erstellt werden.", filename)
            return False

    def __create_worksheet(self):
        """Erstellen des Arbeitsblattes
        """
        self.set_worksheet(self.station[STATION_SHORT])
        self.worksheet.title = "%s-%s" % (self.station[STATION_SHORT], str(self.group[GROUP_NAME]))

        data = self.database.get_group_overview(self.group)
        self.table_reader.write(data)

        self.set_value(self.settings["values_cell_groupname"], str(self.group[GROUP_NAME]))
        self.set_footer(settings=self.settings, center="Wertetabelle")
