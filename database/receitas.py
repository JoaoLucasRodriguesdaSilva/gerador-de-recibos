# Este arquivo contem as requisições das receitas
from .criar_bd import connect_db

# Criar receita
def add_receita(cliente, oficina, motor_cabecote, placa):
    """Adiciona uma nova receita ao banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO receitas (cliente, oficina, motor_cabecote, placa)
        VALUES (?, ?, ?, ?)
    ''', (cliente, oficina, motor_cabecote, placa))
    receita_id = cursor.lastrowid

    cursor.close()
    conn.commit()
    conn.close()
    return receita_id

# Obter todas as receitas
def get_all_receitas():
    """Retorna todas as receitas do banco de dados."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM receitas')
    receitas = cursor.fetchall()

    cursor.close()
    conn.close()
    return receitas

# Obter receita por ID
def get_receita_by_id(receita_id):
    """Retorna uma receita específica pelo seu ID."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM receitas WHERE id = ?', (receita_id,))
    receita = cursor.fetchone()

    cursor.close()
    conn.close()
    return receita

# Obter receita por oficina
def get_receita_by_oficina(oficina):
    """Retorna uma receita específica pela oficina."""
    conn = connect_db()
    cursor = conn.cursor()

    search_term = f'%{oficina}%'
    cursor.execute('SELECT * FROM receitas WHERE oficina LIKE ?', (search_term,))
    receita = cursor.fetchall()

    cursor.close()
    conn.close()
    return receita

# Obter receita por nome
def get_receita_by_cliente(cliente):
    """Retorna uma receita específica pelo nome do cliente."""
    conn = connect_db()
    cursor = conn.cursor()

    search_term = f'%{cliente}%'
    cursor.execute('SELECT * FROM receitas WHERE cliente LIKE ?', (search_term,))
    receita = cursor.fetchall()

    cursor.close()
    conn.close()
    return receita

# Atualizar receita
def update_receita(receita_id, cliente, oficina, motor_cabecote, placa):
    """Atualiza uma receita existente."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE receitas
        SET cliente = ?, oficina = ?, motor_cabecote = ?, placa = ?
        WHERE id = ?
    ''', (cliente, oficina, motor_cabecote, placa, receita_id))

    cursor.close()
    conn.commit()
    conn.close()

# Deletar receita
def delete_receita(receita_id):
    """Deleta uma receita e todas as suas tarefas associadas."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM receitas WHERE id = ?', (receita_id,))

    cursor.close()
    conn.commit()
    conn.close()
