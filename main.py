#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter.filedialog
import os

class Main:
    def open(self):
        root = tkinter.Tk()
        root.iconbitmap("util/icon.ico")
        root.withdraw()

        folder = self.__read_last_path()
        if not folder:
            folder = self.__open_folder_dialog(os.getcwd())

        print(folder)
        
    def __read_last_path(self) -> str:
        filename = ".last_competition"
        
        if not os.path.exists(filename):
            print("Datei .last_competition exisitiert nicht.")
            return None
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return file.readline()
        except IOError:
            print("Fehler beim Lesen der Datei .last_competition.")
            return None
    
    def __open_folder_dialog(self, initial_dir) -> str:
        return tkinter.filedialog.askdirectory(initialdir=initial_dir, title="Ordner der Veranstaltung auswählen")

if __name__ == "__main__":
    main = Main()
    main.open()