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

def build_pdf_filename(receita):
    """Constrói o caminho completo do arquivo PDF para uma receita.

    O nome do arquivo segue o padrão Cliente_Placa_Data.pdf, com espaços
    substituídos por '_' e barras da data substituídas por '-'.
    """
    cliente = receita.cliente.strip().replace(" ", "_")
    placa = receita.placa.strip().replace(" ", "_")
    data = receita.data.strip().replace("/", "-")
    filename = f"{cliente}_{placa}_{data}.pdf"
    return os.path.join(get_receitas_dir(), filename)

def get_resource_path(relative_path):
    """
    Retorna o caminho absoluto para um recurso (arquivo), funcionando tanto
    em desenvolvimento quanto após compilado com PyInstaller (--add-data).
    """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Em desenvolvimento, usa a raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

    return os.path.join(base_path, relative_path)
