#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Talentiadeverwaltung für Sportwettkämpfe der Ruderjugend Sachsen
Programm zum Einlesen, Bearbeiten und Abspeichern von Excel-Tabellen
von Robert Fromm (Ruderclub Eilenburg e. V.), Februar 2020
Email: robert_fromm@web.de
"""

import logging
import os
import tkinter.filedialog

import coloredlogs

from gui.main_form import ExitReason
from initialization.competition_loader import CompetitionLoader
from util.error_collector import ErrorCollector

coloredlogs.install(fmt='%(asctime)s,%(msecs)d %(levelname)-5s '
                    '[%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

ICON_PATH = "util/icon.ico"


def main(force_open=False):
    """Hauptfunktion

    Args:
        force_open (bool, optional): True, wenn Ordnerdialog erzwungen werden soll. Defaults to False.
    """
    # TKinter initialisieren
    root = tkinter.Tk()
    root.iconbitmap(ICON_PATH)
    root.withdraw()

    # Ordner abfragen, ggf. Dialog öffnen
    folder = CompetitionLoader.read_last_path()
    if not folder or force_open:
        folder = CompetitionLoader.open_dialog(os.getcwd())
        if not folder:
            return

    # Veranstaltung initialisieren
    errors = ErrorCollector()
    competition = CompetitionLoader.load(folder)
    if (competition is None) or errors.has_error():
        errors.show_messagebox()
        return
    else:
        errors.remove()

    # GUI öffnen, Aktionen beim Beenden
    reason = competition.open_gui(root)
    if reason == ExitReason.OPEN:
        main(True)
    elif reason == ExitReason.REFRESH:
        main()


if __name__ == "__main__":
    main()
