from .services import criar_pasta_backup, copiar_arquivos, compactar_pasta, config

def AutoBKP():
    pasta_backup = criar_pasta_backup(config.DESTINO)
    if copiar_arquivos(config.ORIGEM, pasta_backup):
        if config.COMPRESSAO:
            compactar_pasta(pasta_backup)

if __name__ == '__main__':
    AutoBKP()
