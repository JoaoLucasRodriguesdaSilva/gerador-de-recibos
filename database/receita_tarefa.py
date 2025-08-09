# Este arquivo é responsavel pelas requisições da relação receita <=> tarefa
from .criar_bd import connect_db

def add_tarefa_to_receita(receita_id, tarefa_id, valor):
    """Associa uma tarefa a uma receita na tabela de junção."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO receita_tarefa (receita_id, tarefa_id, valor) VALUES (?, ?, ?)",
        (receita_id, tarefa_id, valor)
    )

    cursor.close()
    conn.commit()
    conn.close()

def get_tarefas_from_receita(receita_id):
    """Retorna todas as tarefas associadas a uma receita específica."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t.* FROM tarefas t
        JOIN receita_tarefa rt ON t.id = rt.tarefa_id
        WHERE rt.receita_id = ?
    """, (receita_id,))
    tarefas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return tarefas

def remove_tarefa_from_receita(receita_id, tarefa_id):
    """Remove a associação entre uma tarefa e uma receita."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM receita_tarefa WHERE receita_id = ? AND tarefa_id = ?",
        (receita_id, tarefa_id)
    )

    cursor.close()
    conn.commit()
    conn.close()

def get_valor_total_from_receita(receita_id):
    """Calcula o valor total somando o valor de todas as tarefas de uma receita."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(valor) FROM receita_tarefa
        WHERE receita_id = ?
    """, (receita_id,))
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return total if total is not None else 0
