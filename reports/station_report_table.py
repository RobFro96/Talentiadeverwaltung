import logging

from database.database import GROUP_NAME, STATION_SHORT, Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table


class StationReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable):
        self.settings = settings
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder,
                       self.settings["stations_template"])

    def open(self):
        if not Table.open(self):
            logging.error("Vorlage der Stationszettel %s kann nicht geöffnet werden.",
                          self.filename)
            return

    def write(self):
        if not Table.write(self, None, self.settings["stations_output"]):
            logging.error("Stationszettel %s konnte nicht gespeichert werden.",
                          self.filename)
            return

    def create(self, database: Database):
        self.table_reader = TableReader(self).from_settings(
            self.settings, "stations", False, False)

        for station in database.get_stations():
            for group in database.get_groups():
                self.__create_worksheet(station, group, database)

        for station in database.get_stations():
            self.workbook.remove_sheet(self.__get_template_sheet(station))

    def __create_worksheet(self, station, group, database: Database):
        self.worksheet = self.workbook.copy_worksheet(
            self.__get_template_sheet(station))
        self.worksheet.title = "%s-%s" % (
            station[STATION_SHORT], str(group[GROUP_NAME]))
        self.table_reader.set_worksheet(self.worksheet)

        data = database.get_group_overview(group)
        self.table_reader.write(data)

        self.worksheet[self.settings["stations_cell_groupname"]
                       ].value = str(group[GROUP_NAME])

    def __get_template_sheet(self, station):
        return self.workbook[station[STATION_SHORT]]
