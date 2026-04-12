# Este arquivo é responsavel pelas requisições da relação receita <=> tarefa
import sqlite3
from .criar_bd import connect_db
from .models import TarefaReceita

# Associa um tarefa a uma receita
def add_tarefa_to_receita(receita_id, tarefa_id, quantidade, valor, observacoes):
    """Associa uma tarefa a uma receita na tabela de junção."""
    conn = connect_db()
    try:
        with conn:
            conn.execute(
                "INSERT INTO receita_tarefa (receita_id, tarefa_id, quantidade, valor, observacoes) VALUES (?, ?, ?, ?, ?)",
                (receita_id, tarefa_id, quantidade, valor, observacoes)
            )
    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa à receita: {e}")
    finally:
        conn.close()

# Retorna as tarefas associadas a uma receita
def get_tarefas_from_receita(receita_id):
    """Retorna todas as tarefas associadas a uma receita específica com detalhes."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.nome, rt.quantidade, rt.valor, rt.observacoes 
            FROM tarefas t
            JOIN receita_tarefa rt ON t.id = rt.tarefa_id
            WHERE rt.receita_id = ?
        """, (receita_id,))
        return [TarefaReceita(*row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erro ao buscar tarefas da receita: {e}")
        return []
    finally:
        conn.close()

# Atualiza uma tarefa associada a uma receita
def update_tarefa_from_receita(receita_id, tarefa_id, quantidade, valor, observacoes):
    """Atualiza uma tarefa associada a uma receita."""
    conn = connect_db()
    try:
        with conn:
            conn.execute("""
                UPDATE receita_tarefa
                SET quantidade = ?, valor = ?, observacoes = ?
                WHERE receita_id = ? AND tarefa_id = ?
            """, (quantidade, valor, observacoes, receita_id, tarefa_id))
    except sqlite3.Error as e:
        print(f"Erro ao atualizar tarefa da receita: {e}")
    finally:
        conn.close()

# Desassocia uma tarefa de uma receita
def remove_tarefa_from_receita(receita_id, tarefa_id):
    """Remove a associação entre uma tarefa e uma receita."""
    conn = connect_db()
    try:
        with conn:
            conn.execute(
                "DELETE FROM receita_tarefa WHERE receita_id = ? AND tarefa_id = ?",
                (receita_id, tarefa_id)
            )
    except sqlite3.Error as e:
        print(f"Erro ao remover tarefa da receita: {e}")
    finally:
        conn.close()

# Retorna o valor total de uma receita
def get_valor_total_from_receita(receita_id):
    """Calcula o valor total somando o valor de todas as tarefas de uma receita."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(valor) FROM receita_tarefa
            WHERE receita_id = ?
        """, (receita_id,))
        total = cursor.fetchone()[0]
        return total if total is not None else 0
    except sqlite3.Error as e:
        print(f"Erro ao calcular valor total: {e}")
        return 0
    finally:
        conn.close()
