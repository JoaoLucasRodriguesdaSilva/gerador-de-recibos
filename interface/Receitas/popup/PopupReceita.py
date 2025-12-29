import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Callable, Dict, Any
from interface.utils.form_entry import FormEntry

class PopupReceita:
    """Popup para adicionar uma nova receita."""
    
    def __init__(self, parent: tk.Widget, save_callback: Callable[[Dict[str, Any], tk.Toplevel], None]):
        self.parent = parent
        self.save_callback = save_callback

        # Gerar popup
        self.popup = tk.Toplevel(parent)
        self.popup.title("Adicionar Receita")
        self.popup.transient(parent)
        self.popup.resizable(False, False)

        # Frame principal do popup
        popup_frame = ttk.Frame(self.popup, padding=10)
        popup_frame.pack(fill="both", expand=True)
        popup_frame.columnconfigure(0, weight=1)

        # Campos para adicionar receita
        self.cliente_entry = FormEntry(popup_frame, "Cliente:")
        self.cliente_entry.frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.oficina_entry = FormEntry(popup_frame, "Oficina:")
        self.oficina_entry.frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        self.motor_entry = FormEntry(popup_frame, "Motor/Cabeçote:")
        self.motor_entry.frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

        self.placa_entry = FormEntry(popup_frame, "Placa:")
        self.placa_entry.frame.grid(row=3, column=0, sticky="ew", pady=(0, 5))

        self.data_entry = FormEntry(popup_frame, "Data:", datetime.now().strftime("%d/%m/%Y"))
        self.data_entry.frame.grid(row=4, column=0, sticky="ew", pady=(0, 5))

        # Frame que contém os botões
        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(row=5, column=0, pady=10)

        # Botões de salvar e cancelar
        self.save_button = ttk.Button(button_frame, text="Próximo", command=self.next_step)
        self.save_button.pack(side="left", padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.popup.destroy)
        self.cancel_button.pack(side="left")

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

    def next_step(self):
        """Coleta os dados, valida e chama a função de callback."""
        data = {
            "cliente": self.cliente_entry.get_entry_value().strip(),
            "oficina": self.oficina_entry.get_entry_value().strip(),
            "motor": self.motor_entry.get_entry_value().strip(),
            "placa": self.placa_entry.get_entry_value().strip(),
            "data": self.data_entry.get_entry_value().strip()
        }

        # Validação simples
        if not data["cliente"] or not data["oficina"]:
             messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha pelo menos Cliente e Oficina.", parent=self.popup)
             return

        self.save_callback(data, self.popup)
