import logging
import tkinter

from database.database import Database
from gui.main_form import ExitReason, MainForm
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
        ec = ErrorCollector()

        table = ClubReportTable(self.folder, self.settings)
        table.open()
        if ec.has_error():
            return ec

        table.create(self.database)
        if ec.has_error():
            return ec

        table.write()
        if ec.has_error():
            return ec

        logging.info("Vereinsübersicht wurde erfolgreich erstellt.")
        return ec

    def on_report_group(self) -> ErrorCollector:
        ec = ErrorCollector()

        table = GroupReportTable(self.folder, self.settings)
        table.open()
        if ec.has_error():
            return ec

        table.create(self.database)
        if ec.has_error():
            return ec

        table.write()
        if ec.has_error():
            return ec

        logging.info("Riegenübersicht wurde erfolgreich erstellt.")
        return ec

    def on_report_stations(self) -> ErrorCollector:
        ec = ErrorCollector()

        table = StationReportTable(self.folder, self.settings)
        table.open()
        if ec.has_error():
            return ec

        table.create(self.database)
        if ec.has_error():
            return ec

        table.write()
        if ec.has_error():
            return ec

        logging.info("Stationszettel wurde erfolgreich erstellt.")
        return ec

    def on_report_values(self) -> ErrorCollector:
        ec = ErrorCollector()

        for station in self.database.get_stations():
            for group in self.database.get_groups():
                table = ValuesReportTable(self.folder, self.settings)
                table.open()
                table.create(self.database, station, group)
                table.write()
                if ec.has_error():
                    return

        if ec.has_error():
            return ec

        logging.info("Wertungszettel wurden erfolgreich erstellt.")
        return ec
