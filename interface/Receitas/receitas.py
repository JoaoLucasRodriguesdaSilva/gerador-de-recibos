from tkinter import ttk, messagebox
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import add_receita, get_all_receitas, delete_receita
from interface.Receitas.popup.PopupReceita import PopupReceita
from interface.Tarefas.RegistroTarefas import RegistroTarefas
from interface.ReceitaTarefas.ReceitaTarefas import ReceitasTarefas

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
        button_frame.pack(pady=5, padx=5, anchor="w")
        ttk.Button(button_frame, text="Nova Receita", command=self.show_add_receita_popup).pack(side="left")
        ttk.Button(button_frame, text="Tarefas Salvas", command=self.show_saved_tarefas_popup).pack(side="left")

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

    def save_receita(self, data, popup):
        """Lógica para salvar a receita, chamada pelo popup."""
        cliente = data["cliente"]
        oficina = data["oficina"]
        motor = data["motor"]
        placa = data["placa"]
        data_str = data["data"]

        if not all([cliente, oficina, motor, placa, data_str]):
            messagebox.showwarning("Campo Vazio", "Todos os campos devem ser preenchidos.", parent=popup)
            return
        
        try:
            add_receita(cliente, oficina, motor, placa, data_str)
            self.populate_receitas_list()
            popup.destroy() # Fecha o popup após o sucesso

            # Pega o ID do último item adicionado na Treeview
            last_item_id = self.tree.get_children()[-1]
            # Pega os valores desse item (o primeiro valor é o ID do banco de dados)
            db_receita_id = self.tree.item(last_item_id, "values")[0]

            # Abre o popup de tarefas para a nova receita, passando o ID correto
            ReceitasTarefas(self, receita_id=db_receita_id)
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a receita: {e}", parent=popup)

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
        """Cria o popup e passa a função de salvar como callback."""
        PopupReceita(self, self.save_receita)

    def show_saved_tarefas_popup(self):
        """Cria o popup de controle de tarefas."""
        RegistroTarefas(self)
