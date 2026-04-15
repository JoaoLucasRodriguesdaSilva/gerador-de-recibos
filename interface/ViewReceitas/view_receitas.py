import tkinter as tk
from tkinter import ttk, messagebox

from database.receitas import get_receita_by_id, delete_receita
from database.receita_tarefa import get_tarefas_from_receita, remove_tarefa_from_receita
from interface.ReceitaTarefas.ReceitaTarefas import ReceitasTarefas
from interface.ViewReceitas.EditReceitas.edit_receitas import EditReceitas
from interface.utils.window_utils import center_window

class ViewReceita:
    """Janela popup para visualizar, editar e deletar uma receita e suas tarefas."""

    def __init__(self, parent, receita_id):
        self.parent = parent
        self.receita_id = receita_id
        
        # Busca os dados da receita no banco
        self.receita = get_receita_by_id(receita_id)
        
        self.create_widgets()

    def create_widgets(self):
        # Cria a janela popup
        self.popup = tk.Toplevel(self.parent)
        self.popup.title(f"Visualizar Receita #{self.receita_id}")
        self.popup.transient(self.parent)
        
        # Configuração inicial de tamanho (será ajustado pelo conteúdo, mas definimos um mínimo)
        self.popup.minsize(600, 400)
        self.popup.geometry("600x500")
        center_window(self.popup, self.parent)

        self.popup.grab_set()

        # --- Frame de Informações da Receita ---
        self.info_frame = ttk.LabelFrame(self.popup, text="Informações da Receita")
        self.info_frame.pack(fill="x", padx=10, pady=10)

        # Configuração de colunas para expandir
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(3, weight=1)

        # Linha 0
        ttk.Label(self.info_frame, text="Cliente:", font=("", 9, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        self.cliente_label = ttk.Label(self.info_frame, text=self.receita.cliente)
        self.cliente_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(self.info_frame, text="Motor/Cabeçote:", font=("", 9, "bold")).grid(row=0, column=2, sticky="e", padx=5, pady=2)
        self.motor_label = ttk.Label(self.info_frame, text=self.receita.motor_cabecote)
        self.motor_label.grid(row=0, column=3, sticky="w", padx=5, pady=2)

        # Linha 1
        ttk.Label(self.info_frame, text="Oficina:", font=("", 9, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        self.oficina_label = ttk.Label(self.info_frame, text=self.receita.oficina)
        self.oficina_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(self.info_frame, text="Placa:", font=("", 9, "bold")).grid(row=1, column=2, sticky="e", padx=5, pady=2)
        self.placa_label = ttk.Label(self.info_frame, text=self.receita.placa)
        self.placa_label.grid(row=1, column=3, sticky="w", padx=5, pady=2)

        # Linha 2
        ttk.Label(self.info_frame, text="Data:", font=("", 9, "bold")).grid(row=2, column=0, sticky="e", padx=5, pady=2)
        self.data_label = ttk.Label(self.info_frame, text=self.receita.data)
        self.data_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        # --- Frame de Tarefas ---
        self.tarefas_frame = ttk.LabelFrame(self.popup, text="Tarefas Associadas")
        self.tarefas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(self.tarefas_frame, columns=("id", "quantidade", "nome", "valor", "observacoes"), show="headings")
        
        scrollbar = ttk.Scrollbar(self.tarefas_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.configure(yscroll=scrollbar.set)

        # Coluna ID oculta
        self.tree.column("id", width=0, stretch=False)
        
        self.tree.heading("quantidade", text="Qtd")
        self.tree.heading("nome", text="Tarefa")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("observacoes", text="Observações")

        self.tree.column("quantidade", width=50, anchor="center")
        self.tree.column("nome", width=200, anchor="w")
        self.tree.column("valor", width=80, anchor="center")
        self.tree.column("observacoes", width=150, anchor="w")

        self.populate_tarefas()

        # --- Frame de Botões ---
        self.button_frame = ttk.Frame(self.popup)
        self.button_frame.pack(fill="x", padx=10, pady=10)
        
        # Configura grid para botões (2x2)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Botões Superiores
        ttk.Button(self.button_frame, text="Editar Receita", command=self.edit_receita).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(self.button_frame, text="Adicionar Tarefa", command=self.add_tarefa).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Botões Inferiores
        ttk.Button(self.button_frame, text="Deletar Receita", command=self.delete_receita_action).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(self.button_frame, text="Deletar Tarefa", command=self.delete_tarefa_action).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def populate_tarefas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        tarefas = get_tarefas_from_receita(self.receita_id)
        for t in tarefas:
            valor_fmt = f"R$ {t.valor:.2f}".replace('.', ',')
            self.tree.insert("", "end", values=(t.id, t.quantidade, t.nome, valor_fmt, t.observacoes))

    def update_info_labels(self):
        self.cliente_label.config(text=self.receita.cliente)
        self.oficina_label.config(text=self.receita.oficina)
        self.motor_label.config(text=self.receita.motor_cabecote)
        self.placa_label.config(text=self.receita.placa)
        self.data_label.config(text=self.receita.data)

    def edit_receita(self):
        edit_app = EditReceitas(self.popup, self.receita)
        self.popup.wait_window(edit_app.popup)
        
        # Recarrega dados
        self.receita = get_receita_by_id(self.receita_id)
        self.update_info_labels()

    def add_tarefa(self):
        # Abre a janela de adicionar tarefas
        app = ReceitasTarefas(self.popup, self.receita)
        self.popup.wait_window(app.popup)
        self.populate_tarefas()

    def delete_receita_action(self):
        if messagebox.askyesno("Confirmar Deleção", "Tem certeza que deseja deletar esta receita e todas as suas tarefas?", parent=self.popup):
            try:
                delete_receita(self.receita_id)
                messagebox.showinfo("Sucesso", "Receita deletada com sucesso.", parent=self.popup)
                self.popup.destroy()
                # Tenta atualizar a lista pai se o método existir
                if hasattr(self.parent, 'populate_receitas_list'):
                    self.parent.populate_receitas_list()
                # Caso o parent seja um frame dentro de outro container, pode ser necessário subir na hierarquia
                # Mas assumindo que parent é ReceitasFrame, deve funcionar.
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar receita: {e}", parent=self.popup)

    def delete_tarefa_action(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seleção Necessária", "Selecione uma tarefa para deletar.", parent=self.popup)
            return
        
        values = self.tree.item(selected_item[0], "values")
        tarefa_id = values[0]
        
        if messagebox.askyesno("Confirmar Deleção", "Tem certeza que deseja remover esta tarefa da receita?", parent=self.popup):
            try:
                remove_tarefa_from_receita(self.receita_id, tarefa_id)
                self.populate_tarefas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover tarefa: {e}", parent=self.popup)