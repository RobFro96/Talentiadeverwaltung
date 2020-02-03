from util.column_range import ColumnRange

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"


class Cell(object):

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    @classmethod
    def from_row_col(cls, row: int, col: int):
        if col > 0 and row > 0:
            return cls(row, col)
        return None

    @classmethod
    def from_string(cls, string: str):
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
        return self.row, self.col

    def __str__(self):
        col_str = ColumnRange.col_to_letter(self.col)

        return col_str + str(self.row)
