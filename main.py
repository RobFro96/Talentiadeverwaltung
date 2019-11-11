#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter.filedialog
import os
from util.json_settings import JSONSettings
from initialization.competition_loader import CompetitionLoader
from util.error_collector import ErrorCollector

ICON_PATH = "util/icon.ico"
SETTINGS_FILE = "settings.json"

def main():
    root = tkinter.Tk()
    root.iconbitmap(ICON_PATH)
    root.withdraw()

    settings = JSONSettings(SETTINGS_FILE)

    competition_loader = CompetitionLoader(settings)

    folder = competition_loader.read_last_path()
    if not folder:
        folder = competition_loader.open_dialog(os.getcwd())
        if not folder:
            return
    errors = ErrorCollector()
    competition_loader.load(folder + "x", errors)
    errors.show_messagebox()

if __name__ == "__main__":
    main()