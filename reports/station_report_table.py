import logging

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_SHORT
from util.table_reader import TableReader
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from util.table import Table


class StationReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 progress: ProgressTask = None):
        self.settings = settings
        self.database = database
        self.progress = progress
        self.table_reader: TableReader = None

        Table.__init__(self, competition_folder,
                       self.settings["stations_template"])

    def write(self, folder=None, filename=None) -> bool:
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
        self.copy_worksheet(station[STATION_SHORT])
        self.worksheet.title = "%s-%s" % (station[STATION_SHORT], str(group[GROUP_NAME]))

        data = self.database.get_group_overview(group)
        self.table_reader.write(data)

        self.set_value(self.settings["stations_cell_groupname"], str(group[GROUP_NAME]))
