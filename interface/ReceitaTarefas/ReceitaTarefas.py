import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from typing import List, Tuple, Optional, Dict, Any

# Adiciona o diretório raiz do projeto ao sys.path para encontrar os módulos do banco de dados
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.tarefas import get_all_tarefas
from database.receita_tarefa import add_tarefa_to_receita
from database.receitas import add_receita
from gerador_pdf.gerador_recibo import gerar_pdf_orcamento

class ReceitasTarefas:
    """Janela para associar tarefas a uma receita e gerar o recibo."""

    def __init__(self, parent: tk.Widget, receita: Tuple[Optional[int], str, str, str, str, str]):
        self.parent = parent
        self.receita = receita
        self.receita_id = receita[0]

        self.tarefas_map: Dict[str, int] = {}
        self.todas_tarefas: List[str] = []
        self.tarefas_associadas: List[List[Any]] = []

        self._load_tarefas()
        self._create_widgets()
    
    def _load_tarefas(self):
        """Carrega as tarefas do banco de dados."""
        try:
            tarefas_db = get_all_tarefas()
            self.tarefas_map = {t[1]: t[0] for t in tarefas_db}
            self.todas_tarefas = list(self.tarefas_map.keys())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tarefas: {e}")
            self.todas_tarefas = []

    def _create_widgets(self):
        """Inicializa a interface gráfica."""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Adicionar Tarefas")
        self.popup.transient(self.parent)
        self.popup.resizable(False, False)

        self._create_info_frame()
        self._create_input_frame()
        self._create_list_frame()
        self._create_buttons_frame()
        
        self._center_window()
        self.popup.grab_set()

    def _create_info_frame(self):
        """Cria o frame com informações da receita."""
        frame = ttk.LabelFrame(self.popup, text="Informações da Receita")
        frame.pack(fill="x", padx=5, pady=5, side="top")

        # Labels com grid
        labels = [
            (f"Cliente: {self.receita[1]}", 0, 0),
            (f"Motor/Cabeçote: {self.receita[3]}", 0, 1),
            (f"Oficina: {self.receita[2]}", 1, 0),
            (f"Placa: {self.receita[4]}", 1, 1),
            (f"Data: {self.receita[5]}", 2, 0),
        ]

        for text, row, col in labels:
            ttk.Label(frame, text=text).grid(row=row, column=col, padx=5, pady=2, sticky="w")

    def _create_input_frame(self):
        """Cria o frame de entrada de tarefas."""
        self.atribuir_tarefa_frame = ttk.LabelFrame(self.popup, text="Atribuir Tarefa")
        self.atribuir_tarefa_frame.pack(fill="x", padx=5, pady=5, side="top")

        # Linha 1
        ttk.Label(self.atribuir_tarefa_frame, text="Quantidade:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_quantidade = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_quantidade.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(self.atribuir_tarefa_frame, text="Tarefa:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_tarefa = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_tarefa.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        
        # Bindings para autocomplete
        self.entry_tarefa.bind("<KeyRelease>", self.on_tarefa_keyrelease)
        self.entry_tarefa.bind("<Down>", self.move_selection_down)
        self.entry_tarefa.bind("<Up>", self.move_selection_up)
        self.entry_tarefa.bind("<Return>", self.confirm_selection)
        self.entry_tarefa.bind("<FocusOut>", self.on_focus_out)

        # Listbox de sugestões
        self.lista_sugestoes = tk.Listbox(self.popup, height=5)
        self.lista_sugestoes.bind("<ButtonRelease-1>", self.on_sugestao_select)

        # Linha 2
        ttk.Label(self.atribuir_tarefa_frame, text="Valor:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_valor = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_valor.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(self.atribuir_tarefa_frame, text="Observações:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.entry_observacoes = ttk.Entry(self.atribuir_tarefa_frame)
        self.entry_observacoes.grid(row=1, column=3, padx=5, pady=2, sticky="w")

    def _create_list_frame(self):
        """Cria o frame com a lista de tarefas associadas."""
        frame = ttk.LabelFrame(self.popup, text="Tarefas Associadas")
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        columns = ("nome", "quantidade", "valor", "observacoes")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        headers = {
            "quantidade": ("Quantidade", 20, "center"),
            "nome": ("Tarefa", 150, "w"),
            "valor": ("Valor", 20, "center"),
            "observacoes": ("Observações", 100, "w")
        }

        for col, (text, width, anchor) in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

    def _create_buttons_frame(self):
        """Cria o frame de botões de ação."""
        frame = ttk.Frame(self.popup)
        frame.pack(side="bottom", fill="x", padx=5, pady=5)

        ttk.Button(frame, text="Adicionar à Lista", command=self.associar_tarefa).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(frame, text="Remover da Lista", command=self.remover).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(frame, text="Salvar no Banco e Fechar", command=self.salvar_no_banco).pack(side="left", padx=5, expand=True, fill="x")

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

    def associar_tarefa(self):
        """Adiciona a tarefa à lista visual (não salva no banco ainda)."""
        quantidade = self.entry_quantidade.get().strip()
        tarefa = self.entry_tarefa.get().strip()
        valor = self.entry_valor.get().strip()
        observacoes = self.entry_observacoes.get().strip()

        if not all([quantidade, tarefa, valor]):
            messagebox.showwarning("Campo Vazio", "Campos obrigatórios devem ser preenchidos.", parent=self.popup)
            return
        
        if tarefa not in self.tarefas_map:
            messagebox.showerror("Tarefa Inválida", "A tarefa selecionada não existe no banco de dados. Selecione uma tarefa da lista.", parent=self.popup)
            return
        
        try:
            qtd_int = int(quantidade)
            if qtd_int <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Quantidade deve ser um número inteiro válido.", parent=self.popup)
            return

        try:
            val_float = float(valor.replace(',', '.'))
            if val_float < 0:
                raise ValueError("Valor não pode ser negativo.")
        except ValueError:
            messagebox.showerror("Erro de Validação", "Valor deve ser um número válido (ex: 100.00 ou 100,00).", parent=self.popup)
            return

        if not observacoes:
            observacoes = "N/D"

        self.tarefas_associadas.append([tarefa, qtd_int, val_float, observacoes])
        self.update_list()

        # Limpa campos
        self.entry_quantidade.delete(0, 'end')
        self.entry_tarefa.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        self.entry_observacoes.delete(0, 'end')
        self.entry_quantidade.focus_set()
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
                
                if hasattr(self.parent, 'populate_receitas_list'):
                    self.parent.populate_receitas_list()

            for item in self.tarefas_associadas:
                nome, qtd, val, obs = item
                tarefa_id = self.tarefas_map.get(nome)
                
                if tarefa_id:
                    add_tarefa_to_receita(self.receita_id, tarefa_id, qtd, val, obs)
                else:
                    print(f"Aviso: Tarefa '{nome}' não encontrada no banco. Ignorada.")
            
            self.gerar_pdf_recibo()

            messagebox.showinfo("Sucesso", f"Receita salva e PDF gerado (recibo_{self.receita_id}.pdf)!", parent=self.popup)
            self.popup.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}", parent=self.popup)

    def gerar_pdf_recibo(self):
        """Coleta os dados e chama o gerador de PDF."""
        recibos_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../receitas'))
        os.makedirs(recibos_dir, exist_ok=True)
        
        output_file = os.path.join(recibos_dir, f"recibo_{self.receita_id}.pdf")
        
        try:
            gerar_pdf_orcamento(self.receita_id, output_file)
            print(f"PDF gerado em: {output_file}")
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            messagebox.showwarning("Aviso PDF", f"Receita salva, mas erro ao gerar PDF: {e}", parent=self.popup)

    def update_list(self):
        """Atualiza a Treeview com as tarefas associadas."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for tarefa in self.tarefas_associadas:
            display_values = list(tarefa)
            if isinstance(display_values[2], (int, float)):
                display_values[2] = f"R$ {display_values[2]:.2f}".replace('.', ',')
            self.tree.insert("", "end", values=display_values)
    
    def remover(self):
        """Remove a tarefa selecionada da lista."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma tarefa para deletar.")
            return

        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja remover esta tarefa da lista?"):
            try:
                index = self.tree.index(selected_item[0])
                del self.tarefas_associadas[index]
                self.update_list()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível remover: {e}")

    def on_tarefa_keyrelease(self, event):
        """Filtra e mostra as sugestões conforme o usuário digita."""
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Return', 'Escape', 'Tab']:
            return

        typed_text = self.entry_tarefa.get()
        
        if not typed_text:
            filtered_list = self.todas_tarefas
        else:
            filtered_list = [tarefa for tarefa in self.todas_tarefas if typed_text.lower() in tarefa.lower()]
        
        self.lista_sugestoes.delete(0, tk.END)
        for item in filtered_list:
            self.lista_sugestoes.insert(tk.END, item)
            
        if filtered_list:
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
        """Move a seleção da lista para baixo."""
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
        """Move a seleção da lista para cima."""
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
        """Confirma a seleção atual da lista."""
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