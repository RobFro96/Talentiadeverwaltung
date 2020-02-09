"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import typing

GROUP_NAME = "Riegenname"
GROUP_AGE_CLASSES = "Altersklassen"
GROUP_LIMIT = "Maximalgröße"
GROUP_SIZE = "Größe"


class DatabaseGroups:
    """Datenbank der Riegen
    """

    def __init__(self):
        self.groups: typing.List[typing.Dict[str, typing.Any]] = []  # : Liste der Riegen

    def clear_groups(self):
        """Löschen aller Riegen aus der Datenbank
        """
        self.groups = []

    def append_group(self, group: typing.Dict[str, typing.Any]):
        """Hinzufügen einer Riege

        Args:
            group (typing.Dict[str, typing.Any]): Riege
        """
        self.groups.append(group)

    def get_groups(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Ausgeben aller Riegen der Datenbank

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Riegen
        """
        return self.groups
