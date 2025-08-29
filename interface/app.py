import sys
import os
import tkinter as tk
from tkinter import ttk
from Receitas.receitas import ReceitasFrame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.criar_bd import create_table

class Main:
    def __init__(self, root):
        create_table()

        # --- Main Application Window ---
        self.root = root
        self.root.title("Gerenciador de Receitas")
        self.root.geometry("1024x600") # Set a default size

        # --- Frame Principal ---
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.show_receitas()

    def _clear_container(self):
        """Destrói todos os widgets filhos do frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_receitas(self):
        """Mostra página das receitas"""
        self._clear_container()
        self.receitas_frame = ReceitasFrame(self.main_frame)
        self.receitas_frame.pack(fill="both", expand=True)

root = tk.Tk()
app = Main(root)
root.mainloop()