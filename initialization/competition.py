import logging
import tkinter

from data.database import Database
from gui.main_form import ExitReason, MainForm
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from reports.club_report_table import ClubReportTable
from reports.group_report_table import GroupReportTable
from reports.station_report_table import StationReportTable
from reports.values_report_table import ValuesReportTable
from util.error_collector import ErrorCollector


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

        table = ClubReportTable(self.folder, self.settings, self.database)
        table.open()
        if errors.has_error():
            return errors

        table.write()
        if errors.has_error():
            return errors

        logging.info("Vereinsübersicht wurde erfolgreich erstellt.")
        return errors

    def on_report_group(self) -> ErrorCollector:
        errors = ErrorCollector()

        table = GroupReportTable(self.folder, self.settings, self.database)
        table.open()
        if errors.has_error():
            return errors

        table.write()
        if errors.has_error():
            return errors

        logging.info("Riegenübersicht wurde erfolgreich erstellt.")
        return errors

    def on_report_stations(self, progress: ProgressTask = None) -> ErrorCollector:
        errors = ErrorCollector()

        table = StationReportTable(self.folder, self.settings, self.database, progress)
        table.open()
        if errors.has_error():
            return errors

        table.write()
        if errors.has_error():
            return errors

        logging.info("Stationszettel wurde erfolgreich erstellt.")
        return errors

    def on_report_values(self, progress: ProgressTask = None) -> ErrorCollector:
        errors = ErrorCollector()

        for station in self.database.get_stations():
            for group in self.database.get_groups():
                table = ValuesReportTable(self.folder, self.settings, self.database, station, group)
                table.open()
                if errors.has_error():
                    return errors

                table.write()
                if errors.has_error():
                    return errors

                if progress:
                    progress.inc_value()

        if errors.has_error():
            return errors

        logging.info("Wertungszettel wurden erfolgreich erstellt.")
        return errors
