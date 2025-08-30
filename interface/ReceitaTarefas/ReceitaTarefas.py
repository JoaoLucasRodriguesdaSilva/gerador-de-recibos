from tkinter import ttk
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
    
    def create_widgets(self):
        # --- Frame de Informações da Receita ---
        self.receita_info_frame = ttk.LabelFrame(self, text="Informações da Receita")
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

        self.atribuir_tarefa_frame = ttk.LabelFrame(self, text="Atribuir Tarefa")
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

        self.tarefas_associadas_frame = ttk.LabelFrame(self, text="Tarefas Associadas")
        self.tarefas_associadas_frame.pack(fill="x", padx=5, pady=5, side="top")

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
