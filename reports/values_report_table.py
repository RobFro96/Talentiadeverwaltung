import logging

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_SHORT
from util.table_reader import TableReader
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from util.table import Table


class ValuesReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, database: Database,
                 station, group):
        self.settings = settings
        self.database = database
        self.station = station
        self.group = group
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder, self.settings["values_template"])

    def write(self, folder=None, filename=None) -> bool:
        generated_filename = self.settings["values_output"] % {
            "station": self.station[STATION_SHORT], "riege": self.group[GROUP_NAME]}
        filename = filename or generated_filename

        try:
            self.table_reader = TableReader.from_settings(self, self.settings, "values")
            self.__create_worksheet()

            for station in self.database.get_stations():
                if station[STATION_SHORT] in self.workbook.sheetnames:
                    self.remove_worksheet(station[STATION_SHORT])

            return Table.write(self, folder, filename)
        except:
            logging.exception("Wertetabelle %s konnte nicht erstellt werden.", filename)
            return False

    def __create_worksheet(self):
        self.set_worksheet(self.station[STATION_SHORT])
        self.worksheet.title = "%s-%s" % (self.station[STATION_SHORT], str(self.group[GROUP_NAME]))

        data = self.database.get_group_overview(self.group)
        self.table_reader.write(data)

        self.set_value(self.settings["values_cell_groupname"], str(self.group[GROUP_NAME]))
