from util.json_settings import JSONSettings
import tkinter
import os
from util.error_collector import ErrorCollector, ErrorType

class CompetitionLoader:
    def __init__(self, settings:JSONSettings):
        self.settings = settings
    
    def read_last_path(self) -> str:
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

    def open_dialog(self, initial_dir:str) -> str:
        return tkinter.filedialog.askdirectory(
            initialdir=initial_dir,
            title="Ordner der Veranstaltung auswählen")
    
    def load(self, folder: str, errors: ErrorCollector):
        if not os.path.isdir(folder):
            errors.append(ErrorType.ERROR, "Angegebner Ordner " + folder + " existiert nicht.")
            return None
        
        

