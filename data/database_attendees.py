import logging
import typing

ID = "ID"
CLUB = "Verein"
AGE = "Jahrgang"
LOGOUT = "Abmeldung"
GROUP = "Riege"
GENDER = "Geschlecht"
MALE = "m"
FEMALE = "w"

TOTAL = "Gesamt"


class DatabaseAttendees:
    def __init__(self):
        self.attendees: typing.List[typing.Dict[str, typing.Any]] = []
        self.clubs: typing.List[str] = []
        self.ages: typing.List[int] = []

    def clear_attendees(self):
        self.attendees = []

    def append_attendee(self, attendee):
        self.attendees.append(attendee)

    def get_attendees(self):
        return self.attendees

    def refresh_clubs(self):
        self.clubs = []
        for attendee in self.attendees:
            if CLUB in attendee:
                if attendee[CLUB] not in self.clubs:
                    self.clubs.append(attendee[CLUB])
        self.clubs.sort()

    def get_clubs(self):
        return self.clubs

    def refresh_ages(self):
        self.ages = []
        for attendee in self.attendees:
            if AGE in attendee:
                if attendee[AGE] not in self.ages:
                    self.ages.append(attendee[AGE])
        self.ages.sort()

    def get_ages(self):
        return self.ages

    def pack_club_table(self):
        data = {}
        total = [0, 0, 0]

        for club in self.clubs:
            row = [0, 0, 0]

            row[0] = len(list(filter(lambda e, club=club: e[CLUB] == club, self.attendees)))
            row[1] = len(list(filter(lambda e, club=club: e[CLUB] == club and e[LOGOUT] is not None,
                                     self.attendees)))
            row[2] = row[0] - row[1]

            data[club] = row

            for i in range(3):
                total[i] += row[i]

        data[TOTAL] = total

        return data

    def get_club_overview(self, club: str):
        return list(filter(lambda e, club=club: e[CLUB] == club, self.attendees))

    def get_age_class(self, attendee: typing.Dict[str, typing.Any]):
        spalte = attendee

        try:
            age_class = eval(self.settings["age_classifier"])
            return age_class
        except:
            logging.exception(
                "Fehler beim Erstellen der Alterklasse des Sportlers mit der ID %d.", attendee["ID"])
        return None

    def get_attending(self):
        return list(filter(lambda e: e[LOGOUT] is None, self.attendees))

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
