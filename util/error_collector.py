import logging
import tkinter.messagebox

INFO_MBOX_TITLE = "Information"
WARN_MBOX_TITLE = "Warnung"
ERROR_MBOX_TITLE = "Fehlermeldung"
WARN_MBOX_PREFIX = "\u26A0 "
ERROR_MBOX_PREFIX = "\u274C "


class ErrorCollector(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.entries = []
        self.global_state = logging.INFO
        logging.getLogger().addHandler(self)

    def emit(self, record: logging.LogRecord):
        self.entries.append(record)

        if record.levelno > self.global_state:
            self.global_state = record.levelno

    def has_error(self):
        return self.global_state >= logging.ERROR

    def show_messagebox(self):
        self.remove()

        if not self.entries:
            return

        if self.global_state <= logging.INFO:
            mbox = tkinter.messagebox.showinfo
            title = INFO_MBOX_TITLE
        elif self.global_state <= logging.WARNING:
            mbox = tkinter.messagebox.showwarning
            title = WARN_MBOX_TITLE
        else:
            mbox = tkinter.messagebox.showerror
            title = ERROR_MBOX_TITLE

        text = ""
        for entry in self.entries:
            if text != "":
                text += "\n"

            if entry.levelno == logging.WARNING:
                text += WARN_MBOX_PREFIX
            elif entry.levelno == logging.ERROR:
                text += ERROR_MBOX_PREFIX

            text += str(entry.msg) % entry.args

        mbox(title, text)

    def remove(self):
        logging.getLogger().removeHandler(self)
