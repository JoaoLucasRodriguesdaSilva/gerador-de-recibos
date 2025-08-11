from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import add_receita, get_all_receitas, delete_receita

class ReceitasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.populate_receitas_list()

    def create_widgets(self):
        # --- Frame de Gerenciamento ---
        management_frame = ttk.LabelFrame(self, text="Gerenciar Receita")
        management_frame.pack(fill="x", padx=5, pady=5)
        
        # --- Entradas de Dados ---
        ttk.Label(management_frame, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cliente_entry = ttk.Entry(management_frame, width=40)
        self.cliente_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(management_frame, text="Oficina:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.oficina_entry = ttk.Entry(management_frame, width=40)
        self.oficina_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(management_frame, text="Motor/Cabeçote:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.motor_entry = ttk.Entry(management_frame, width=40)
        self.motor_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(management_frame, text="Placa:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.placa_entry = ttk.Entry(management_frame, width=40)
        self.placa_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(management_frame, text="Data:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.data_entry = ttk.Entry(management_frame, width=40)
        self.data_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # --- Botões de Ação ---
        button_frame = ttk.Frame(management_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        ttk.Button(button_frame, text="Salvar Receita", command=self.save_receita).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpar Formulário", command=self.clear_form).pack(side="left", padx=5)

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

    def save_receita(self):
        cliente = self.cliente_entry.get()
        oficina = self.oficina_entry.get()
        motor = self.motor_entry.get()
        placa = self.placa_entry.get()
        data = self.data_entry.get()
        
        if not all([cliente, oficina, motor, placa, data]):
            messagebox.showwarning("Campo Vazio", "Todos os campos devem ser preenchidos.")
            return
            
        try:
            add_receita(cliente, oficina, motor, placa, data)
            self.clear_form()
            self.populate_receitas_list()
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

    def clear_form(self):
        self.cliente_entry.delete(0, "end")
        self.oficina_entry.delete(0, "end")
        self.motor_entry.delete(0, "end")
        self.placa_entry.delete(0, "end")
        self.data_entry.delete(0, "end")
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))