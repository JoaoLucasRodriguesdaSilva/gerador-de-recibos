from database.tarefas import *
from database.receita_tarefa import *
from database.receitas import update_receita, delete_receita
def test():
    import sqlite3
    from database.criar_bd import connect_db
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO receitas (cliente, oficina, motor_cabecote, placa, data) VALUES ("C", "O", "M", "P", "D")')
    rid = cursor.lastrowid
    tid = add_tarefa("Tarefa Unica")
    cursor.execute('INSERT INTO receita_tarefa (receita_id, tarefa_id, quantidade, valor, observacoes) VALUES (?, ?, 1, 100, "obs")', (rid, tid))
    conn.commit()
    conn.close()
    
    delete_tarefa(tid)
    print(f"Task is still there? {get_tarefa(tid)}")
test()
