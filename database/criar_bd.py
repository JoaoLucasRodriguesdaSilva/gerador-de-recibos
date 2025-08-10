#Este arquivo inicializa o banco de dados
import sqlite3
import os

def get_db_path():
    """Retorna o caminho para o arquivo do banco de dados."""
    # Garante que o diretório do banco de dados exista
    db_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'receitas.db')

def connect_db():
    """Cria e conecta ao banco de dados SQLite."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # Ativa o suporte a chaves estrangeiras
    return conn

def create_table():
    """Cria a tabela de recibos se ela não existir."""
    conn = connect_db()
    cursor = conn.cursor()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quantidade INTEGER NOT NULL,
            nome TEXT NOT NULL,
            observacoes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receita_tarefa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            receita_id INTEGER NOT NULL,
            tarefa_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (receita_id) REFERENCES receitas(id) ON DELETE CASCADE,
            FOREIGN KEY (tarefa_id) REFERENCES tarefas(id) ON DELETE CASCADE
        )
    ''')

    cursor.close()
    conn.commit()
    conn.close()

def criar_db():
    create_table()
    print(f"Banco de dados '{get_db_path()}' e tabela 'receitas' verificados/criados com sucesso.")