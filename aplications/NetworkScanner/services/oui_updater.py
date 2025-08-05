import os
import requests
from datetime import datetime, timedelta
from ..getAbsolutPath import get_absolute_path

OUI_URL = 'https://standards-oui.ieee.org/oui/oui.txt'
OUI_PATH = get_absolute_path('./resources/oui.txt')
MAX_DAYS = 7  # Atualizar se o arquivo tiver mais de X dias

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}


def download_oui():
    print("[+] Baixando a base OUI mais recente da IEEE...")
    response = requests.get(OUI_URL, headers=HEADERS)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(OUI_PATH), exist_ok=True)
        with open(OUI_PATH, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"[+] OUI database salvo em {OUI_PATH}")
    else:
        print(f"[ERRO] Falha ao baixar OUI. Código: {response.status_code}")


def check_and_update_oui():
    """
    Verifica se o arquivo OUI existe e se precisa ser atualizado.
    """
    if not os.path.exists(OUI_PATH):
        print("[INFO] OUI database não encontrado. Baixando agora...")
        download_oui()
        return

    # Verifica a data de modificação do arquivo
    file_mtime = datetime.fromtimestamp(os.path.getmtime(OUI_PATH))
    if datetime.now() - file_mtime > timedelta(days=MAX_DAYS):
        print("[INFO] OUI database está desatualizado. Baixando nova versão...")
        download_oui()
    else:
        print("[OK] OUI database está atualizado.")


if __name__ == "__main__":
    check_and_update_oui()
