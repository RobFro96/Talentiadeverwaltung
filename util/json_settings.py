import json

class JSONSettings:
    def __init__(self, filename):
        self.filename = filename
        self.reload()
    
    def reload(self):
        self.changed = False
        with open(self.filename, "r", encoding="utf-8") as json_file:
            self.dict = json.load(json_file)
    
    def get(self, string: str, default=None):
        sub_dict = self.dict
        for element in string.split("."):
            if not element in sub_dict:
                return default
            sub_dict = sub_dict[element]
        return sub_dict
    
    def set(self, string: str, value: str):
        self.changed = True

        sub_dict = self.dict
        splitted = string.split(".")
        for element in splitted[:-1]:
            if not element in sub_dict:
                sub_dict[element] = {}
            sub_dict = sub_dict[element]
        sub_dict[splitted[-1]] = value
    
    def save(self, filename = None, force=False):
        if not (self.changed or force):
            return
        
        if filename == None:
            filename = self.filename

        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(self.dict, json_file)