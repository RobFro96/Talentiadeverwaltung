"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""
import typing

SCLASS_WORKSHEET = "Tabellenblatt"
SCLASS_AGE_CLASSES = "Altersklassen"


class DatabaseSClasses:
    """Datenbank der Wertungsklassen (scoring classes)
    """

    def __init__(self):
        self.sclasses: typing.List[typing.Dict[str, typing.Any]] = []  # : Liste der Wertungsklassen

    def clear_sclasses(self):
        """Löschen aller Wertungsklassen aus der Datenbank
        """
        self.sclasses = []

    def append_sclass(self, sclass: typing.Dict[str, typing.Any]):
        """Hinzufügen einer Wertungsklasse zur Datenbank

        Args:
            sclass (typing.Dict[str, typing.Any]): Wertungsklasse
        """
        self.sclasses.append(sclass)

    def get_sclasses(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """Gibt alle Wertungsklassen zurück.

        Returns:
            typing.List[typing.Dict[str, typing.Any]]: Wertungsklassen
        """
        return self.sclasses
