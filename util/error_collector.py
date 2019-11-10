import enum

class ErrorType(enum.IntEnum):
    NONE = 0
    WARNING = 1
    ERROR = 2

class ErrorEntry:
    def __init__(self, _type: ErrorType, message: str):
        self.type = _type
        self.message = message

class ErrorCollector:
    def __init__(self):
        self.entries = []
        self.global_state = ErrorType.NONE

    def append(self, _type: ErrorType, message: str):
        self.entries.append(ErrorEntry(_type, message))
        if self.global_state < _type:
            self.global_state = _type