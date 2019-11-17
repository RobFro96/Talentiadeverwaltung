#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tkinter.filedialog

from gui.main_form import ExitReason
from initialization.competition_loader import CompetitionLoader
from util.error_collector import ErrorCollector

ICON_PATH = "util/icon.ico"
SETTINGS_FILE = "settings.json"

def main(force_open=False):
    root = tkinter.Tk()
    root.iconbitmap(ICON_PATH)
    root.withdraw()

    competition_loader = CompetitionLoader()

    folder = competition_loader.read_last_path()
    if not folder or force_open:
        folder = competition_loader.open_dialog(os.getcwd())
        if not folder:
            return

    errors = ErrorCollector()
    competition = competition_loader.load(folder, errors)
    errors.show_messagebox()
    if competition is None:
        return

    reason = competition.open_gui(root)
    if reason == ExitReason.OPEN:
        main(True)
    elif reason == ExitReason.REFRESH:
        main()

if __name__ == "__main__":
    main()
