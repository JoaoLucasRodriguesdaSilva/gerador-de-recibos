#Este arquivo inicializa o banco de dados e popula com tarefas padrão
import sqlite3
import os
import sys

TAREFAS_PADRAO = [
    "Mão de Obra",
    "Comando de Válvulas",
    "Recup. e Retíf. de Cabeçote",
    "Soldar Cabeçote",
    "Guias de Válvulas",
    "Plainar",
    "Esmerilhar Cabeçote",
    "Trocar Retentores",
    "Limpeza Química",
    "Selo d'Água do Cabeçote",
    "Teste de Trinca",
    "Calibragem",
    "Recuperação",
    "Retent. Comand. Válvulas",
    "Venda de Comando de Valv.",
    "Extração",
    "Bucha 14",
    "Helicoide de 08",
    "Válv. Escape",
    "Válv. Admissão",
    "Trocar Sedes de Valvulas",
    "Sede sob. Medida",
    "Encamisar Bloco",
    "Brunir Camisas Bloco",
    "Venda de Virabrequim",
    "Ret. Bloco",
    "Ret. Virabrequim",
    "Retificar Ferro de Bielas",
    "Plainar Bloco",
    "Teste Planicidade do Bloco",
    "Brz. Chumaceira",
    "Brz. de Bielas",
    "Bucha do Comando Interm.",
    "Montar Pistão",
    "Descarbonização",
    "Jogo de pistão",
    "Recuperação no bloco"
]

def get_db_path():
    """Retorna o caminho para o arquivo do banco de dados."""
    
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável (PyInstaller)
        # Pega o caminho da pasta AppData/Roaming do Windows
        appdata_dir = os.environ.get('APPDATA')
        
        # Caso o APPDATA não seja encontrado (muito raro), usa a pasta do usuário (C:\Users\NomeDoUsuario)
        if not appdata_dir:
            appdata_dir = os.path.expanduser('~')
            
        # Cria uma pasta específica para o seu programa dentro do AppData
        # Você pode mudar 'GeradorDeRecibos' para o nome exato do seu programa
        db_dir = os.path.join(appdata_dir, 'GeradorDeRecibos', 'dados')
    else:
        # Se estiver rodando como script (em desenvolvimento)
        # Salva dentro da própria pasta 'database'
        db_dir = os.path.dirname(os.path.abspath(__file__))
        
    # Cria os diretórios caso eles não existam
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'receitas.db')

def connect_db():
    """Cria e conecta ao banco de dados SQLite."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Ativa o suporte a chaves estrangeiras
    return conn

def create_table():
    """Cria as tabelas e insere dados iniciais se necessário."""
    conn = connect_db()
    
    try:
        with conn:
            cursor = conn.cursor()

            # Tabela de Recibos (Cabeçalho do Orçamento)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receitas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente TEXT NOT NULL,
                    oficina TEXT NOT NULL,
                    motor_cabecote TEXT NOT NULL,
                    placa TEXT NOT NULL,
                    data TEXT NOT NULL
                )
            ''')

            # Tabela de Tarefas (Catálogo de serviços disponíveis)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')

            # Tabela de Ligação (Itens do Orçamento: qual receita tem qual tarefa)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS receita_tarefa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receita_id INTEGER NOT NULL,
                    tarefa_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    valor REAL NOT NULL,
                    observacoes TEXT NOT NULL,
                    FOREIGN KEY (receita_id) REFERENCES receitas(id) ON DELETE CASCADE,
                    FOREIGN KEY (tarefa_id) REFERENCES tarefas(id)
                )
            ''')

            # Verifica se já existem tarefas cadastradas
            cursor.execute('SELECT count(*) FROM tarefas')
            count = cursor.fetchone()[0]

            if count == 0:
                print("Populando tabela 'tarefas' com itens padrão do recibo...")
                dados_tarefas = [(tarefa,) for tarefa in TAREFAS_PADRAO]
                cursor.executemany('INSERT OR IGNORE INTO tarefas (nome) VALUES (?)', dados_tarefas)
            else:
                print(f"Tabela 'tarefas' já contém {count} itens. Nenhuma inserção realizada.")
                
    except sqlite3.Error as e:
        print(f"Erro ao manipular banco de dados: {e}")
    finally:
        conn.close()

def criar_db():
    create_table()
    print(f"Banco de dados '{get_db_path()}' verificado com sucesso.")