import re
import typing

from database.table_reader import TableReader
from util.error_collector import ErrorCollector, ErrorType

ID = "ID"
CLUB = "Verein"
AGE = "Jahrgang"
LOGOUT = "Abmeldung"
GROUP = "Riege"
GENDER = "Geschlecht"
MALE = "m"
FEMALE = "w"

TOTAL = "Gesamt"
SORT_CLUBS = True

GROUP_NAME = "Riegenname"
GROUP_AGE_CLASSES = "Altersklassen"
GROUP_LIMIT = "Maximalgröße"
GROUP_SIZE = "Größe"

AGE_CLASS_CREATE_ERROR = "Fehler beim Erstellen der Alterklasse des Sportlers mit der ID %d. Fehler: %s"
NO_MATCH_WARN = "Den folgenden Sportlern konnte keine Riege zugeordnet werden: %s"


class Database:
    def __init__(self, settings):
        from initialization.settings_table import SettingsTable
        self.settings: SettingsTable = settings

        self.database: typing.List[typing.Dict[str, typing.Any]] = []
        self.clubs: typing.List[str] = []
        self.ages: typing.List[int] = []
        self.groups: typing.List[typing.Dict[str, typing.Any]] = []
        self.errors: ErrorCollector = None

        self.age_classifier: str = self.settings["age_classifier"]

    def read_attendees_table(self, table_reader: TableReader, errors: ErrorCollector):
        self.database = []
        self.clubs = []
        self.ages = []
        self.errors = errors
        table_reader.read(self.__read_attendees_table_cb)

    def __read_attendees_table_cb(self, row: int, row_data: typing.Dict[str, typing.Any]):
        self.database.append(row_data)
        if CLUB in row_data:
            if row_data[CLUB] not in self.clubs:
                self.clubs.append(row_data[CLUB])
                if SORT_CLUBS:
                    self.clubs.sort()
        if AGE in row_data:
            if row_data[AGE] not in self.ages:
                self.ages.append(row_data[AGE])
                self.ages.sort()

    def get_clubs(self):
        return self.clubs

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

    def get_club_overview(self, club: str):
        return list(filter(lambda e, club=club:
                           e[CLUB] == club,
                           self.database))

    def read_group_table(self, table_reader: TableReader, errors: ErrorCollector):
        self.groups = []
        self.errors = errors
        table_reader.read(self.__read_group_table_cb)

    def __read_group_table_cb(self, row: int, row_data: typing.Dict[str, typing.Any]):
        self.groups.append(row_data)

    def get_age_class(self, attendee: typing.Dict[str, typing.Any]):
        spalte = attendee

        try:
            age_class = eval(self.age_classifier)
        except Exception as e:
            self.errors.append(
                ErrorType.ERROR, AGE_CLASS_CREATE_ERROR % (attendee["ID"], str(e)))

        return age_class

    def do_grouping(self, errors: ErrorCollector):
        self.errors = errors
        self.sort_attendees(self.settings["group_sort_before"])
        self.__grouping_clear()

        no_matchs = []

        for attendee in self.get_attending():
            if not self.__get_group(attendee):
                no_matchs.append(str(attendee["ID"]))

        self.sort_attendees(self.settings["group_sort_after"])

        if no_matchs:
            self.errors.append(ErrorType.WARNING, NO_MATCH_WARN %
                               (", ".join(no_matchs)))

    def get_attending(self):
        return list(filter(lambda e: e[LOGOUT] is None, self.database))

    def sort_attendees(self, sort_list: typing.List[str]):
        def sorter(element: typing.Dict[str, typing.Any]):
            return tuple([element[col] for col in sort_list])

        self.database.sort(key=sorter)

    def __grouping_clear(self):
        for attendee in self.database:
            attendee[GROUP] = None

        for group in self.groups:
            group[GROUP_SIZE] = 0

    def __get_group(self, attendee):
        age_class = self.get_age_class(attendee)

        for group in self.groups:
            if re.match(group[GROUP_AGE_CLASSES], age_class) and \
                (group[GROUP_LIMIT] is None or
                    group[GROUP_SIZE] < group[GROUP_LIMIT]):
                attendee[GROUP] = group[GROUP_NAME]
                group[GROUP_SIZE] += 1
                return group[GROUP_NAME]

        return None

    def pack_age_table(self):
        data = {}
        total = [0, 0, 0]

        for age in self.ages:
            row = [0, 0, 0]

            row[0] = len(list(filter(lambda e, age=age:
                                     e[AGE] == age and
                                     e[GENDER].startswith(MALE),
                                     self.get_attending())))
            row[1] = len(list(filter(lambda e, age=age:
                                     e[AGE] == age and
                                     e[GENDER].startswith(FEMALE),
                                     self.get_attending())))
            row[2] = row[0] + row[1]

            data[str(age)] = row

            for i in range(3):
                total[i] += row[i]

        data[TOTAL] = total

        return data
