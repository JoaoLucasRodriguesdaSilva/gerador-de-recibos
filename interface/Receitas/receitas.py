import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import add_receita, get_all_receitas, delete_receita
from interface.utils.form_entry import FormEntry

class ReceitasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.populate_receitas_list()

    def create_widgets(self):
        # --- Frame de Gerenciamento ---
        management_frame = ttk.LabelFrame(self, text="Gerenciar Receita")
        management_frame.pack(fill="x", padx=5, pady=5)

        # --- Botões de Ação ---
        button_frame = ttk.Frame(management_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(button_frame, text="Nova Receita", command=self.show_add_receita_popup).pack(side="left", padx=5)

        # --- Frame da Lista de Receitas ---
        list_frame = ttk.LabelFrame(self, text="Receitas Cadastradas")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("id", "cliente", "oficina", "motor_cabecote", "placa", "data")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("oficina", text="Oficina")
        self.tree.heading("motor_cabecote", text="Motor/Cabeçote")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("data", text="Data")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cliente", width=200)
        self.tree.column("oficina", width=200)
        self.tree.column("motor_cabecote", width=150)
        self.tree.column("placa", width=100, anchor="center")
        self.tree.column("data", width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Botões da Lista ---
        list_button_frame = ttk.Frame(self)
        list_button_frame.pack(fill="x", padx=5, pady=(0, 5), anchor="w")
        ttk.Button(list_button_frame, text="Deletar Selecionada", command=self.delete_selected_receita).pack(side="left")

    def populate_receitas_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for receita in get_all_receitas():
            self.tree.insert("", "end", values=receita)

    def save_receita(self, popup, cliente_entry, oficina_entry, motor_entry, placa_entry, data_entry):

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
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a receita: {e}")

    def delete_selected_receita(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma receita para deletar.")
            return
            
        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar a receita selecionada?"):
            try:
                receita_id = self.tree.item(selected_item[0], "values")[0]
                delete_receita(receita_id)
                self.populate_receitas_list()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar a receita: {e}")

    def show_add_receita_popup(self):
        # Inicia o popup
        popup = tk.Toplevel(self)
        popup.title("Adicionar Receita")

        popup_frame = ttk.Frame(popup, padding=10)
        popup_frame.pack(fill="both", expand=True)

        # Campos para adicionar receita
        cliente_entry = FormEntry(popup_frame, "Cliente:")
        cliente_entry.frame.grid(row=0, column=0, sticky="ew", pady=5)

        oficina_entry = FormEntry(popup_frame, "Oficina:")
        oficina_entry.frame.grid(row=1, column=0, sticky="ew")

        motor_entry = FormEntry(popup_frame, "Motor/Cabeçote:")
        motor_entry.frame.grid(row=2, column=0, sticky="ew")

        placa_entry = FormEntry(popup_frame, "Placa:")
        placa_entry.frame.grid(row=3, column=0, sticky="ew")

        data_entry = FormEntry(popup_frame, "Data:", datetime.now().strftime("%d/%m/%Y"))
        data_entry.frame.grid(row=4, column=0, sticky="ew")

        save_command = lambda: self.save_receita(popup, cliente_entry, oficina_entry, motor_entry, placa_entry, data_entry)

        button_frame = ttk.Frame(popup_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        SaveButton = ttk.Button(button_frame, text="Salvar", command=save_command)
        SaveButton.pack(side="left", padx=5)

        CancelButton = ttk.Button(button_frame, text="Cancelar", command=popup.destroy)
        CancelButton.pack(side="left")

        # Centraliza o popup na tela
        popup.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        popup.grab_set()
