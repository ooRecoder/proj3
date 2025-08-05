import os

# Configurações do Backup
ORIGEM = r'C:\MeusDocumentos'
DESTINO = r'D:\Backups'
COMPRESSAO = True

# Log
LOG_FILE = os.path.join(DESTINO, 'backup_log.txt')
