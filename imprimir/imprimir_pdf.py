import os
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional

def imprimir_arquivo(caminho_arquivo: str, impressora: Optional[str] = None):
    """
    Envia um arquivo PDF para a impressora configurada no sistema.
    
    No Linux, utiliza o comando 'lp' (CUPS).
    No Windows, utiliza 'os.startfile' com verbo 'print'.
    
    Args:
        caminho_arquivo (str): Caminho completo do arquivo PDF.
        impressora (str, optional): Nome da impressora (apenas Linux/macOS). Se None, usa a padrão.
    """
    if not os.path.exists(caminho_arquivo):
        messagebox.showerror("Erro", f"Arquivo não encontrado:\n{caminho_arquivo}")
        return

    sistema = platform.system()

    try:
        if sistema == "Linux" or sistema == "Darwin":
            # Monta o comando lp
            cmd = ["lp"]
            if impressora:
                cmd.extend(["-d", impressora])
            
            # Adiciona o arquivo
            cmd.append(caminho_arquivo)
            
            # Executa o comando
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Sucesso", "Arquivo enviado para a impressora.")
            
        elif sistema == "Windows":
            # No Windows, imprime na impressora padrão
            os.startfile(caminho_arquivo, "print")
            
        else:
            messagebox.showwarning("Sistema não suportado", f"Impressão não implementada para {sistema}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro de Impressão", f"Falha ao executar comando de impressão:\n{e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado ao imprimir:\n{e}")

def selecionar_e_imprimir():
    """
    Abre uma janela de seleção de arquivo e imprime o PDF selecionado.
    """
    arquivo = filedialog.askopenfilename(
        title="Selecione o PDF para Imprimir",
        filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os Arquivos", "*.*")]
    )
    
    if arquivo:
        imprimir_arquivo(arquivo)

if __name__ == "__main__":
    # Cria uma raiz Tk oculta se executado diretamente
    root = tk.Tk()
    root.withdraw()
    imprimir_arquivo("Roberio_POD3B41_01-01-2026.pdf")
    root.destroy()
