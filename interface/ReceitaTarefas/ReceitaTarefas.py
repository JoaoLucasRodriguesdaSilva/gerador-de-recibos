from tkinter import ttk, messagebox
import tkinter as tk
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import get_receita_by_id
from database.tarefas import get_all_tarefas

class ReceitasTarefas:
    def __init__(self, parent, receita_id):
        self.parent = parent
        self.receita = get_receita_by_id(receita_id)

        self.create_widgets()
        self.tarefas_associadas = []
    
    def create_widgets(self):
        # Gerar popup
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Adicionar Receita")
        self.popup.transient(self.parent)

        # --- Frame de Informações da Receita ---
        self.receita_info_frame = ttk.LabelFrame(self.popup, text="Informações da Receita")
        self.receita_info_frame.pack(fill="x", padx=5, pady=5, side="top")

        self.label_cliente = ttk.Label(self.receita_info_frame, text=f"Cliente: {self.receita['cliente']}")
        self.label_cliente.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.label_oficina = ttk.Label(self.receita_info_frame, text=f"Oficina: {self.receita['oficina']}")
        self.label_oficina.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.label_motor_cabecote = ttk.Label(self.receita_info_frame, text=f"Motor/Cabeçote: {self.receita['motor_cabecote']}")
        self.label_motor_cabecote.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.label_placa = ttk.Label(self.receita_info_frame, text=f"Placa: {self.receita['placa']}")
        self.label_placa.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        self.label_data = ttk.Label(self.receita_info_frame, text=f"Data: {self.receita['data']}")
        self.label_data.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.atribuir_tarefa_frame = ttk.LabelFrame(self.popup, text="Atribuir Tarefa")
        self.atribuir_tarefa_frame.pack(fill="x", padx=5, pady=5, side="top")

        self.label_quantidade = ttk.Label(self.atribuir_tarefa_frame, text="Quantidade:")
        self.label_quantidade.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_quantidade = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_quantidade.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.label_tarefa = ttk.Label(self.atribuir_tarefa_frame, text="Tarefa:")
        self.label_tarefa.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_tarefa = ttk.Combobox(self.atribuir_tarefa_frame, values=self.get_all_tarefa_nomes())
        self.entry_tarefa.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.entry_tarefa.bind("<KeyRelease>", self.on_tarefa_search)

        self.label_valor = ttk.Label(self.atribuir_tarefa_frame, text="Valor:")
        self.label_valor.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_valor = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_valor.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        self.label_observacoes = ttk.Label(self.atribuir_tarefa_frame, text="Observações:")
        self.label_observacoes.grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.entry_observacoes = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_observacoes.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        self.tarefas_associadas_frame = ttk.LabelFrame(self.popup, text="Tarefas Associadas")
        self.tarefas_associadas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree = ttk.Treeview(self.tarefas_associadas_frame, columns=("nome", "quantidade", "valor", "observacoes"), show="headings")
        self.tree.pack(fill="both", expand=True)

        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("nome", text="Tarefa")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("observacoes", text="Observações")

        self.tree.column("quantidade", width=20, anchor="center")
        self.tree.column("nome", width=150, anchor="w")
        self.tree.column("valor", width=20, anchor="center")
        self.tree.column("observacoes", width=100, anchor="w")

        scrollbar = ttk.Scrollbar(self.tarefas_associadas_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar.set)

        self.salvar_button = ttk.Button(self.popup, text="Salvar", command=self.associar_tarefa)
        self.salvar_button.pack(side="bottom", padx=5, pady=5)

        self.remover_button = ttk.Button(self.popup, text="Remover", command=self.remover)
        self.remover_button.pack(side="bottom", padx=5, pady=5)

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

    def associar_tarefa(self):
        """Salva as informações da tarefa."""
        quantidade = self.entry_quantidade.get()
        tarefa = self.entry_tarefa.get()
        valor = self.entry_valor.get()
        observacoes = self.entry_observacoes.get()

        if not all([quantidade, tarefa, valor]):
            messagebox.showwarning("Campo Vazio", "Campos obrigatórios devem ser preenchidos.", parent=self)
            return
        
        if not observacoes:
            observacoes = "N/D"

        self.tarefas_associadas.append([quantidade, tarefa, valor, observacoes])
        self.update_list()

    def update_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tarefa in self.tarefas_associadas:
            self.tree.insert("", "end", values=tarefa)
    
    def remover(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para deletar.")
            return

        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar a tarefa selecionada?"):
            try:
                tarefa = self.tree.item(selected_item[0], "values")
                self.tarefas_associadas.remove(list(tarefa))
                self.update_list()
            except Exception as e:
                messagebox.showerror("Erro de Banco de Dados", f"Não foi possível deletar a tarefa: {e}")

    def on_tarefa_search(self, event):
        """Filtra a lista de tarefas no combobox com base no que o usuário digita."""
        typed_text = self.entry_tarefa.get()

        if not typed_text:
            # Se o campo estiver vazio, mostra todas as tarefas
            filtered_list = self.get_all_tarefa_nomes()
        else:
            # Filtra a lista de tarefas (case-insensitive)
            filtered_list = [tarefa for tarefa in self.get_all_tarefa_nomes() if typed_text.lower() in tarefa.lower()]

        # Atualiza os valores do combobox com a lista filtrada
        self.tarefa_combobox['values'] = filtered_list

    def get_all_tarefa_nomes(self):
        tarefas = get_all_tarefas()
        return [tarefa['nome'] for tarefa in tarefas]
