# Este arquivo contem as requisições das receitas
import sqlite3
from .criar_bd import connect_db

# Criar receita
def add_receita(cliente, oficina, motor_cabecote, placa, data):
    """Adiciona uma nova receita ao banco de dados."""
    conn = connect_db()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO receitas (cliente, oficina, motor_cabecote, placa, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente, oficina, motor_cabecote, placa, data))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao adicionar receita: {e}")
        return None
    finally:
        conn.close()

# Obter todas as receitas
def get_all_receitas():
    """Retorna todas as receitas do banco de dados."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar receitas: {e}")
        return []
    finally:
        conn.close()

# Obter receita por ID
def get_receita_by_id(receita_id):
    """Retorna uma receita específica pelo seu ID."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE id = ?', (receita_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao buscar receita por ID: {e}")
        return None
    finally:
        conn.close()

# Obter receita por oficina
def get_receita_by_oficina(oficina):
    """Retorna uma receita específica pela oficina."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        search_term = f'%{oficina}%'
        cursor.execute('SELECT * FROM receitas WHERE oficina LIKE ?', (search_term,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar receita por oficina: {e}")
        return []
    finally:
        conn.close()

# Obter receita por nome
def get_receita_by_cliente(cliente):
    """Retorna uma receita específica pelo nome do cliente."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        search_term = f'%{cliente}%'
        cursor.execute('SELECT * FROM receitas WHERE cliente LIKE ?', (search_term,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar receita por cliente: {e}")
        return []
    finally:
        conn.close()

# Obter receita por data
def get_receita_by_data(data):
    """Retorna uma receita específica pela data."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM receitas WHERE data = ?', (data,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao buscar receita por data: {e}")
        return []
    finally:
        conn.close()

# Atualizar receita
def update_receita(receita_id, cliente, oficina, motor_cabecote, placa, data):
    """Atualiza uma receita existente."""
    conn = connect_db()
    try:
        with conn:
            conn.execute('''
                UPDATE receitas
                SET cliente = ?, oficina = ?, motor_cabecote = ?, placa = ?, data = ?
                WHERE id = ?
            ''', (cliente, oficina, motor_cabecote, placa, data, receita_id))
    except sqlite3.Error as e:
        print(f"Erro ao atualizar receita: {e}")
    finally:
        conn.close()

# Deletar receita
def delete_receita(receita_id):
    """Deleta uma receita e todas as suas tarefas associadas."""
    conn = connect_db()
    try:
        with conn:
            conn.execute('DELETE FROM receitas WHERE id = ?', (receita_id,))
    except sqlite3.Error as e:
        print(f"Erro ao deletar receita: {e}")
    finally:
        conn.close()
