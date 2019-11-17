import tkinter.ttk


class GuiTable:
    def __init__(self, parent, headers, widths):
        self.treeview = tkinter.ttk.Treeview(parent)
        self.update_headers(headers, widths)

        self.vsb = tkinter.ttk.Scrollbar(parent, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.vsb.set)

        self.treeview.tag_configure("bold", font=(None, 9, "bold"))


    def update_headers(self, headers, widths):
        self.treeview.grid_remove()
        self.treeview.delete(*self.treeview.get_children())
        self.treeview["columns"] = [("col" + str(i))
                                    for i in range(len(headers) - 1)]
        self.treeview.heading("#0", text=headers[0], anchor="w")
        self.treeview.column("#0", anchor="w", width=widths[0], stretch=False)

        i = 0
        for header in headers[1:]:
            self.treeview.heading("col" + str(i), text=header)
            self.treeview.column(
                "col" + str(i), anchor='center', width=widths[i+1], stretch=False)
            i += 1

    def grid(self, *args, **kwargs):
        self.treeview.grid(*args, **kwargs)
    
    def grid_vsb(self, *args, **kwargs):
        self.vsb.grid(*args, **kwargs)


    def update(self, data, tags={}):
        self.treeview.delete(*self.treeview.get_children())
        for name, values in data.items():
            tag = tags[name] if name in tags else ()
            self.treeview.insert("", "end", text=name, values=values, tags=tag)
