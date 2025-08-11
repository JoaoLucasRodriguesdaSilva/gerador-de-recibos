# Este arquivo contem as requisições das tarefas
from .criar_bd import connect_db

# Criar tarefa
def add_tarefa(nome):
    """Adiciona uma nova tarefa."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO tarefas (nome)
        VALUES (?)
    ''', (nome,))
    tarefa_id = cursor.lastrowid

    cursor.close()
    conn.commit()
    conn.close()
    return tarefa_id

# Atualizar tarefa
def update_tarefa(tarefa_id, nome):
    """Atualiza uma tarefa existente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE tarefas
        SET nome = ?
        WHERE id = ?
    ''', (nome, tarefa_id))

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
