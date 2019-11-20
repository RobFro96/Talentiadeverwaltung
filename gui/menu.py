import tkinter

FILE_MENU = "Veranstaltung"
FILE_OPEN = "Öffnen"
FILE_REFRESH = "Aktualisieren"
FILE_QUIT = "Beenden"
REPORT_MENU = "Reports"
REPORT_CLUB_TABLE = "Vereinsübersicht erstellen"
REPORT_GROUP = "Riegenübersicht erstellen"
REPORT_STATIONS = "Stationszettel erstellen"
REPORT_VALUES = "Wertetabellen erstellen"
SCORING_MENU = "Auswertung"
SCORING_REFRESH = "Stationsübersicht aktualisieren"
SCORING_CREATE = "Auswertung erstellen"


class Menu:
    def __init__(self, main_form):
        from gui.main_form import MainForm
        self.main_form: MainForm = main_form
        self.menu = None
        self.file_menu = None
        self.report_menu = None
        self.scoring_menu = None

    def create(self):
        self.menu = tkinter.Menu(self.main_form.root)
        self.main_form.root.config(menu=self.menu)

        self.file_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(
            label=FILE_MENU, underline=0, menu=self.file_menu)
        self.file_menu.add_command(
            label=FILE_OPEN, command=self.main_form.on_open, accelerator="Strg+O")
        self.file_menu.add_command(
            label=FILE_REFRESH, command=self.main_form.on_refresh, accelerator="Strg+R")
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label=FILE_QUIT, command=self.main_form.on_quit)

        self.report_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(
            label=REPORT_MENU, underline=0, menu=self.report_menu)
        self.report_menu.add_command(
            label=REPORT_CLUB_TABLE, command=self.main_form.on_report_club)
        self.report_menu.add_command(
            label=REPORT_GROUP, command=self.main_form.on_report_group)
        self.report_menu.add_command(
            label=REPORT_STATIONS, command=self.main_form.on_report_stations)
        self.report_menu.add_command(
            label=REPORT_VALUES, command=self.main_form.on_create_value_tables)

        self.scoring_menu = tkinter.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(
            label=SCORING_MENU, underline=0, menu=self.scoring_menu)
        self.scoring_menu.add_command(
            label=SCORING_REFRESH, command=self.main_form.on_scoring_refresh, accelerator="F5")
        self.scoring_menu.add_command(
            label=SCORING_CREATE, command=self.main_form.on_scoring_create)

        self.main_form.root.bind_all("<Control-o>", self.main_form.on_open)
        self.main_form.root.bind_all("<Control-r>", self.main_form.on_refresh)
        self.main_form.root.bind_all("<F5>", self.main_form.on_scoring_refresh)
