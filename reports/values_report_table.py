import logging

from database.database import GROUP_NAME, STATION_SHORT, Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.table import Table


class ValuesReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable):
        self.settings = settings
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder,
                       self.settings["values_template"])

    def open(self):
        if not Table.open(self):
            logging.error("Vorlage der Wertetabellen %s kann nicht geöffnet werden.",
                          self.filename)
            return

    def write(self):
        if not Table.write(self, None, None):
            logging.error("Wertetabelle %s konnte nicht gespeichert werden.",
                          self.filename)
            return

    def create(self, database: Database, station, group):
        self.filename = self.settings["values_output"] % (
            station[STATION_SHORT], group[GROUP_NAME])

        self.table_reader = TableReader(self).from_settings(
            self.settings, "values", False, False)

        self.__create_worksheet(station, group, database)

        for stations in database.get_stations():
            station_name = stations[STATION_SHORT]
            if station_name in self.workbook:
                self.workbook.remove_sheet(self.workbook[station_name])

    def __create_worksheet(self, station, group, database: Database):
        self.worksheet = self.__get_template_sheet(station)
        self.worksheet.title = "%s-%s" % (
            station[STATION_SHORT], str(group[GROUP_NAME]))
        self.table_reader.set_worksheet(self.worksheet)

        data = database.get_group_overview(group)
        self.table_reader.write(data)

        self.worksheet[self.settings["values_cell_groupname"]
                       ].value = str(group[GROUP_NAME])

    def __get_template_sheet(self, station):
        return self.workbook[station[STATION_SHORT]]
