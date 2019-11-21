import tkinter

from database.database import Database
from gui.main_form import ExitReason, MainForm
from initialization.settings_table import SettingsTable
from reports.club_report_table import ClubReportTable
from reports.group_report_table import GroupReportTable
from reports.station_report_table import StationReportTable
from reports.values_report_table import ValuesReportTable
from util.error_collector import ErrorCollector, ErrorType

CLUBS_SAVED = "Vereinsübersicht wurde erfolgreich erstellt."
GROUPS_SAVED = "Riegenübersicht wurde erfolgreich erstellt."
STATIONS_SAVED = "Stationszettel wurde erfolgreich erstellt."


class Competition:
    def __init__(self, folder: str, settings: SettingsTable, database: Database):
        self.folder = folder
        self.settings = settings
        self.database = database
        self.main_form: MainForm = None

    def open_gui(self, root: tkinter.Tk) -> ExitReason:
        self.main_form = MainForm(self)
        return self.main_form.open(root)

    def get_name(self):
        return self.settings["competition_name"]

    def on_report_club(self) -> ErrorCollector:
        errors = ErrorCollector()

        table = ClubReportTable(self.folder, self.settings, errors)
        table.open()
        if errors.has_error():
            return errors

        table.create(self.database, errors)
        if errors.has_error():
            return errors

        table.write()
        if not errors.has_error():
            errors.append(ErrorType.NONE, CLUBS_SAVED)

        return errors

    def on_report_group(self) -> ErrorCollector:
        errors = ErrorCollector()

        table = GroupReportTable(self.folder, self.settings, errors)
        table.open()
        if errors.has_error():
            return errors

        table.create(self.database, errors)
        if errors.has_error():
            return errors

        table.write()
        if not errors.has_error():
            errors.append(ErrorType.NONE, GROUPS_SAVED)

        return errors

    def on_report_stations(self) -> ErrorCollector:
        errors = ErrorCollector()

        table = StationReportTable(self.folder, self.settings, errors)
        table.open()
        if errors.has_error():
            return errors

        table.create(self.database, errors)
        if errors.has_error():
            return errors

        table.write()
        if not errors.has_error():
            errors.append(ErrorType.NONE, STATIONS_SAVED)

        return errors

    def on_report_values(self) -> ErrorCollector:
        errors = ErrorCollector()

        for station in self.database.get_stations():
            for group in self.database.get_groups():
                table = ValuesReportTable(self.folder, self.settings, errors)
                table.open()
                table.create(self.database, errors, station, group)
                table.write()
                if errors.has_error():
                    return

        if not errors.has_error():
            errors.append(ErrorType.NONE, STATIONS_SAVED)

        return errors
