"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging
import tkinter
import typing

from data.database import Database
from gui.main_form import ExitReason, MainForm
from gui.progress_task import ProgressTask
from initialization.settings_table import SettingsTable
from reports.club_report_table import ClubReportTable
from reports.group_report_table import GroupReportTable
from reports.station_report_table import StationReportTable
from reports.values_report_table import ValuesReportTable
from scoring.scoring_table import ScoringTable
from scoring.values_input_table import ValuesInputTable
from util.error_collector import ErrorCollector


class Competition:
    """Veranstaltung: Hauptklasse der Anwendung.
    Alle Daten, Einstellungen und Aktionen werden in dieser Klasse miteinander verknüpft.
    """

    def __init__(self, folder: str, settings: SettingsTable, database: Database):
        """Konstruktor.

        Args:
            folder (str): Ordner der Veranstaltung
            settings (SettingsTable): Einstellungen
            database (Database): Datenbank
        """
        self.folder = folder
        self.settings = settings
        self.database = database
        self.main_form: MainForm = None

    def open_gui(self, root: tkinter.Tk) -> ExitReason:
        """Öffnen des Fensters der GUI

        Args:
            root (tkinter.Tk): tkinter-Root

        Returns:
            ExitReason: Grund warum Fenster geschlossen wurde.
        """
        self.main_form = MainForm(self)
        return self.main_form.open(root)

    def get_name(self) -> str:
        """Name der Veranstaltung

        Returns:
            str: Name
        """
        return self.settings["competition_name"]

    def on_report_club(self) -> ErrorCollector:
        """Erstellen der Vereinsübersicht

        Returns:
            ErrorCollector: Fehler
        """
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
        """Erstellen der Riegenübersicht

        Returns:
            ErrorCollector: Fehler
        """
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
        """Erstellen der Stationszettel

        Args:
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.

        Returns:
            ErrorCollector: Fehler
        """
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
        """Erstellen der Wertungstabellen

        Args:
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.

        Returns:
            ErrorCollector: Fehler
        """
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

    def on_scoring_refresh(self, progress: ProgressTask = None) -> (ErrorCollector, typing.List):
        """Einlesen der Wertungstabellen

         Args:
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.

        Returns:
            ErrorCollector: Fehler
            typing.List: Matrix
        """
        errors = ErrorCollector()
        matrix = []

        self.database.remove_all_scoring_values()

        for station in self.database.get_stations():
            matrix_line = []
            for group in self.database.get_groups():
                table = ValuesInputTable(self.folder, self.settings, self.database, station, group)
                if table.file_exists():
                    table.open()
                else:
                    table.status = logging.ERROR

                if progress:
                    progress.inc_value()

                matrix_line.append(table.status)
            matrix.append(matrix_line)

        if errors.has_error():
            return errors, matrix

        logging.info("Wertungszettel wurden erfolgreich eingelesen.")
        return errors, matrix

    def on_scoring_create(self, progress: ProgressTask = None) -> ErrorCollector:
        """Auswertung erstellen.

        Args:
            progress (ProgressTask, optional): Fortschrittsanzeige. Defaults to None.

        Returns:
            ErrorCollector: Fehler
        """
        errors = ErrorCollector()

        table = ScoringTable(self.folder, self.settings, self.database, progress)
        table.open()
        if errors.has_error():
            return errors

        table.write()
        if errors.has_error():
            return errors

        logging.info("Auswertung wurde erfolgreich erstellt.")
        return errors
