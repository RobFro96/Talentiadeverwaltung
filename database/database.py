import typing

from database.table_reader import TableReader
from util.error_collector import ErrorCollector

CLUB = "Verein"
LOGOUT = "Abmeldung"
TOTAL = "Gesamt"


class Database:
    def __init__(self):
        self.database: typing.List[typing.Dict[str, typing.Any]] = []
        self.clubs: typing.List[str] = []
        self.errors: ErrorCollector = None

    def read_attendees_table(self, table_reader: TableReader, errors: ErrorCollector):
        self.database = []
        self.clubs = []
        self.errors = errors
        table_reader.read(self.__read_attendees_table_cb)

    def __read_attendees_table_cb(self, row: int, row_data: typing.Dict[str, typing.Any]):
        self.database.append(row_data)
        if CLUB in row_data:
            if row_data[CLUB] not in self.clubs:
                self.clubs.append(row_data[CLUB])

    def pack_club_table(self):
        data = {}
        total = [0, 0, 0]

        for club in self.clubs:
            row = [0, 0, 0]

            row[0] = len(list(filter(lambda e, club=club:
                                e[CLUB] == club,
                                self.database)))
            row[1] = len(list(filter(lambda e, club=club:
                                e[CLUB] == club and e[LOGOUT] is not None,
                                self.database)))
            row[2] = row[0] - row[1]

            data[club] = row

            for i in range(3):
                total[i] += row[i]
        
        data[TOTAL] = total
        
        return data
