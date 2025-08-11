import os
from datetime import datetime

# Adiciona o diretório raiz ao sys.path para permitir a importação dos módulos do banco de dados
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.criar_bd import criar_db, get_db_path
from database.receitas import (
    add_receita,
    get_receita_by_id,
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
    update_tarefa_from_receita,
    remove_tarefa_from_receita,
    get_valor_total_from_receita
)

def run_all_tests():
    """
    Executa um teste de fluxo completo para o banco de dados.
    """
    print("--- INICIANDO TESTE COMPLETO DO BANCO DE DADOS ---")
    
    try:
        # 1. Criar dados iniciais
        print("\n[PASSO 1] Criando dados iniciais...")
        current_date = datetime.now().strftime("%Y-%m-%d")
        receita_id = add_receita("Cliente Standalone", "Oficina Script", "Motor Teste", "RUN-2024", current_date)
        tarefa1_id = add_tarefa("Inspecao de Freios")
        tarefa2_id = add_tarefa("Balanceamento de Rodas")
        
        assert receita_id is not None
        assert tarefa1_id is not None
        assert tarefa2_id is not None
        print(f"-> SUCESSO: Receita ID: {receita_id}, Tarefa1 ID: {tarefa1_id}, Tarefa2 ID: {tarefa2_id}")

        # 2. Associar tarefas à receita
        print("\n[PASSO 2] Associando tarefas à receita...")
        add_tarefa_to_receita(receita_id, tarefa1_id, 1, 95.00, "Verificacao de pastilhas e discos")
        add_tarefa_to_receita(receita_id, tarefa2_id, 4, 25.00, "Balanceamento por roda")
        
        tarefas_associadas = get_tarefas_from_receita(receita_id)
        assert len(tarefas_associadas) == 2
        print(f"-> SUCESSO: 2 tarefas associadas. {tarefas_associadas}")

        # 3. Verificar o valor total
        print("\n[PASSO 3] Verificando o valor total...")
        total = get_valor_total_from_receita(receita_id)
        # 95.00 + (4 * 25.00) = 195.00 (Este cálculo depende da sua regra de negócio)
        # Assumindo que o valor na junção é o total para aquele item: 95.00 + 25.00 = 120.00
        # Vou usar a regra atual da sua função get_valor_total_from_receita
        total_esperado = 95.00 + 25.00
        assert total == total_esperado
        print(f"-> SUCESSO: Valor total calculado é {total:.2f}")

        # 4. Atualizar dados
        print("\n[PASSO 4] Atualizando dados...")
        update_receita(receita_id, "Cliente Standalone Atualizado", "Oficina Script", "Motor Teste V2", "RUN-2025", current_date)
        update_tarefa(tarefa1_id, "Inspecao Completa de Freios")
        
        receita_atualizada = get_receita_by_id(receita_id)
        assert receita_atualizada[1] == "Cliente Standalone Atualizado"
        print("-> SUCESSO: Dados da receita e tarefa atualizados.")

        # 5. Atualizar uma associação
        print("\n[PASSO 5] Atualizando uma associação de tarefa...")
        update_tarefa_from_receita(receita_id, tarefa1_id, 2, 100.00, "Verificacao de pastilhas e discos - ATUALIZADO")
        
        total_apos_update = get_valor_total_from_receita(receita_id)
        assert total_apos_update == 125.00  # 100.00 (tarefa 1 atualizada) + 25.00 (tarefa 2)
        print(f"-> SUCESSO: Associação atualizada. Novo total: {total_apos_update:.2f}")

        # 6. Remover uma associação
        print("\n[PASSO 6] Removendo uma associação de tarefa...")
        remove_tarefa_from_receita(receita_id, tarefa2_id)
        
        tarefas_restantes = get_tarefas_from_receita(receita_id)
        assert len(tarefas_restantes) == 1
        
        novo_total = get_valor_total_from_receita(receita_id)
        assert novo_total == 100.00
        print(f"-> SUCESSO: Associação removida. Novo total: {novo_total:.2f}")

        # 7. Deletar a receita (e verificar a cascata)
        print("\n[PASSO 7] Deletando a receita e verificando a cascata...")
        delete_receita(receita_id)
        
        receita_deletada = get_receita_by_id(receita_id)
        assert receita_deletada is None
        
        tarefas_apos_cascata = get_tarefas_from_receita(receita_id)
        assert len(tarefas_apos_cascata) == 0
        print("-> SUCESSO: Receita e suas associações foram deletadas.")

        # 8. Deletar tarefas órfãs
        print("\n[PASSO 8] Deletando tarefas órfãs...")
        delete_tarefa(tarefa1_id)
        delete_tarefa(tarefa2_id)
        print("-> SUCESSO: Tarefas órfãs deletadas.")

        print("\n--- TODOS OS TESTES PASSARAM COM SUCESSO! ---")

    except AssertionError as e:
        print(f"\n--- !!! TESTE FALHOU !!! ---")
        print(f"Erro de asserção: {e}")
    except Exception as e:
        print(f"\n--- !!! OCORREU UM ERRO INESPERADO DURANTE O TESTE !!! ---")
        print(f"Erro: {e}")


if __name__ == "__main__":
    # Setup: Garante um ambiente limpo para o teste
    db_path = get_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)
    criar_db()
    
    # Executa os testes
    run_all_tests()
    
    # Teardown: Limpa o banco de dados após o teste
    if os.path.exists(db_path):
        os.remove(db_path)
        print("\nBanco de dados de teste limpo.")