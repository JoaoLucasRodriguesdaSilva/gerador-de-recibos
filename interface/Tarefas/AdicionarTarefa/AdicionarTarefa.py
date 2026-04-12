import tkinter as tk
from tkinter import ttk
from typing import Callable, Any, Dict
from interface.utils.form_entry import FormEntry

class AdicionarTarefa:
    """Popup para adicionar uma nova tarefa."""
    
    def __init__(self, parent: tk.Widget, save_callback: Callable[[Dict[str, Any], tk.Toplevel], None]):
        self.parent = parent
        self.save_callback = save_callback
        self._create_widgets()

    def _create_widgets(self):
        """Cria e organiza os widgets da janela."""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Adicionar Tarefa")
        self.popup.transient(self.parent)
        self.popup.resizable(False, False)

        popup_frame = ttk.Frame(self.popup, padding=10)
        popup_frame.pack(fill="both", expand=True)
        popup_frame.columnconfigure(0, weight=1)

        # Campo para adicionar tarefa
        self.nome_entry = FormEntry(popup_frame, "Nome:")
        self.nome_entry.frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        # Frame que contém os botões
        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(row=1, column=0, pady=10)

        # Botões de salvar e cancelar
        ttk.Button(button_frame, text="Salvar", command=self.on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.popup.destroy).pack(side="left")

        self._center_window()
        self.popup.grab_set()

    def _center_window(self):
        """Centraliza o popup na janela pai."""
        self.popup.update_idletasks()
        width = self.popup.winfo_reqwidth()
        height = self.popup.winfo_reqheight()
        
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.popup.geometry(f"+{x}+{y}")

    def on_save(self):
        """Coleta os dados e chama a função de callback para salvar."""
        data = {"nome": self.nome_entry.get_entry_value()}
        self.save_callback(data, self.popup)
