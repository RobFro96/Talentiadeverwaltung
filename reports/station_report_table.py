from database.database import GROUP_NAME, STATION_SHORT, Database
from database.table_reader import TableReader
from initialization.settings_table import SettingsTable
from util.error_collector import ErrorCollector, ErrorType
from util.table import Table

ERROR_OPENING = "Vorlage der Stationszettel %s kann nicht geöffnet werden."
ERROR_SAVING = "Stationszettel %s konnte nicht gespeichert werden."


class StationReportTable(Table):
    def __init__(self, competition_folder: str, settings: SettingsTable, errors: ErrorCollector):
        self.settings = settings
        self.errors = errors
        self.table_reader: TableReader = None
        Table.__init__(self, competition_folder,
                       self.settings["stations_template"])

    def open(self):
        if not Table.open(self):
            self.errors.append(ErrorType.ERROR, ERROR_OPENING % self.filename)
            return

    def write(self):
        if not Table.write(self, None, self.settings["stations_output"]):
            self.errors.append(ErrorType.ERROR, ERROR_SAVING % self.filename)
            return

    def create(self, database: Database, errors: ErrorCollector):
        self.table_reader = TableReader(self, errors).from_settings(
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
