import threading
import time
import tkinter
import tkinter.ttk


class ProgressTask(threading.Thread):
    def __init__(self, root):
        self.toplevel = tkinter.Toplevel(root)

        from main import ICON_PATH
        self.toplevel.iconbitmap(ICON_PATH)

        x = root.winfo_x()
        y = root.winfo_y()
        self.toplevel.geometry("300x50+%d+%d" % (x+10, y+10))
        self.toplevel.resizable(False, False)
        self.toplevel.grab_set()
        self.toplevel.transient(root)

        self.label = tkinter.Label(self.toplevel, text="Hallo")
        self.label.pack(side="top", fill="both")

        self.progress = tkinter.ttk.Progressbar(self.toplevel)
        self.progress.pack(fill="both")

        threading.Thread.__init__(self)

    def set_title(self, title: str):
        self.toplevel.title(title)

    def set_label(self, text: str):
        self.label.config(text=text)

    def set_progress(self, value: int, maximum: int):
        self.progress["maximum"] = maximum
        self.progress["value"] = value

    def run(self):
        for i in range(10):
            self.set_progress(i, 9)
            time.sleep(.5)
