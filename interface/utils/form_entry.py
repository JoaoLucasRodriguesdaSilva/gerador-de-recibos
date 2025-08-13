from tkinter import ttk

class FormEntry:
    def __init__(self, parent, label_text, placeholder="", width=40):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text=label_text)
        self.entry = ttk.Entry(self.frame, width=width)
        self.entry.insert(0, placeholder)
        self.label.grid(row=0, column=0, padx=5, sticky="w")
        self.entry.grid(row=1, column=0, padx=5)

    def get_entry_value(self):
        return self.entry.get()