import os
import zipfile
import shutil
from .logger import log_message

def compactar_pasta(pasta_origem):
    zip_nome = pasta_origem + '.zip'
    with zipfile.ZipFile(zip_nome, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, dirs, arquivos in os.walk(pasta_origem):
            for arquivo in arquivos:
                caminho_arquivo = os.path.join(raiz, arquivo)
                arcname = os.path.relpath(caminho_arquivo, pasta_origem)
                zipf.write(caminho_arquivo, arcname)
    log_message(f"Pasta compactada em {zip_nome}")
    shutil.rmtree(pasta_origem)
