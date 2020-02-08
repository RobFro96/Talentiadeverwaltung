import logging
import re
import typing

from data.database_attendees import GROUP, DatabaseAttendees
from data.database_groups import (GROUP_AGE_CLASSES, GROUP_LIMIT, GROUP_NAME,
                                  GROUP_SIZE, DatabaseGroups)
from data.database_stations import DatabaseStations


class Database(DatabaseGroups, DatabaseStations, DatabaseAttendees):
    def __init__(self, settings):
        self.settings = settings
        DatabaseGroups.__init__(self)
        DatabaseStations.__init__(self)
        DatabaseAttendees.__init__(self)

    def do_grouping(self):
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
        def sorter(element: typing.Dict[str, typing.Any]):
            return tuple([element[col] for col in sort_list])

        self.attendees.sort(key=sorter)

    def __grouping_clear(self):
        for attendee in self.attendees:
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

    def pack_group_table(self):
        data = {}
        for group in self.groups:
            row = []
            row.append(group[GROUP_AGE_CLASSES])
            row.append(group[GROUP_LIMIT] or "\u221E")
            row.append(group[GROUP_SIZE])
            data[group[GROUP_NAME]] = row
        return data

    def get_group_overview(self, group):
        return list(filter(lambda e, group=group:
                           e[GROUP] == group[GROUP_NAME],
                           self.attendees))

    def get_process_steps(self, extra_groups=0, extra_stations=0):
        return (len(self.groups) + extra_groups) * (len(self.stations) + extra_stations)
