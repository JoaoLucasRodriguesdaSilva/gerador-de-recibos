import os
import sys

def get_base_path():
    """
    Retorna o caminho base da aplicação.
    Se estiver rodando como executável (PyInstaller), retorna o diretório do executável.
    Se estiver rodando como script, retorna o diretório raiz do projeto.
    """
    if getattr(sys, 'frozen', False):
        # Se for executável
        return os.path.dirname(sys.executable)
    else:
        # Se for script, assume que este arquivo está em interface/utils/
        # Retorna a raiz do projeto (../../)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def get_receitas_dir():
    """Retorna o caminho absoluto para a pasta de receitas."""
    base_path = get_base_path()
    return os.path.join(base_path, 'receitas')
