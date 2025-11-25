from tkinter import ttk, messagebox
import tkinter as tk
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.receitas import get_receita_by_id
from database.tarefas import get_all_tarefas
from database.receita_tarefa import add_tarefa_to_receita

class ReceitasTarefas:
    def __init__(self, parent, receita_id):
        self.parent = parent
        self.receita_id = receita_id
        self.receita = get_receita_by_id(receita_id)

        # Carrega tarefas e cria um mapa {Nome: ID} para salvar corretamente depois
        # O banco retorna tuplas (id, nome), então acessamos por índice
        tarefas_db = get_all_tarefas()
        self.tarefas_map = {t[1]: t[0] for t in tarefas_db}
        self.todas_tarefas = list(self.tarefas_map.keys())

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

        # Acessando por índice pois o retorno é uma tupla: (id, cliente, oficina, motor, placa, data)
        self.label_cliente = ttk.Label(self.receita_info_frame, text=f"Cliente: {self.receita[1]}")
        self.label_cliente.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        self.label_oficina = ttk.Label(self.receita_info_frame, text=f"Oficina: {self.receita[2]}")
        self.label_oficina.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        self.label_motor_cabecote = ttk.Label(self.receita_info_frame, text=f"Motor/Cabeçote: {self.receita[3]}")
        self.label_motor_cabecote.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.label_placa = ttk.Label(self.receita_info_frame, text=f"Placa: {self.receita[4]}")
        self.label_placa.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        self.label_data = ttk.Label(self.receita_info_frame, text=f"Data: {self.receita[5]}")
        self.label_data.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        self.atribuir_tarefa_frame = ttk.LabelFrame(self.popup, text="Atribuir Tarefa")
        self.atribuir_tarefa_frame.pack(fill="x", padx=5, pady=5, side="top")

        self.label_quantidade = ttk.Label(self.atribuir_tarefa_frame, text="Quantidade:")
        self.label_quantidade.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_quantidade = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_quantidade.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        self.label_tarefa = ttk.Label(self.atribuir_tarefa_frame, text="Tarefa:")
        self.label_tarefa.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        
        # Substituindo Combobox por Entry + Listbox customizada
        self.entry_tarefa = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_tarefa.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.entry_tarefa.bind("<KeyRelease>", self.on_tarefa_keyrelease)
        self.entry_tarefa.bind("<Down>", self.move_selection_down)
        self.entry_tarefa.bind("<Up>", self.move_selection_up)
        self.entry_tarefa.bind("<Return>", self.confirm_selection)
        self.entry_tarefa.bind("<FocusOut>", self.on_focus_out)

        # Listbox para sugestões (inicialmente escondida)
        # Mudamos o pai para self.popup para evitar que a lista seja cortada pelo frame
        self.lista_sugestoes = tk.Listbox(self.popup, height=5)
        self.lista_sugestoes.bind("<ButtonRelease-1>", self.on_sugestao_select)

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

        self.salvar_button = ttk.Button(self.popup, text="Adicionar à Lista", command=self.associar_tarefa)
        self.salvar_button.pack(side="bottom", padx=5, pady=5)

        self.remover_button = ttk.Button(self.popup, text="Remover da Lista", command=self.remover)
        self.remover_button.pack(side="bottom", padx=5, pady=5)

        self.btn_finalizar = ttk.Button(self.popup, text="Salvar no Banco e Fechar", command=self.salvar_no_banco)
        self.btn_finalizar.pack(side="bottom", padx=5, pady=5)

        # Label de Debug para identificar cliques
        self.lbl_debug = ttk.Label(self.popup, text="Último clique: Nenhum", foreground="red")
        self.lbl_debug.pack(side="bottom", padx=5, pady=2)

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
        
        self.setup_click_outside()

    def setup_click_outside(self):
        """Configura o evento de clique para tirar o foco dos campos de entrada."""
        self._bind_recursive(self.popup)

    def _bind_recursive(self, widget):
        """Aplica o bind recursivamente em widgets não interativos."""
        # Bind de debug em TODOS os widgets (add='+' para não sobrescrever eventos existentes)
        try:
            widget.bind("<Button-1>", self.update_debug_label, add="+")
        except Exception:
            pass

        # Lista de classes de widgets que devem manter seu comportamento padrão de clique
        # Usamos strings de classe (winfo_class) pois isinstance pode falhar em alguns contextos
        ignore_classes = (
            "TEntry", "Entry", "Text", "Listbox", "TCombobox", 
            "Button", "TButton", "Treeview", "Scrollbar", "TScrollbar"
        )
        
        try:
            if widget.winfo_class() not in ignore_classes:
                widget.bind("<Button-1>", self.check_focus_release, add="+")
        except Exception:
            pass
        
        for child in widget.winfo_children():
            self._bind_recursive(child)

    def update_debug_label(self, event):
        """Atualiza a label de debug com o tipo do widget clicado."""
        try:
            widget_type = event.widget.winfo_class()
            self.lbl_debug.config(text=f"Último clique: {widget_type}")
        except Exception:
            pass

    def check_focus_release(self, event):
        """Tira o foco se o widget focado atualmente for um Entry."""
        focused_widget = self.popup.focus_get()
        if focused_widget:
            try:
                # Verifica se o widget focado é um campo de texto pelo nome da classe
                if focused_widget.winfo_class() in ("TEntry", "Entry", "Text", "TCombobox"):
                    self.popup.focus_set()
            except Exception:
                pass

    def associar_tarefa(self):
        """Adiciona a tarefa à lista visual (não salva no banco ainda)."""
        quantidade = self.entry_quantidade.get()
        tarefa = self.entry_tarefa.get()
        valor = self.entry_valor.get()
        observacoes = self.entry_observacoes.get()

        if not all([quantidade, tarefa, valor]):
            messagebox.showwarning("Campo Vazio", "Campos obrigatórios devem ser preenchidos.", parent=self.popup)
            return
        
        # Valida se a tarefa existe no banco
        if tarefa not in self.tarefas_map:
            messagebox.showerror("Tarefa Inválida", "A tarefa selecionada não existe no banco de dados. Selecione uma tarefa da lista.", parent=self.popup)
            return
        
        # Validação de Quantidade e Valor
        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Quantidade deve ser um número inteiro válido.", parent=self.popup)
            return

        try:
            # Substitui vírgula por ponto para aceitar formato brasileiro
            valor = float(valor.replace(',', '.'))
            if valor < 0:
                raise ValueError("Valor não pode ser negativo.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Valor deve ser um número válido (ex: 100.00 ou 100,00).", parent=self.popup)
            return

        if not observacoes:
            observacoes = "N/D"

        # Adiciona à lista interna
        self.tarefas_associadas.append([tarefa, quantidade, valor, observacoes])
        self.update_list()

        # Limpa os campos para facilitar a próxima inserção
        self.entry_quantidade.delete(0, 'end')
        self.entry_tarefa.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        self.entry_observacoes.delete(0, 'end')
        self.entry_quantidade.focus_set()
        
        # Esconde a lista de sugestões se estiver aberta
        self.lista_sugestoes.place_forget()

    def salvar_no_banco(self):
        """Percorre a lista de tarefas e salva no banco de dados."""
        if not self.tarefas_associadas:
            messagebox.showwarning("Aviso", "Nenhuma tarefa na lista para salvar.", parent=self.popup)
            return

        try:
            for item in self.tarefas_associadas:
                # item = [tarefa_nome, quantidade, valor, observacoes]
                nome, qtd, val, obs = item
                
                # Busca o ID da tarefa pelo nome usando o mapa criado no __init__
                tarefa_id = self.tarefas_map.get(nome)
                
                if tarefa_id:
                    add_tarefa_to_receita(self.receita_id, tarefa_id, qtd, val, obs)
                else:
                    # Caso raro onde o nome não existe no mapa (ex: digitado manualmente e não selecionado)
                    print(f"Aviso: Tarefa '{nome}' não encontrada no banco. Ignorada.")
            
            messagebox.showinfo("Sucesso", "Tarefas salvas na receita com sucesso!", parent=self.popup)
            self.popup.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}", parent=self.popup)

    def update_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tarefa in self.tarefas_associadas:
            # Cria uma cópia para exibição para formatar o valor como moeda
            display_values = list(tarefa)
            # Formata o valor (índice 2)
            if isinstance(display_values[2], (int, float)):
                display_values[2] = f"R$ {display_values[2]:.2f}".replace('.', ',')
            
            self.tree.insert("", "end", values=display_values)
    
    def remover(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para deletar.")
            return

        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja remover esta tarefa da lista?"):
            try:
                # Remove pelo índice para evitar problemas com tipos de dados (str vs float/int)
                index = self.tree.index(selected_item[0])
                del self.tarefas_associadas[index]
                self.update_list()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível remover: {e}")

    def on_tarefa_keyrelease(self, event):
        """Filtra e mostra as sugestões conforme o usuário digita."""
        # Ignora teclas de navegação
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Return', 'Escape', 'Tab']:
            return

        typed_text = self.entry_tarefa.get()
        
        # Filtra as tarefas
        if not typed_text:
            filtered_list = self.todas_tarefas
        else:
            filtered_list = [tarefa for tarefa in self.todas_tarefas if typed_text.lower() in tarefa.lower()]
        
        # Atualiza a Listbox
        self.lista_sugestoes.delete(0, tk.END)
        for item in filtered_list:
            self.lista_sugestoes.insert(tk.END, item)
            
        # Posiciona e mostra a Listbox abaixo do Entry
        if filtered_list:
            # Calcula a posição relativa à janela popup, pois a lista agora é filha do popup
            x = self.entry_tarefa.winfo_rootx() - self.popup.winfo_rootx()
            y = self.entry_tarefa.winfo_rooty() - self.popup.winfo_rooty() + self.entry_tarefa.winfo_height()
            w = self.entry_tarefa.winfo_width()
            
            self.lista_sugestoes.place(x=x, y=y, width=w)
            self.lista_sugestoes.lift()
        else:
            self.lista_sugestoes.place_forget()

    def on_sugestao_select(self, event):
        """Preenche o campo com o valor selecionado na lista."""
        selection = self.lista_sugestoes.curselection()
        if selection:
            item = self.lista_sugestoes.get(selection[0])
            self.entry_tarefa.delete(0, tk.END)
            self.entry_tarefa.insert(0, item)
            self.lista_sugestoes.place_forget()
            self.entry_tarefa.focus_set()

    def move_selection_down(self, event):
        """Move a seleção da lista para baixo sem tirar o foco do Entry."""
        if self.lista_sugestoes.winfo_ismapped():
            current_selection = self.lista_sugestoes.curselection()
            if current_selection:
                index = current_selection[0] + 1
                if index < self.lista_sugestoes.size():
                    self.lista_sugestoes.selection_clear(0, tk.END)
                    self.lista_sugestoes.selection_set(index)
                    self.lista_sugestoes.activate(index)
                    self.lista_sugestoes.see(index)
            else:
                self.lista_sugestoes.selection_set(0)
                self.lista_sugestoes.activate(0)
            return "break"

    def move_selection_up(self, event):
        """Move a seleção da lista para cima sem tirar o foco do Entry."""
        if self.lista_sugestoes.winfo_ismapped():
            current_selection = self.lista_sugestoes.curselection()
            if current_selection:
                index = current_selection[0] - 1
                if index >= 0:
                    self.lista_sugestoes.selection_clear(0, tk.END)
                    self.lista_sugestoes.selection_set(index)
                    self.lista_sugestoes.activate(index)
                    self.lista_sugestoes.see(index)
            return "break"

    def confirm_selection(self, event):
        """Confirma a seleção atual da lista ao pressionar Enter."""
        if self.lista_sugestoes.winfo_ismapped():
            selection = self.lista_sugestoes.curselection()
            if selection:
                item = self.lista_sugestoes.get(selection[0])
                self.entry_tarefa.delete(0, tk.END)
                self.entry_tarefa.insert(0, item)
                self.lista_sugestoes.place_forget()
                return "break"

    def on_focus_out(self, event):
        """Agenda verificação para esconder a lista se o foco sair."""
        self.popup.after(100, self._check_focus_and_hide)

    def _check_focus_and_hide(self):
        """Esconde a lista se o foco não estiver nela nem no entry."""
        try:
            if not self.popup.winfo_exists():
                return
            focused = self.popup.focus_get()
            if focused != self.entry_tarefa and focused != self.lista_sugestoes:
                self.lista_sugestoes.place_forget()
        except Exception:
            pass