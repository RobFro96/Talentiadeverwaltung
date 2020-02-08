import typing

GROUP_NAME = "Riegenname"
GROUP_AGE_CLASSES = "Altersklassen"
GROUP_LIMIT = "Maximalgröße"
GROUP_SIZE = "Größe"


class DatabaseGroups:
    def __init__(self):
        self.groups: typing.List[typing.Dict[str, typing.Any]] = []

    def clear_groups(self):
        self.groups = []

    def append_group(self, group):
        self.groups.append(group)

    def get_groups(self):
        return self.groups
