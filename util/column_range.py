
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ColumnRange:
    @classmethod
    def letter_to_col(cls, letter):
        col = 0
        for c in letter:
            if c not in ALPHABET:
                return None
            col = col * 26 + ALPHABET.index(c) + 1
        return col

    @classmethod
    def col_to_letter(cls, col):
        col_str = ""

        while col > 0:
            col -= 1
            col_str += ALPHABET[col % 26]
            col //= 26
        return col_str

    @classmethod
    def from_string(cls, string: str):
        splitted = string.split("-")
        if len(splitted) != 2:
            return None
        start = cls.letter_to_col(splitted[0])
        end = cls.letter_to_col(splitted[1])

        if (not start) or (not end):
            return None

        return cls(start, end)

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __repr__(self):
        return "%s-%s" % (self.col_to_letter(self.start), self.col_to_letter(self.end))

    def range(self):
        return range(self.start, self.end + 1)

    def id(self, i):
        return self.start + i
