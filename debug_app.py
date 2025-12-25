import sys
import os
import traceback

try:
    print("Iniciando debug...")
    # Adiciona interface ao path para simular estar na pasta interface, ou ajusta imports
    sys.path.append(os.path.abspath('interface'))
    
    print("Importando app...")
    import interface.app
    print("App importado com sucesso.")
except Exception:
    traceback.print_exc()
