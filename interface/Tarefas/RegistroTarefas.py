import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from database.tarefas import add_tarefa, get_all_tarefas, delete_tarefa
from interface.Tarefas.AdicionarTarefa.AdicionarTarefa import AdicionarTarefa

class RegistroTarefas:
    """Popup para registrar, remover e atualizar possíveis tarefas."""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self._create_widgets()
        self.populate_tarefas_list()

    def _create_widgets(self):
        """Cria e organiza os widgets da janela."""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Gerenciar Tarefas")
        self.popup.transient(self.parent)
        self.popup.resizable(False, False)

        popup_frame = ttk.Frame(self.popup, padding=10)
        popup_frame.pack(fill="both", expand=True)

        self._create_list_frame(popup_frame)
        self._create_buttons_frame(popup_frame)
        
        self._center_window()
        self.popup.grab_set()

    def _create_list_frame(self, parent: ttk.Frame):
        """Cria o frame com a lista de tarefas."""
        list_frame = ttk.LabelFrame(parent, text="Tarefas Cadastradas")
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("id", "nome")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=250, anchor="w")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_buttons_frame(self, parent: ttk.Frame):
        """Cria o frame com os botões de ação."""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(button_frame, text="Adicionar Tarefa", command=self.show_add_tarefa_popup).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(button_frame, text="Deletar Tarefa", command=self.delete_selected_tarefa).pack(side="left", padx=5, expand=True, fill="x")

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

    def populate_tarefas_list(self):
        """Preenche a lista de tarefas com as tarefas existentes."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            tarefas = get_all_tarefas()
            for tarefa in tarefas:
                self.tree.insert("", "end", values=tarefa)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tarefas: {e}", parent=self.popup)
    
    def save_tarefa(self, data: Dict[str, Any], popup: tk.Toplevel):
        """Lógica para salvar a tarefa, chamada pelo popup."""
        nome = data.get("nome", "").strip()

        if not nome:
            messagebox.showwarning("Campo Vazio", "O campo nome deve ser preenchido.", parent=popup)
            return
            
        try:
            add_tarefa(nome)
            self.populate_tarefas_list()
            popup.destroy()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!", parent=self.popup)
        except Exception as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a tarefa: {e}", parent=popup)
    
    def show_add_tarefa_popup(self):
        """Cria o popup e passa a função de salvar como callback."""
        AdicionarTarefa(self.popup, self.save_tarefa)

    def delete_selected_tarefa(self):
        """Deleta a tarefa selecionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para deletar.", parent=self.popup)
            return
            
        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar a tarefa selecionada?", parent=self.popup):
            try:
                tarefa_id = self.tree.item(selected_item[0], "values")[0]
                delete_tarefa(tarefa_id)
                self.populate_tarefas_list()
                messagebox.showinfo("Sucesso", "Tarefa removida com sucesso!", parent=self.popup)
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar a tarefa: {e}", parent=self.popup)
