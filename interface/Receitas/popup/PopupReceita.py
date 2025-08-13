import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import add_receita, get_all_receitas
from interface.utils.form_entry import FormEntry

class PopupReceita:
    def __init__(self, parent):
        self.parent = parent

        self.popup = tk.Toplevel(parent)
        self.popup.title("Adicionar Receita")

        popup_frame = ttk.Frame(self.popup, padding=10)
        popup_frame.pack(fill="both", expand=True)

        # Campos para adicionar receita
        cliente_entry = FormEntry(popup_frame, "Cliente:")
        cliente_entry.frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        oficina_entry = FormEntry(popup_frame, "Oficina:")
        oficina_entry.frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        motor_entry = FormEntry(popup_frame, "Motor/Cabeçote:")
        motor_entry.frame.grid(row=2, column=0, sticky="ew", pady=(0, 5))

        placa_entry = FormEntry(popup_frame, "Placa:")
        placa_entry.frame.grid(row=3, column=0, sticky="ew", pady=(0, 5))

        data_entry = FormEntry(popup_frame, "Data:", datetime.now().strftime("%d/%m/%Y"))
        data_entry.frame.grid(row=4, column=0, sticky="ew", pady=(0, 5))

        save_command = lambda: self.save_receita(cliente_entry, oficina_entry, motor_entry, placa_entry, data_entry)

        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        SaveButton = ttk.Button(button_frame, text="Salvar", command=save_command)
        SaveButton.pack(side="left", padx=5)

        CancelButton = ttk.Button(button_frame, text="Cancelar", command=self.destroy)
        CancelButton.pack(side="left")

        # Centraliza o popup na tela
        self.popup.update_idletasks()
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        popup_width = self.popup.winfo_width()
        popup_height = self.popup.winfo_height()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        self.popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        self.popup.grab_set()

    def save_receita(self, cliente_entry, oficina_entry, motor_entry, placa_entry, data_entry):

            cliente = cliente_entry.get_entry_value()
            oficina = oficina_entry.get_entry_value()
            motor = motor_entry.get_entry_value()
            placa = placa_entry.get_entry_value()
            data = data_entry.get_entry_value()

            if not all([cliente, oficina, motor, placa, data]):
                messagebox.showwarning("Campo Vazio", "Todos os campos devem ser preenchidos.")
                return
                
            try:
                add_receita(cliente, oficina, motor, placa, data)
                self.populate_receitas_list()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a receita: {e}")
    
    def populate_receitas_list(self):
        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)
        for receita in get_all_receitas():
            self.parent.tree.insert("", "end", values=receita)

    def destroy(self):
        self.popup.destroy()
        self = None