# Este arquivo contem as requisições das tarefas
import sqlite3
from .criar_bd import connect_db

# Criar tarefa
def add_tarefa(nome):
    """Adiciona uma nova tarefa."""
    conn = connect_db()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tarefas (nome)
                VALUES (?)
            ''', (nome,))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa: {e}")
        return None
    finally:
        conn.close()

# Buscar tarefa por ID
def get_tarefa(tarefa_id):
    """Busca uma tarefa pelo ID."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas WHERE id = ?', (tarefa_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar tarefa por ID: {e}")
        return None
    finally:
        conn.close()

# Listar tarefas
def get_all_tarefas():
    """Lista todas as tarefas em ordem alfabética."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas ORDER BY nome ASC')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar tarefas: {e}")
        return []
    finally:
        conn.close()

# Listar tarefas por sub-string
def get_tarefas_by_name(substring):
    """Busca tarefas que contêm a sub-string em ordem alfabética."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM tarefas 
                       WHERE nome LIKE ? 
                       ORDER BY nome ASC""", 
                       (f'%{substring}%',))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar tarefas por nome: {e}")
        return []
    finally:
        conn.close()

# Atualizar tarefa
def update_tarefa(tarefa_id, nome):
    """Atualiza uma tarefa existente."""
    conn = connect_db()
    try:
        with conn:
            conn.execute('''
                UPDATE tarefas
                SET nome = ?
                WHERE id = ?
            ''', (nome, tarefa_id))
    except sqlite3.Error as e:
        print(f"Erro ao atualizar tarefa: {e}")
    finally:
        conn.close()

# Deletar tarefa
def delete_tarefa(tarefa_id):
    """Deleta uma tarefa específica."""
    conn = connect_db()
    try:
        with conn:
            conn.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
    except sqlite3.Error as e:
        print(f"Erro ao deletar tarefa: {e}")
    finally:
        conn.close()
