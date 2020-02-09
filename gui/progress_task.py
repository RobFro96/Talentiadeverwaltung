"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import tkinter
import tkinter.ttk


class ProgressTask:
    """Klasse zum Erstellen eines Fensters mit Fortschrittsanzeige
    """

    def __init__(self, root):
        """Konstruktor.

        Args:
            root: tkinter-Root
        """
        self.toplevel = tkinter.Toplevel(root)

        from main import ICON_PATH
        self.toplevel.iconbitmap(ICON_PATH)

        x = root.winfo_x()
        y = root.winfo_y()
        self.toplevel.geometry("300x50+%d+%d" % (x+10, y+10))
        self.toplevel.resizable(False, False)
        self.toplevel.grab_set()
        self.toplevel.transient(root)

        self.label = tkinter.Label(self.toplevel, text="Hallo")
        self.label.pack(side="top", fill="both")

        self.progress = tkinter.ttk.Progressbar(self.toplevel)
        self.progress.pack(fill="both")

    def set_title(self, title: str):
        """Setzen des Titels

        Args:
            title (str): Titel
        """
        self.toplevel.title(title)

    def set_label(self, text: str):
        """Setzen des Labels

        Args:
            text (str): Label
        """
        self.label.config(text=text)

    def set_value(self, value: int):
        """Setzen des Zählers des Fortschrittsanteils

        Args:
            value (int): Zähler
        """
        self.progress["value"] = value

    def inc_value(self):
        """Inkrementieren des Zählers des Fortschrittsanteils
        """
        self.progress["value"] += 1

    def set_maximum(self, maximum: int):
        """Setzen des Nenners des Fortschrittsanteils

        Args:
            maximum (int): [description]
        """
        self.progress["maximum"] = maximum

    def close(self):
        """Schließen des Fensters
        """
        self.toplevel.destroy()
