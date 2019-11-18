import tkinter
import tkinter.ttk

from gui.gui_table import GuiTable

TITLE = "Altersklassen"
HEADERS = ["Altersklasse", "männlich", "weiblich", "gesamt"]
TOTAL = "Gesamt"


class AgeTab:
    def __init__(self, main_form):
        from gui.main_form import MainForm
        self.main_form: MainForm = main_form
        self.tab = None
        self.age_table: GuiTable = None

    def create(self):
        self.tab = tkinter.ttk.Frame(self.main_form.notebook)
        self.main_form.notebook.add(self.tab, text=TITLE)

        self.age_table = GuiTable(self.tab, HEADERS, [100]*4)
        self.age_table.grid(row=0, column=0, sticky="nsew")
        self.age_table.grid_vsb(row=0, column=1, sticky='nse')

        self.tab.grid_rowconfigure(0, weight=1)
        self.tab.grid_columnconfigure(0, weight=1)

    def update_table(self, data):
        self.age_table.update(data, {TOTAL: ("bold",)})
