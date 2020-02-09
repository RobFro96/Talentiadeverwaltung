"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import tkinter.ttk
import typing


class GuiTable:
    """Klasse zur Verwendung des Tkinter-Treeviews als Datentabelle
    """

    def __init__(self, parent: tkinter.ttk.Notebook, headers: typing.List[str],
                 widths: typing.List[int]):
        """Konstruktor.

        Args:
            parent (tkinter.ttk.Notebook): GUI-Element auf dem Tabelle platziert wird
            headers (typing.List[str]): Überschriften
            widths (typing.List[int]): Spaltenbreite
        """
        self.treeview = tkinter.ttk.Treeview(parent)
        self.update_headers(headers, widths)

        self.vsb = tkinter.ttk.Scrollbar(parent, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.vsb.set)

        self.treeview.tag_configure("bold", font=(None, 9, "bold"))

    def update_headers(self, headers: typing.List[str], widths: typing.List[int]):
        """Aktualisieren der Überschriften und Spaltenbreiten

        Args:
            headers (typing.List[str]): Überschriften
            widths (typing.List[int]): Spaltenbreite
        """
        self.treeview.grid_remove()
        self.treeview.delete(*self.treeview.get_children())
        self.treeview["columns"] = [("col" + str(i))
                                    for i in range(len(headers) - 1)]
        self.treeview.heading("#0", text=headers[0], anchor="w")
        self.treeview.column("#0", anchor="w", width=widths[0], stretch=False)

        i = 0
        for header in headers[1:]:
            self.treeview.heading("col" + str(i), text=header)
            self.treeview.column(
                "col" + str(i), anchor='center', width=widths[i+1], stretch=False)
            i += 1

    def grid(self, *args, **kwargs):
        """Grid-Funktion zum Platzieren des Treeviews
        """
        self.treeview.grid(*args, **kwargs)

    def grid_vsb(self, *args, **kwargs):
        """Grid-Funktion zum Platzieren der Scrollbar
        """
        self.vsb.grid(*args, **kwargs)

    def update(self, data: typing.List[typing.Dict], tags=None):
        """Aktualisieren der Daten der Tabelle
        Daten werden als Dict übergeben. Der Schlüssel entspricht dem ersten Element.

        Args:
            data (typing.List[typing.Dict]): Daten
            tags (optional): Daten mit einem Tag. Defaults to None.
        """
        tags = tags or {}
        self.treeview.delete(*self.treeview.get_children())
        for name, values in data.items():
            tag = tags[name] if name in tags else ()
            self.treeview.insert("", "end", text=name, values=values, tags=tag)
