import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from database.tarefas import add_tarefa, get_all_tarefas, delete_tarefa
from interface.Tarefas.AdicionarTarefa import AdicionarTarefa

class RegistroTarefas:
    """Popup para registrar, remover e atualizar possíveis tarefas."""
    def __init__(self, parent):
        self.parent = parent

        self.create_widgets()
        self.populate_tarefas_list()

    def create_widgets(self):
        # Gerar popup
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Tarefas")
        self.popup.transient(self.parent)

        # Frame principal do popup
        popup_frame = ttk.Frame(self.popup, padding=10)
        popup_frame.pack(fill="both", expand=True)

        # Frame mostrando todas as tarefas salvas
        list_frame = ttk.LabelFrame(popup_frame, text="Tarefas Cadastradas")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("id", "nome")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=200)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame botões de adicionar e deletar tarefa
        button_frame = ttk.Frame(popup_frame)
        button_frame.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(button_frame, text="Adicionar Tarefa", command=self.show_add_tarefa_popup).pack(side="left")
        ttk.Button(button_frame, text="Deletar Tarefa", command=self.delete_selected_tarefa).pack(side="left")

        # Centraliza o popup na janela pai
        self.popup.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        popup_width = self.popup.winfo_width()
        popup_height = self.popup.winfo_height()
        x = parent_x + (parent_width // 2) - (popup_width // 2)
        y = parent_y + (parent_height // 2) - (popup_height // 2)
        self.popup.geometry(f'+{x}+{y}')

        self.popup.grab_set()

    def populate_tarefas_list(self):
        """Preenche a lista de tarefas com as tarefas existentes."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tarefa in get_all_tarefas():
            self.tree.insert("", "end", values=tarefa)
    
    def save_tarefa(self, data, popup):
        """Lógica para salvar a tarefa, chamada pelo popup."""
        nome = data["nome"]

        if not nome:
            messagebox.showwarning("Campo Vazio", "O campo deve ser preenchido.", parent=popup)
            return
            
        try:
            add_tarefa(nome)
            self.populate_tarefas_list()
            popup.destroy() # Fecha o popup após o sucesso
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a tarefa: {e}", parent=popup)
    
    def show_add_tarefa_popup(self):
        """Cria o popup e passa a função de salvar como callback."""
        AdicionarTarefa(self, self.save_tarefa)

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
