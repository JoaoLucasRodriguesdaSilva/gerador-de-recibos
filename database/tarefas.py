# Este arquivo contem as requisições das tarefas
from .criar_bd import connect_db

# Criar tarefa
def add_tarefa(quantidade, nome, observacoes):
    """Adiciona uma nova tarefa."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tarefas (quantidade, nome, observacoes)
        VALUES (?, ?, ?)
    ''', (quantidade, nome, observacoes))
    tarefa_id = cursor.lastrowid

    cursor.close()
    conn.commit()
    conn.close()
    return tarefa_id

# Atualizar tarefa
def update_tarefa(tarefa_id, quantidade, nome, observacoes):
    """Atualiza uma tarefa existente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tarefas
        SET quantidade = ?, nome = ?, observacoes = ?
        WHERE id = ?
    ''', (quantidade, nome, observacoes, tarefa_id))

    cursor.close()
    conn.commit()
    conn.close()

# Deletar tarefa
def delete_tarefa(tarefa_id):
    """Deleta uma tarefa específica."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))

    cursor.close()
    conn.commit()
    conn.close()
