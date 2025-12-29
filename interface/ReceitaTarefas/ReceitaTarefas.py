from tkinter import ttk, messagebox
import tkinter as tk
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.tarefas import get_all_tarefas
from database.receita_tarefa import add_tarefa_to_receita
from database.receitas import add_receita
from gerador_pdf.gerador_recibo import gerar_pdf_orcamento

class ReceitasTarefas:
    def __init__(self, parent, receita):
        self.parent = parent
        self.receita = receita
        self.receita_id = receita[0]

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
        
        scrollbar = ttk.Scrollbar(self.tarefas_associadas_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("nome", text="Tarefa")
        self.tree.heading("valor", text="Valor")
        self.tree.heading("observacoes", text="Observações")

        self.tree.column("quantidade", width=20, anchor="center")
        self.tree.column("nome", width=150, anchor="w")
        self.tree.column("valor", width=20, anchor="center")
        self.tree.column("observacoes", width=100, anchor="w")

        self.tree.configure(yscroll=scrollbar.set)

        # Frame para botões
        self.buttons_frame = ttk.Frame(self.popup)
        self.buttons_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        self.salvar_button = ttk.Button(self.buttons_frame, text="Adicionar à Lista", command=self.associar_tarefa)
        self.salvar_button.pack(side="left", padx=5, expand=True, fill="x")

        self.remover_button = ttk.Button(self.buttons_frame, text="Remover da Lista", command=self.remover)
        self.remover_button.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_finalizar = ttk.Button(self.buttons_frame, text="Salvar no Banco e Fechar", command=self.salvar_no_banco)
        self.btn_finalizar.pack(side="left", padx=5, expand=True, fill="x")

        # Centraliza o popup na janela pai
        self.popup.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        popup_width = self.popup.winfo_width()
        popup_height = self.popup.winfo_height()
        x = parent_x + (parent_width // 2) - (popup_width // 2)
        y = parent_y + (parent_height // 2) - (popup_height // 2)
        self.popup.geometry(f'+{x}+{y}')

        self.popup.grab_set()

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
            # Se a receita ainda não tem ID (é nova), salva ela primeiro
            if self.receita_id is None:
                _, cliente, oficina, motor, placa, data_str = self.receita
                self.receita_id = add_receita(cliente, oficina, motor, placa, data_str)
                
                # Atualiza a lista na janela principal se possível
                if hasattr(self.parent, 'populate_receitas_list'):
                    self.parent.populate_receitas_list()

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
            
            # Gera o PDF do recibo
            self.gerar_pdf_recibo()

            messagebox.showinfo("Sucesso", f"Receita salva e PDF gerado (recibo_{self.receita_id}.pdf)!", parent=self.popup)
            self.popup.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}", parent=self.popup)

    def gerar_pdf_recibo(self):
        """Coleta os dados e chama o gerador de PDF."""
        receita_dict = {
            "cliente": self.receita[1],
            "oficina": self.receita[2],
            "motor_cabecote": self.receita[3],
            "placa": self.receita[4],
            "data": self.receita[5]
        }
        
        tarefas_list = []
        for item in self.tarefas_associadas:
            tarefas_list.append({
                "descricao": item[0],
                "quantidade": item[1],
                "valor": item[2],
                "observacao": item[3]
            })
            
        # Define o caminho para salvar o PDF na pasta 'receitas' na raiz do projeto
        recibos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../receitas'))
        os.makedirs(recibos_dir, exist_ok=True)
        
        output_file = os.path.join(recibos_dir, f"recibo_{self.receita_id}.pdf")
        
        try:
            gerar_pdf_orcamento(receita_dict, tarefas_list, output_file)
            print(f"PDF gerado em: {output_file}")
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            # Não impede o fluxo principal, apenas loga o erro (ou poderia mostrar um aviso)
            messagebox.showwarning("Aviso PDF", f"Receita salva, mas erro ao gerar PDF: {e}", parent=self.popup)

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