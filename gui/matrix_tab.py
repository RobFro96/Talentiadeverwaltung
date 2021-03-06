"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging
import tkinter
import tkinter.ttk
import typing

from data.database import Database
from data.database_groups import GROUP_NAME
from data.database_stations import STATION_NAME
from gui.gui_table import GuiTable

TITLE = "Dateneingabe"
FIRST_CELL = "Station\u2193  Riege\u2192"


class MatrixTab:
    """GUI-Tab der Übersicht der Dateneingabe
    """

    def __init__(self, main_form, database: Database):
        """Konstruktor.

        Args:
            main_form (MainFrom): MainForm
        """
        from gui.main_form import MainForm
        self.main_form: MainForm = main_form
        self.database = database
        self.tab = None
        self.table: GuiTable = None

    def create(self):
        """Erstellen des Tabs
        """
        self.tab = tkinter.ttk.Frame(self.main_form.notebook)
        self.main_form.notebook.add(self.tab, text=TITLE)

        headers, sizes = self.get_headers_and_sizes()
        self.table = GuiTable(self.tab, headers, sizes)
        self.table.grid(row=0, column=0, sticky="nsew")
        self.table.grid_vsb(row=0, column=1, sticky='nse')

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

        self.dummy_fill()

    def get_headers_and_sizes(self) -> (typing.List[str], typing.List[int]):
        """Methode zum Erstellen der Liste der Überschriften und Spaltenbreiten

        Returns:
            (typing.List[str], typing.List[int]): Überschriften und Spaltenbreiten
        """
        headers = [FIRST_CELL]
        sizes = [150]
        for group in self.database.get_groups():
            headers.append(group[GROUP_NAME])
            sizes.append(40)
        return headers, sizes

    def dummy_fill(self):
        """Füllen der Tabelle mit leeren Werten
        """
        matrix = []
        for _ in self.database.get_stations():
            matrix.append([logging.ERROR] * len(self.database.get_groups()))

        self.update_table(matrix)

    def update_table(self, matrix):
        """Aktualisieren der Tabelle

        Args:
            matrix: Matrix
        """
        data = {}
        for row_id, station in enumerate(self.database.get_stations()):
            station_name = station[STATION_NAME]
            row = []

            for col_id, _ in enumerate(self.database.get_groups()):
                element = matrix[row_id][col_id]

                if element == logging.INFO:
                    row.append("\u2714")
                elif element == logging.WARNING:
                    row.append("?")
                else:
                    row.append(" ")

            data[station_name] = row

        self.table.update(data)
