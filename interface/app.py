import sys
import os
import tkinter as tk
from tkinter import ttk

# Adiciona o diretório raiz ao path antes de importar módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface.Receitas.receitas import ReceitasFrame
from database.criar_bd import create_table

class MainApp:
    def __init__(self, root):
        """Cria a aplicação principal."""
        self.root = root
        self.root.title("Gerenciador de Receitas")
        
        # Centralizar a janela na tela
        window_width = 1024
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.container = ttk.Frame(root)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.show_page_receitas()
    
    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_page_receitas(self):
        self._clear_container()
        receitas_frame = ReceitasFrame(self.container)
        receitas_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    create_table()
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()