import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import Dict, Any

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import get_all_receitas, delete_receita
from interface.Receitas.popup.PopupReceita import PopupReceita
from interface.Tarefas.RegistroTarefas import RegistroTarefas
from interface.ReceitaTarefas.ReceitaTarefas import ReceitasTarefas
from interface.ViewReceitas.view_receitas import ViewReceita

class ReceitasFrame(ttk.Frame):
    """Frame principal para gerenciamento e visualização de receitas."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        
        self.create_widgets()
        self.populate_receitas_list()

    def create_widgets(self):
        """Cria os componentes da interface."""
        # --- Frame de Gerenciamento ---
        management_frame = ttk.LabelFrame(self, text="Gerenciar Receita")
        management_frame.pack(fill="x", padx=5, pady=5)

        # --- Botões de Ação ---
        button_frame = ttk.Frame(management_frame)
        button_frame.pack(pady=5, padx=5, anchor="w")
        
        ttk.Button(button_frame, text="Nova Receita", command=self.show_add_receita_popup).pack(side="left", padx=(0, 5))
        ttk.Button(button_frame, text="Tarefas Salvas", command=self.show_saved_tarefas_popup).pack(side="left")
        ttk.Button(button_frame, text="Atualizar Lista", command=self.populate_receitas_list).pack(side="left", padx=(5, 0))

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
        ttk.Button(list_button_frame, text="Visualizar Selecionada", command=self.view_selected_receita).pack(side="left", padx=(0, 5))
        ttk.Button(list_button_frame, text="Deletar Selecionada", command=self.delete_selected_receita).pack(side="left")

    def populate_receitas_list(self):
        """Busca as receitas no banco e popula a Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            receitas = get_all_receitas()
            for receita in receitas:
                self.tree.insert("", "end", values=receita)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar receitas: {e}")

    def save_receita(self, data: Dict[str, Any], popup: tk.Toplevel):
        """
        Callback chamado pelo PopupReceita.
        Fecha o popup inicial e abre a tela de adição de tarefas.
        """
        # Validação básica já feita no popup, mas reforçamos aqui se necessário
        cliente = data.get("cliente")
        oficina = data.get("oficina")
        motor = data.get("motor")
        placa = data.get("placa")
        data_str = data.get("data")

        if not all([cliente, oficina, motor, placa, data_str]):
            messagebox.showwarning("Campo Vazio", "Todos os campos devem ser preenchidos.", parent=popup)
            return
        
        # Fecha o popup de dados da receita
        popup.destroy()

        # Abre o popup de tarefas para a nova receita
        # Passamos None como ID pois a receita ainda não foi salva no banco
        # A classe ReceitasTarefas lidará com a criação do registro no banco
        nova_receita = (None, cliente, oficina, motor, placa, data_str)
        ReceitasTarefas(self, receita=nova_receita)

    def view_selected_receita(self):
        """Abre a visualização detalhada da receita selecionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma receita para visualizar.")
            return
        
        # O primeiro valor da tupla values é o ID
        try:
            receita_id = self.tree.item(selected_item[0], "values")[0]
            ViewReceita(self, receita_id)
        except IndexError:
            messagebox.showerror("Erro", "Erro ao recuperar ID da receita selecionada.")

    def delete_selected_receita(self):
        """Deleta a receita selecionada após confirmação."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma receita para deletar.")
            return
            
        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar a receita selecionada?"):
            try:
                receita_id = self.tree.item(selected_item[0], "values")[0]
                delete_receita(receita_id)
                self.populate_receitas_list()
                messagebox.showinfo("Sucesso", "Receita deletada com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar a receita: {e}")

    def show_add_receita_popup(self):
        """Cria o popup e passa a função de salvar como callback."""
        PopupReceita(self, self.save_receita)

    def show_saved_tarefas_popup(self):
        """Cria o popup de controle de tarefas."""
        RegistroTarefas(self)
