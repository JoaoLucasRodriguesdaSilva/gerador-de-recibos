import os
import tkinter as tk
from tkinter import ttk

from interface.Receitas.receitas import ReceitasFrame
from interface.utils.app_paths import get_resource_path

class MainApp:
    def __init__(self, root):
        """Cria a aplicação principal."""
        self.root = root
        self.root.title("Gerenciador de Receitas")
        
        # Tenta carregar o ícone da janela usando o caminho correto do recurso
        try:
            icon_path_ico = get_resource_path("FrangoAmelia.ico")
            icon_path_png = get_resource_path("FrangoAmelia.png")

            # Para Windows (.ico)
            if os.path.exists(icon_path_ico):
                self.root.iconbitmap(icon_path_ico)
            # Para Linux/Mac (.png)
            elif os.path.exists(icon_path_png):
                icon = tk.PhotoImage(file=icon_path_png)
                self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
        
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

