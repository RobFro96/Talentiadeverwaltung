"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
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
    """Teilnehmer-Datenbank
    """

    def __init__(self):
        self.attendees: typing.List[typing.Dict[str, typing.Any]] = []  # : Teilnehmer
        self.clubs: typing.List[str] = []  # : Liste der verschiedenen Vereine
        self.ages: typing.List[int] = []  # : Lister der verschiedenen Altersklassen

    def clear_attendees(self):
        """Löschen aller Teilnehmer aus der Datenbank
        """
        self.attendees = []

    def append_attendee(self, attendee: typing.Dict[str, typing.Any]):
        """Hinzufügen eines Teilnehmers zur Datenbank

        Args:
            attendee (typing.Dict[str, typing.Any]): Teilnehmer
        """
        self.attendees.append(attendee)

    def get_attendees(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt alle Teilnehmer der Veranstaltung zurück

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Teilnehmer
        """
        return self.attendees

    def refresh_clubs(self):
        """Aktualisieren der Liste der Vereine aus der Datenbank der Teilnehmer
        """
        self.clubs = []
        for attendee in self.attendees:
            if CLUB in attendee:
                if attendee[CLUB] not in self.clubs:
                    self.clubs.append(attendee[CLUB])
        self.clubs.sort()

    def get_clubs(self) -> typing.List[str]:
        """Gibt alle verschiedene Vereine der Veranstaltung zurück

        Returns:
            typing.List[str]: Vereine
        """
        return self.clubs

    def refresh_ages(self):
        """Aktualisieren der Liste der Altersklassen aus der Datenbank der Teilnehmer
        """
        self.ages = []
        for attendee in self.attendees:
            if AGE in attendee:
                if attendee[AGE] not in self.ages:
                    self.ages.append(attendee[AGE])
        self.ages.sort()

    def get_ages(self) -> typing.List[int]:
        """Gibt alle verschiedenne Altersklassen der Veranstaltung zurück

        Returns:
            typing.List[int]: Altersklassen
        """
        return self.ages

    def pack_club_table(self) -> typing.Dict[str, int]:
        """Erstellen der Vereinsübersicht für die Anzeige in der GUI

        Returns:
            typing.Dict[str, int]: Daten der Tabelle der Vereinsübersicht
        """
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

    def get_club_overview(self, club: str) -> typing.List[typing.Dict[str, typing.Any]]:
        """Filtert alle Teilnehmer des angegebenen Vereins

        Args:
            club (str): Name des Vereins

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Teilnehmer
        """
        return list(filter(lambda e, club=club: e[CLUB] == club, self.attendees))

    def get_age_class(self, attendee: typing.Dict[str, typing.Any]) -> str:
        """Erstellen der Altersklasse-Zeichenkette mit Geschlecht eines Teilnehmers

        Args:
            attendee (typing.Dict[str, typing.Any]): Teilnehmer

        Returns:
            str: Altersklassen-Zeichenkette
        """
        spalte = attendee

        try:
            age_class = eval(self.settings["age_classifier"])
            return age_class
        except:
            logging.exception(
                "Fehler beim Erstellen der Alterklasse des Sportlers mit der ID %d.", attendee["ID"])
        return None

    def get_attending(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt alle Teilnehmer zurück, die nicht abgemeldet wurden

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Teilnehmer
        """
        return list(filter(lambda e: e[LOGOUT] is None, self.attendees))

    def pack_age_table(self) -> typing.Dict[str, int]:
        """Erstellen der Altersübersicht über die Anzeige auf der GUI

        Returns:
            typing.Dict[str, int]: Anzeige
        """
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

    def filter_attendee(self, row_data: typing.Dict[str, typing.Any], required: typing.List[str]) \
            -> typing.Dict[str, typing.Any]:
        """Herausfiltern eines Teilnehmers aus der angegebenen Tabellenzeile
        Alle Werte die in der Liste required stehen, müssen übereinstimmen.
        Kann der Teilnehmer nicht eindeutig bestimmt werden, wird None zurückgegeben

        Args:
            row_data (typing.Dict[str, typing.Any]): Zeile
            required (typing.List[str]): Erforderliche Spalten

        Returns:
            typing.Dict[str, typing.Any]: Teilnehmer
        """
        def filter_func(attendee):
            for prop in required:
                if prop not in attendee:
                    return
                if attendee[prop] != row_data[prop]:
                    return False
            return True

        result = list(filter(filter_func, self.get_attending()))

        if len(result) != 1:
            return None
        return result[0]
