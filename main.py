#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter.filedialog
import os
from util.json_settings import JSONSettings
from competition.competition_loader import CompetitionLoader
from util.error_collector import ErrorCollector

def main():
    root = tkinter.Tk()
    root.iconbitmap("util/icon.ico")
    root.withdraw()

    settings = JSONSettings("settings.json")

    competition_loader = CompetitionLoader(settings)

    folder = competition_loader.read_last_path()
    if not folder:
        folder = competition_loader.open_dialog(os.getcwd())
        if not folder:
            return
    errors = ErrorCollector()
    competition_loader.load(folder, errors)

if __name__ == "__main__":
    main()