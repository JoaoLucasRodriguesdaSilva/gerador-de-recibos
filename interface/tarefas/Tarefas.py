from tkinter import ttk, messagebox
from popup.PopupTarefa import PopupTarefa
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.tarefas import add_tarefa, get_all_tarefas, delete_tarefa

class TarefasFrame(ttk.Frame):
    def __init__(self, parent, show_receitas_callback):
        super().__init__(parent)
        
        self.create_widgets(show_receitas_callback)
        self.populate_tarefas_list()

    def create_widgets(self, show_receitas_callback):
        # --- Frame de Gerenciamento ---
        management_frame = ttk.LabelFrame(self, text="Gerenciar Tarefa")
        management_frame.pack(fill="x", padx=5, pady=5)

        # --- Botões de Ação ---
        button_frame = ttk.Frame(management_frame)
        button_frame.pack(pady=5, padx=5, anchor="w")
        ttk.Button(button_frame, text="Nova Tarefa", command=self.add_tarefa_entry).pack(side="left")
        ttk.Button(button_frame, text="Voltar para Receitas", command=show_receitas_callback).pack(side="left", padx=(5, 0))

        # --- Frame da Lista de Tarefas ---
        list_frame = ttk.LabelFrame(self, text="Tarefas Cadastradas")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("id", "nome")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Nome")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Botões da Lista ---
        list_button_frame = ttk.Frame(self)
        list_button_frame.pack(fill="x", padx=5, pady=(0, 5), anchor="w")
        ttk.Button(list_button_frame, text="Deletar Selecionada", command=self.delete_selected_tarefa).pack(side="left")

    def populate_tarefas_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for receita in get_all_tarefas():
            self.tree.insert("", "end", values=receita)

    def save_tarefa(self, data, popup):
        """Lógica para salvar a tarefa, chamada pelo popup."""
        nome = data["nome"]

        if not nome:
            messagebox.showwarning("Campo Vazio", "Todos os campos devem ser preenchidos.", parent=popup)
            return
            
        try:
            add_tarefa(nome)
            self.populate_tarefas_list()
            popup.destroy() # Fecha o popup após o sucesso
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a tarefa: {e}", parent=popup)

    def delete_selected_tarefa(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para deletar.")
            return

        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar a tarefa selecionada?"):
            try:
                tarefa_id = self.tree.item(selected_item[0], "values")[0]
                delete_tarefa(tarefa_id)
                self.populate_tarefas_list()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar a tarefa: {e}")

    def show_add_tarefa_popup(self):
        """Cria o popup e passa a função de salvar como callback."""
        PopupTarefa(self, self.save_tarefa)
