import os
import shutil
from datetime import datetime
from .logger import log_message

def criar_pasta_backup(destino_base):
    agora = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    pasta_backup = os.path.join(destino_base, f'Backup_{agora}')
    os.makedirs(pasta_backup, exist_ok=True)
    return pasta_backup

def copiar_arquivos(origem, destino):
    try:
        shutil.copytree(origem, destino)
        log_message(f"Backup realizado com sucesso em {destino}")
        return True
    except Exception as e:
        log_message(f"Erro ao fazer backup: {e}")
        return False
