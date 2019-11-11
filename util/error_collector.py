import enum
import tkinter.messagebox

INFO_CONSOLE_PREFIX = "[\033[92mINFO\033[0m] "
WARN_CONSOLE_PREFIX = "[\033[93mWARN\033[0m] "
ERROR_CONSOLE_PREFIX = "[\033[91mERROR\033[0m] "
INFO_MBOX_TITLE = "Information"
WARN_MBOX_TITLE = "Warnung"
ERROR_MBOX_TITLE = "Fehlermeldung"
WARN_MBOX_PREFIX = "\u26A0 "
ERROR_MBOX_PREFIX = "\u274C "

def print_info(message: str):
    ErrorCollector().append(ErrorType.NONE, str(message))

def print_warning(message: str):
    ErrorCollector().append(ErrorType.WARNING, str(message))

def print_error(message: str):
    ErrorCollector().append(ErrorType.ERROR, str(message))

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
        self.entries.append(ErrorEntry(_type, str(message)))
        if self.global_state < _type:
            self.global_state = _type

        if _type == ErrorType.NONE:
            print(INFO_CONSOLE_PREFIX + str(message))
        elif _type == ErrorType.WARNING:
            print(WARN_CONSOLE_PREFIX + str(message))
        elif _type == ErrorType.ERROR:
            print(ERROR_CONSOLE_PREFIX + str(message))
    
    def is_filled(self):
        return len(self.entries) > 0
    
    def has_warning(self):
        return self.global_state == ErrorType.WARNING
    
    def has_error(self):
        return self.global_state == ErrorType.ERROR
    
    def show_messagebox(self):
        if not self.entries:
            return

        if self.global_state == ErrorType.NONE:
            mbox = tkinter.messagebox.showinfo
            title = INFO_MBOX_TITLE
        elif self.global_state == ErrorType.WARNING:
            mbox = tkinter.messagebox.showwarning
            title = WARN_MBOX_TITLE
        elif self.global_state == ErrorType.ERROR:
            mbox = tkinter.messagebox.showerror
            title = ERROR_MBOX_TITLE
        
        text = ""
        entry: ErrorEntry
        for entry in self.entries:
            if text != "":
                text += "\n"

            if entry.type == ErrorType.WARNING:
                text += WARN_MBOX_PREFIX
            elif entry.type == ErrorType.ERROR:
                text += ERROR_MBOX_PREFIX
            
            text += entry.message

        mbox(title, text)

