import enum
import tkinter
import tkinter.ttk

from gui.age_tab import AgeTab
from gui.group_tab import GroupTab
from gui.login_tab import LoginTab
from gui.menu import Menu
from gui.progress_task import ProgressTask
from util.error_collector import print_info


class ExitReason(enum.Enum):
    EXIT = 0
    OPEN = 1
    REFRESH = 2


TITLE = "Talentiadeverwaltung [%s]"


class MainForm:
    def __init__(self, competition):
        from initialization.competition import Competition
        self.competition: Competition = competition
        self.root: tkinter.Tk = None
        self.notebook: tkinter.ttk.Notebook = None
        self.exit_reason = ExitReason.EXIT
        self.menu: Menu = None
        self.login_tab: LoginTab = None
        self.age_tab: AgeTab = None
        self.group_tab: GroupTab = None

    def open(self, root: tkinter.Tk) -> ExitReason:
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

        self.__set_from_data()

        self.root.mainloop()

        return self.exit_reason

    def set_title(self):
        self.root.title(TITLE % self.competition.get_name())

    def on_open(self, *_):
        print_info("Veranstaltung öffnen")
        self.exit_reason = ExitReason.OPEN
        self.root.destroy()

    def on_refresh(self, *_):
        print_info("Veranstaltung aktualisieren")
        self.exit_reason = ExitReason.REFRESH
        self.root.destroy()

    def on_quit(self, *_):
        print_info("Programm beenden")
        self.exit_reason = ExitReason.EXIT
        self.root.destroy()

    def on_report_club(self, *_):
        print_info("Vereinsübersicht erstellen")
        self.competition.on_report_club().show_messagebox()

    def on_report_group(self, *_):
        print_info("Riegenübersicht erstellen")
        self.competition.on_report_group().show_messagebox()

    def on_report_stations(self, *_):
        print_info("Stationsübersicht erstellen")
        self.competition.on_report_stations().show_messagebox()

    def on_create_value_tables(self, *_):
        print_info("Wertetabellen erstellen")
        ProgressTask(self.root).start()

        # self.competition.on_report_values().show_messagebox()

    def on_scoring_refresh(self, *_):
        print_info("Auswertung aktualisieren")

    def on_scoring_create(self, *_):
        print_info("Auswertung erstellen")

    def __set_from_data(self):
        self.login_tab.update_table(
            self.competition.database.pack_club_table())
        self.age_tab.update_table(
            self.competition.database.pack_age_table())
        self.group_tab.update_table(
            self.competition.database.pack_group_table())
