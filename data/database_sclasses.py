import typing

SCLASS_WORKSHEET = "Tabellenblatt"
SCLASS_AGE_CLASSES = "Altersklassen"


class DatabaseSClasses:
    def __init__(self):
        self.sclasses: typing.List[typing.Dict[str, typing.Any]] = []

    def clear_sclasses(self):
        self.sclasses = []

    def append_sclass(self, sclass):
        self.sclasses.append(sclass)

    def get_sclasses(self):
        return self.sclasses
