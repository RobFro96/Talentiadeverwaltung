"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ColumnRange:
    """Klasse zur Beschreibung einer Folge von Spalten einer Tabelle
    """

    @classmethod
    def letter_to_col(cls, letter):
        """Umwandeln mehrerer Zeichen in die Spaltennummer.
        A = 1, AA = 27, ...

        Args:
            letter (str): einer oder mehrere Buchstaben

        Returns:
            int: Spaltennummer
        """
        col = 0
        for c in letter:
            if c not in ALPHABET:
                return None
            col = col * 26 + ALPHABET.index(c) + 1
        return col

    @classmethod
    def col_to_letter(cls, col):
        """Umwandln der Spaltennummer in eine Zeichenkette
        Umkehrfunktion zu letter_to_col()

        Args:
            col (int): Spaltennummer

        Returns:
            str: Zeichenkette
        """
        col_str = ""

        while col > 0:
            col -= 1
            col_str += ALPHABET[col % 26]
            col //= 26
        return col_str

    @classmethod
    def from_string(cls, string: str):
        """Umwandeln einer Zeichenkette in eine ColumnRange

        Args:
            string (str): Zeichkette

        Returns:
            ColumnRange: Spaltenfolge
        """
        splitted = string.split("-")
        if len(splitted) != 2:
            return None
        start = cls.letter_to_col(splitted[0])
        end = cls.letter_to_col(splitted[1])

        if (not start) or (not end):
            return None

        return cls(start, end)

    def __init__(self, start: int, end: int):
        """Konstruktor.

        Args:
            start (int): Start-Spaltennummer
            end (int): End-Spaltennummer
        """
        self.start = start
        self.end = end

    def __repr__(self):
        """Umwandlung in eine Zeichenkette

        Returns:
            str: Zeichenkette der Form A-Z
        """
        return "%s-%s" % (self.col_to_letter(self.start), self.col_to_letter(self.end))

    def range(self):
        """Gibt die Spaltennummern aller Spalten innerhalb der Folge zurück.

        Returns:
            range: Range-Folge
        """
        return range(self.start, self.end + 1)

    def id(self, i):
        """Umwandeln der id in die entsprechende Spaltennummer

        Args:
            i (int): id

        Returns:
            int: Spaltennummer
        """
        return self.start + i
