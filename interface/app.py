import tkinter as tk
from tkinter import ttk
from Receitas.receitas import ReceitasFrame

# --- Main Application Window ---
root = tk.Tk()
root.title("Gerenciador de Receitas")
root.geometry("1024x600") # Set a default size

# --- Frame Principal ---
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# --- Seção Receitas ---
receitas_frame = ReceitasFrame(main_frame)
receitas_frame.pack(fill="both", expand=True)

# --- Seção Tarefas ---


# --- Seção Tarefas de uma Receita ---


# --- Start the application ---
root.mainloop()