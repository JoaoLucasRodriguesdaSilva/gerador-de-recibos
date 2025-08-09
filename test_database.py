# Arquivo para testar requisições
import sys
import os

# Adiciona o diretório raiz do projeto ao path para permitir importações de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), )))

from database.criar_bd import criar_db
from database.receitas import (
    add_receita,
    get_all_receitas,
    get_receita_by_id,
    get_receita_by_cliente,
    get_receita_by_oficina,
    update_receita,
    delete_receita
)
from database.tarefas import (
    add_tarefa,
    update_tarefa,
    delete_tarefa
)
from database.receita_tarefa import (
    add_tarefa_to_receita,
    get_tarefas_from_receita,
    remove_tarefa_from_receita,
    get_valor_total_from_receita
)

def test_database_workflow():
    """Executa um conjunto de testes para as funções de requisição ao banco de dados."""
    print("--- Iniciando testes ---")
    
    # 1. Garante que o banco de dados e as tabelas existam
    print("\n1. Verificando/Criando banco de dados e tabelas...")
    criar_db()

    # --- Testes de Criação ---
    print("\n--- Testando Criação de Dados ---")

    # 2. Adicionar uma receita e duas tarefas
    print("\n2. Adicionando dados iniciais...")
    receita_id = add_receita("Carlos Pereira", "Mecânica Rápida", "Motor Ford Zetec", "XYZ-7890")
    tarefa1_id = add_tarefa(1, "Retífica de Cabeçote", "Plainar e assentar válvulas")
    tarefa2_id = add_tarefa(4, "Troca de Velas", "Velas de Iridium")
    print(f"Receita adicionada com ID: {receita_id}")
    print(f"Tarefa 1 adicionada com ID: {tarefa1_id}")
    print(f"Tarefa 2 adicionada com ID: {tarefa2_id}")

    # 3. Associar tarefas à receita com valores específicos
    print(f"\n3. Associando tarefas à receita {receita_id}...")
    add_tarefa_to_receita(receita_id, tarefa1_id, 850.00)
    add_tarefa_to_receita(receita_id, tarefa2_id, 120.50)
    print("Associação concluída.")

    # --- Testes de Leitura ---
    print("\n--- Testando Leitura de Dados ---")

    # 4. Obter tarefas de uma receita
    print(f"\n4. Buscando tarefas da receita {receita_id}...")
    tarefas_da_receita = get_tarefas_from_receita(receita_id)
    print(f"Tarefas encontradas: {tarefas_da_receita}")
    assert len(tarefas_da_receita) == 2

    # 5. Calcular valor total da receita
    print(f"\n5. Calculando valor total da receita {receita_id}...")
    valor_total = get_valor_total_from_receita(receita_id)
    print(f"Valor total calculado: R$ {valor_total:.2f}")
    assert valor_total == 970.50

    # 6. Testar buscas por substring
    print("\n6. Testando buscas por substring...")
    cliente_encontrado = get_receita_by_cliente("Pereira")
    oficina_encontrada = get_receita_by_oficina("Rápida")
    print(f"Busca por 'Pereira' encontrou: {cliente_encontrado}")
    print(f"Busca por 'Rápida' encontrou: {oficina_encontrada}")
    assert len(cliente_encontrado) == 1
    assert len(oficina_encontrada) == 1

    # --- Testes de Atualização ---
    print("\n--- Testando Atualização de Dados ---")

    # 7. Atualizar uma tarefa
    print(f"\n7. Atualizando tarefa {tarefa1_id}...")
    update_tarefa(tarefa1_id, 1, "Retífica de Cabeçote Completa", "Inclui troca de retentores")
    tarefas_atualizadas = get_tarefas_from_receita(receita_id)
    print(f"Tarefas após atualização: {tarefas_atualizadas}")

    # --- Testes de Remoção e Deleção ---
    print("\n--- Testando Remoção e Deleção ---")

    # 8. Remover uma tarefa da receita
    print(f"\n8. Removendo tarefa {tarefa2_id} da receita {receita_id}...")
    remove_tarefa_from_receita(receita_id, tarefa2_id)
    tarefas_restantes = get_tarefas_from_receita(receita_id)
    print(f"Tarefas restantes na receita: {tarefas_restantes}")
    assert len(tarefas_restantes) == 1

    # 9. Recalcular valor total
    print("\n9. Recalculando valor total...")
    novo_valor_total = get_valor_total_from_receita(receita_id)
    print(f"Novo valor total: R$ {novo_valor_total:.2f}")
    assert novo_valor_total == 850.00

    # 10. Deletar a receita (deve deletar as associações em cascata)
    print(f"\n10. Deletando a receita {receita_id}...")
    delete_receita(receita_id)
    receita_deletada = get_receita_by_id(receita_id)
    tarefas_apos_delete_receita = get_tarefas_from_receita(receita_id)
    print(f"Busca pela receita deletada (esperado: None): {receita_deletada}")
    print(f"Associações da receita deletada (esperado: []): {tarefas_apos_delete_receita}")
    assert receita_deletada is None
    assert len(tarefas_apos_delete_receita) == 0

    # 11. Deletar as tarefas órfãs
    print(f"\n11. Deletando tarefas órfãs {tarefa1_id} e {tarefa2_id}...")
    delete_tarefa(tarefa1_id)
    delete_tarefa(tarefa2_id)
    print("Tarefas de teste deletadas.")

    print("\n--- Testes concluídos com sucesso! ---")

if __name__ == '__main__':
    test_database_workflow()
