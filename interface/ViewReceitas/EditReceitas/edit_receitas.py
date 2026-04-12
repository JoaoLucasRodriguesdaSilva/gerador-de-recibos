import tkinter as tk
from tkinter import ttk
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from interface.utils.form_entry import FormEntry
from interface.utils.window_utils import center_window
from database.receitas import update_receita

class EditReceitas:
    def __init__(self, parent, receita):
        self.receita = receita

        # 1. Criar pop-up
        self.popup = tk.Toplevel(parent)
        self.popup.title(f"Editar Receita #{receita[0]}")
        self.popup.transient(parent)
        self.popup.grab_set()
        
        # 2. Criar frame com os dados pré-preenchidos de cliente, oficina, motor/cabeçote, placa, data
        self.create_form()

        # 3. Botão salvar que atualiza os dados no banco de dados e botão cancelar para fechar o pop-up
        self.create_buttons()

        center_window(self.popup, parent)

    def create_form(self):
        # Frame principal do formulário
        form_frame = ttk.Frame(self.popup, padding=20)
        form_frame.pack(fill="both", expand=True)
        
        # Desempacotar dados da receita: id, cliente, oficina, motor_cabecote, placa, data
        _, cliente, oficina, motor, placa, data = self.receita

        # Campos
        self.cliente_entry = FormEntry(form_frame, "Cliente:", cliente)
        self.cliente_entry.frame.pack(fill="x", pady=5)

        self.oficina_entry = FormEntry(form_frame, "Oficina:", oficina)
        self.oficina_entry.frame.pack(fill="x", pady=5)

        self.motor_entry = FormEntry(form_frame, "Motor/Cabeçote:", motor)
        self.motor_entry.frame.pack(fill="x", pady=5)

        self.placa_entry = FormEntry(form_frame, "Placa:", placa)
        self.placa_entry.frame.pack(fill="x", pady=5)

        self.data_entry = FormEntry(form_frame, "Data:", data)
        self.data_entry.frame.pack(fill="x", pady=5)

    def create_buttons(self):
        button_frame = ttk.Frame(self.popup, padding=20)
        button_frame.pack(fill="x", side="bottom")

        save_btn = ttk.Button(button_frame, text="Salvar", command=self.save_receita)
        save_btn.pack(side="left", padx=5, expand=True, anchor="e")

        cancel_btn = ttk.Button(button_frame, text="Cancelar", command=self.popup.destroy)
        cancel_btn.pack(side="left", padx=5, expand=True, anchor="w")

    def save_receita(self):
        cliente = self.cliente_entry.get_entry_value()
        oficina = self.oficina_entry.get_entry_value()
        motor = self.motor_entry.get_entry_value()
        placa = self.placa_entry.get_entry_value()
        data = self.data_entry.get_entry_value()
        
        update_receita(self.receita[0], cliente, oficina, motor, placa, data)
        self.popup.destroy()


