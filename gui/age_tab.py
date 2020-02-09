"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import tkinter
import tkinter.ttk

from gui.gui_table import GuiTable

TITLE = "Altersklassen"
HEADERS = ["Altersklasse", "männlich", "weiblich", "gesamt"]
TOTAL = "Gesamt"


class AgeTab:
    """GUI-Tab der Altersübersicht
    """

    def __init__(self, main_form):
        """Konstruktor.

        Args:
            main_form (MainFrom): MainForm
        """
        from gui.main_form import MainForm
        self.main_form: MainForm = main_form
        self.tab = None
        self.table: GuiTable = None

    def create(self):
        """Erstellen des Tabs
        """
        self.tab = tkinter.ttk.Frame(self.main_form.notebook)
        self.main_form.notebook.add(self.tab, text=TITLE)

        self.table = GuiTable(self.tab, HEADERS, [100]*4)
        self.table.grid(row=0, column=0, sticky="nsew")
        self.table.grid_vsb(row=0, column=1, sticky='nse')

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

    def update_table(self, data):
        """Aktualisieren der Tabelle

        Args:
            data: Daten
        """
        self.table.update(data, {TOTAL: ("bold",)})
