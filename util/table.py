import os

import openpyxl
import tkinter.messagebox

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Table:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.path = os.path.join(folder, filename)

    def open(self) -> str:
        try:
            self.workbook = openpyxl.open(self.path)
        except:
            return False
        return True
    
    def write(self, folder=None, filename=None) -> str:
        if not folder:
            folder = self.folder
        if not filename:
            filename = self.filename
        path = os.path.join(folder, filename)

        self.check_lock(folder, filename)

        try:
            self.workbook.save(path)
        except:
            return False
        return True
    
    def check_lock(self, folder, filename):
        path1 = os.path.join(folder, ".~lock." + filename + "#")
        path2 = os.path.join(folder, "~$" + filename)

        if os.path.exists(path1) or os.path.exists(path2):
            tkinter.messagebox.showwarning("Warnung", "Die Datei " + filename + " ist gerade von einem anderen Programm geöffnet.")

    def column_letter_to_number(self, col_letter):
        if len(col_letter) == 1:
            return ALPHABET.index(col_letter.upper()) + 1
        else:
            first_digit = ALPHABET.index(col_letter[0].upper()) + 1
            second_digit = ALPHABET.index(col_letter[1].upper()) + 1
            return first_digit * 26 + second_digit
    
    def column_number_to_letter(self, col_number):
        return ALPHABET[col_number - 1]