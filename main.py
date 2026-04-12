import sys
import os

# Garante que a raiz do projeto esteja no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from database.criar_bd import create_table
from interface.app import MainApp

if __name__ == "__main__":
    # Garante que o banco de dados existe
    create_table()
    
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
