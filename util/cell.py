"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
from util.column_range import ColumnRange

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"


class Cell:
    """Klasse der Positionsbeschreibung einer Zelle
    """

    def __init__(self, row: int, col: int):
        """Konstruktor

        Args:
            row (int): Zeilennummer (beginnend bei 1)
            col (int): Spaltennummer (beginnend bei 1)
        """
        self.row = row
        self.col = col

    @classmethod
    def from_row_col(cls, row: int, col: int):
        """Zell aus Zeile und Spalte erstellen.
        Es wird überprüft, dass Zeile und Spalte > 0 sind.

        Args:
            row (int): Zeile
            col (int): Spalte

        Returns:
            Cell: Zelle
        """
        if col > 0 and row > 0:
            return cls(row, col)
        return None

    @classmethod
    def from_string(cls, string: str):
        """Zelle aus einer Zeichenkette erstellen

        Args:
            string (str): Zeichenkette

        Returns:
            Cell: Zelle
        """
        col = 0
        row = 0

        state = 0
        for c in string:
            if c in ALPHABET:
                if state == 0:
                    col = col * 26 + ALPHABET.index(c) + 1
                else:
                    return None
            elif c in NUMBERS:
                state = 1
                row = 10 * row + NUMBERS.index(c)
            else:
                return None

        if col > 0 and row > 0:
            return cls(row, col)
        return None

    def get(self):
        """Gibt Zeile und Spalte zurück.
        *cell.get() kann verwendet werden, um auf eine openpyxl-Zelle zuzugreifen.

        Returns:
            (int, int): Zeile, Spalte
        """
        return self.row, self.col

    def __str__(self):
        """Umwandeln in eine Zeichenkette

        Returns:
            str: Zeichenkette
        """
        col_str = ColumnRange.col_to_letter(self.col)

        return col_str + str(self.row)
