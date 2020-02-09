"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import enum
import logging
import threading
import tkinter
import tkinter.ttk

from gui.age_tab import AgeTab
from gui.group_tab import GroupTab
from gui.login_tab import LoginTab
from gui.matrix_tab import MatrixTab
from gui.menu import Menu
from gui.progress_task import ProgressTask


class ExitReason(enum.Enum):
    """Enum.
    Gibt an, aus welchen Grund das MainForm beendet wurde.
    """
    EXIT = 0
    OPEN = 1
    REFRESH = 2


TITLE = "Talentiadeverwaltung [%s]"
STATION_REPORT_PROGRESS_LABEL = "Stationsübersicht wird erstellt."
VALUE_TABLES_PROGRESS_LABEL = "Wertetabellen werden erstellt."
REFRESH_SCORING_PROGRESS_LABEL = "Wertetabellen werden eingelesen."
SCORING_PROGRESS_LABEL = "Auswertung wird erstellt."


class MainForm:
    """Haupt-Fenster der Anwendung
    """

    def __init__(self, competition):
        """Konstruktor.

        Args:
            competition (Competition): Zurgehörige Veranstaltung
        """
        from initialization.competition import Competition
        self.competition: Competition = competition
        self.root: tkinter.Tk = None
        self.notebook: tkinter.ttk.Notebook = None
        self.exit_reason = ExitReason.EXIT
        self.menu: Menu = None
        self.login_tab: LoginTab = None
        self.age_tab: AgeTab = None
        self.group_tab: GroupTab = None
        self.matrix_tab: MatrixTab = None

    def open(self, root: tkinter.Tk) -> ExitReason:
        """Öffnen der Anwendung
        Programmzeiger bleibt in dieser Funktion, bis Fenster beendet wird.
        Der Grund des Beendens wird zurückgegeben

        Args:
            root (tkinter.Tk): Tkinter-Root

        Returns:
            ExitReason: Grund des Beendens
        """
        self.root = root
        self.root.update()
        self.root.deiconify()

        self.set_title()
        self.root.minsize(500, 300)

        self.menu = Menu(self)
        self.menu.create()

        self.notebook = tkinter.ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.login_tab = LoginTab(self)
        self.login_tab.create()

        self.age_tab = AgeTab(self)
        self.age_tab.create()

        self.group_tab = GroupTab(self)
        self.group_tab.create()

        self.matrix_tab = MatrixTab(self, self.competition.database)
        self.matrix_tab.create()

        self.__set_from_data()

        self.root.mainloop()

        return self.exit_reason

    def set_title(self):
        """Setzen der Titelzeile der Anwendung
        """
        self.root.title(TITLE % self.competition.get_name())

    def on_open(self, *_):
        """Wenn eine neue Veranstaltung geöffnet werden soll.
        """
        logging.info("Veranstaltung öffnen")
        self.exit_reason = ExitReason.OPEN
        self.root.destroy()

    def on_refresh(self, *_):
        """Wenn die Veranstaltung aktualisiert werden soll.
        """
        logging.info("Veranstaltung aktualisieren")
        self.exit_reason = ExitReason.REFRESH
        self.root.destroy()

    def on_quit(self, *_):
        """Wenn das Programm beendet werden soll.
        """
        logging.info("Programm beenden")
        self.exit_reason = ExitReason.EXIT
        self.root.destroy()

    def on_report_club(self, *_):
        """Wenn die Vereinsübersicht erstellt werden soll.
        """
        logging.info("Vereinsübersicht erstellen")
        self.competition.on_report_club().show_messagebox()

    def on_report_group(self, *_):
        """Wenn die Riegenübersicht erstellt werden soll.
        """
        logging.info("Riegenübersicht erstellen")
        self.competition.on_report_group().show_messagebox()

    def on_report_stations(self, *_):
        """Wenn die Stations-Listen erstellt werden sollen
        """
        logging.info("Stationsübersicht erstellen")
        progress = ProgressTask(self.root)
        progress.set_label(STATION_REPORT_PROGRESS_LABEL)
        progress.set_maximum(self.competition.database.get_process_steps(0, 1))

        def process():
            errors = self.competition.on_report_stations(progress)
            progress.close()
            errors.show_messagebox()

        threading.Thread(target=process).start()

    def on_create_value_tables(self, *_):
        """Wenn die Wertungstabellen erstellt werden sollen.
        """
        logging.info("Wertetabellen erstellen")
        progress = ProgressTask(self.root)
        progress.set_label(VALUE_TABLES_PROGRESS_LABEL)
        progress.set_maximum(self.competition.database.get_process_steps())

        def process():
            errors = self.competition.on_report_values(progress)
            progress.close()
            errors.show_messagebox()

        threading.Thread(target=process).start()

    def on_scoring_refresh(self, *_):
        """Wenn die Wertungslisten eingelesen werden sollen.
        """
        logging.info("Auswertung aktualisieren")
        progress = ProgressTask(self.root)
        progress.set_label(REFRESH_SCORING_PROGRESS_LABEL)
        progress.set_maximum(self.competition.database.get_process_steps())

        def process():
            errors, matrix = self.competition.on_scoring_refresh(progress)
            progress.close()
            errors.show_messagebox()
            self.matrix_tab.update_table(matrix)

        threading.Thread(target=process).start()

    def on_scoring_create(self, *_):
        """Wenn die Auswertung erstellt werden soll.
        """
        logging.info("Auswertung erstellen")
        progress = ProgressTask(self.root)
        progress.set_label(SCORING_PROGRESS_LABEL)
        progress.set_maximum(len(self.competition.database.get_sclasses()))

        def process():
            errors = self.competition.on_scoring_create(progress)
            progress.close()
            errors.show_messagebox()

        threading.Thread(target=process).start()

    def __set_from_data(self):
        """Aktualsieren der Daten von LoginTab, AgeTab, GroupTab
        """
        self.login_tab.update_table(self.competition.database.pack_club_table())
        self.age_tab.update_table(self.competition.database.pack_age_table())
        self.group_tab.update_table(self.competition.database.pack_group_table())
