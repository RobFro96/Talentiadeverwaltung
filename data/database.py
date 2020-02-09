"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import logging
import re
import typing

from data.database_attendees import GROUP, DatabaseAttendees
from data.database_groups import (GROUP_AGE_CLASSES, GROUP_LIMIT, GROUP_NAME,
                                  GROUP_SIZE, DatabaseGroups)
from data.database_sclasses import SCLASS_AGE_CLASSES, DatabaseSClasses
from data.database_stations import DatabaseStations


class Database(DatabaseGroups, DatabaseStations, DatabaseAttendees, DatabaseSClasses):
    """Datenbank, Erben von den einzelnen Klassen
    """

    def __init__(self, settings):
        self.settings = settings
        DatabaseGroups.__init__(self)
        DatabaseStations.__init__(self)
        DatabaseAttendees.__init__(self)
        DatabaseSClasses.__init__(self)

    def do_grouping(self):
        """Ordnet den Teilnehmern die entsprechenden Riege zu
        """
        self.sort_attendees(self.settings["group_sort_before"])
        self.__grouping_clear()

        no_matchs = []

        for attendee in self.get_attending():
            if not self.__get_group(attendee):
                no_matchs.append(str(attendee["ID"]))

        self.sort_attendees(self.settings["group_sort_after"])

        if no_matchs:
            logging.warning("Den folgenden Sportlern konnte keine Riege zugeordnet werden: %s",
                            ", ".join(no_matchs))

    def sort_attendees(self, sort_list: typing.List[str]):
        """Sortieren der Sportler nach den angegebenen Spalten

        Args:
            sort_list (typing.List[str]): Spalten
        """
        def sorter(element: typing.Dict[str, typing.Any]):
            return tuple([element[col] for col in sort_list])

        self.attendees.sort(key=sorter)

    def __grouping_clear(self):
        """Zurücksetzen der Werte der Riegeneinteilung
        """
        for attendee in self.attendees:
            attendee[GROUP] = None

        for group in self.groups:
            group[GROUP_SIZE] = 0

    def __get_group(self, attendee: typing.Dict[str, typing.Any]) -> str:
        """Zuordnen einer Riege dem entsprechenden Teilnehmer

        Args:
            attendee (typing.Dict[str, typing.Any]): Teilnehmer

        Returns:
            str: Bezeichnung der Riege
        """
        age_class = self.get_age_class(attendee)

        for group in self.groups:
            if re.match(group[GROUP_AGE_CLASSES], age_class) and \
                    (group[GROUP_LIMIT] is None or group[GROUP_SIZE] < group[GROUP_LIMIT]):
                attendee[GROUP] = group[GROUP_NAME]
                group[GROUP_SIZE] += 1
                return group[GROUP_NAME]

        return None

    def pack_group_table(self) -> typing.Dict[str, typing.List]:
        """Erstellen der Riegenübersicht für die GUI

        Returns:
            typing.Dict[str, typing.List]: Riegenübersicht
        """
        data = {}
        for group in self.groups:
            row = []
            row.append(group[GROUP_AGE_CLASSES])
            row.append(group[GROUP_LIMIT] or "\u221E")
            row.append(group[GROUP_SIZE])
            data[group[GROUP_NAME]] = row
        return data

    def get_group_overview(self, group: typing.Dict[str, typing.Any]) \
            -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt die Teilnehmer einer Gruppe zurück

        Args:
            group (typing.Dict[str, typing.Any]): [description]

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Teilnehmer
        """
        return list(filter(lambda e, group=group:
                           e[GROUP] == group[GROUP_NAME],
                           self.attendees))

    def get_process_steps(self, extra_groups=0, extra_stations=0) -> int:
        """Gibt zurück, wie viele Verarbeitungsschritte benötigt werden

        Args:
            extra_groups (int, optional): Extraschritte für Gruppen. Defaults to 0.
            extra_stations (int, optional): Extraschritte für Stationen. Defaults to 0.

        Returns:
            int: Schrittanzahl
        """
        return (len(self.groups) + extra_groups) * (len(self.stations) + extra_stations)

    def remove_all_scoring_values(self):
        """Entfernen aller Stationswerte aus der Datenbank
        """
        for col in self.get_all_station_scoring_columns():
            for attendee in self.get_attending():
                if col in attendee:
                    attendee.pop(col)

    @classmethod
    def save_as_json(cls, filename: str, obj: typing.Any):
        """Debug-Methode
        Speichern der Datenbank in Quasi-Json-Format (Python-Dict-Format)

        Args:
            filename (str): Dateiname
            obj (typing.Any): Beliebiges Objekt
        """
        with open(filename, "w", encoding="utf8") as json_file:
            json_file.write(repr(obj))

    def get_attendees_in_sclass(self, sclass: typing.Dict[str, typing.Any]) \
            -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt alle Teilnehmer einer Wertungsklasse zurück

        Args:
            sclass (typing.Dict[str, typing.Any]): Wertungsklasse

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Teilnehmer
        """
        def fiter_func(attendee):
            return re.match(sclass[SCLASS_AGE_CLASSES], self.get_age_class(attendee))

        return list(filter(fiter_func, self.get_attending()))
