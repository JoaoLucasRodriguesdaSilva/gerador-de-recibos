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

# Buscar tarefa por ID
def get_tarefa(tarefa_id):
    """Busca uma tarefa pelo ID."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tarefas WHERE id = ?', (tarefa_id,))
    tarefa = cursor.fetchone()

    cursor.close()
    conn.close()

    return tarefa

# Listar tarefas
def get_all_tarefas():
    """Lista todas as tarefas em ordem alfabética."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tarefas ORDER BY nome ASC')
    tarefas = cursor.fetchall()

    cursor.close()
    conn.close()

    return tarefas

# Listar tarefas por sub-string
def get_tarefas_by_name(substring):
    """Busca tarefas que contêm a sub-string em ordem alfabética."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM tarefas 
                   WHERE nome LIKE ? 
                   ORDER BY nome ASC""", 
                   (f'%{substring}%',))
    tarefas = cursor.fetchall()

    cursor.close()
    conn.close()

    return tarefas

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
