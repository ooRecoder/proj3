import json
import psutil
import os


def carregar_blacklist(pasta: str, nome_arquivo: str) -> list:
    # Caminho absoluto para a raiz do projeto
    raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    caminho_absoluto = os.path.join(raiz_projeto, pasta, nome_arquivo)
    with open(caminho_absoluto, 'r') as f:
        return [p.lower() for p in json.load(f)]


def analisar_processos(pasta: str, nome_arquivo: str,
                       limite_cpu: float = 20.0,
                       limite_mem_mb: float = 150.0) -> dict:
    processos_suspeitos = []
    processos_pesados = []

    blacklist = carregar_blacklist(pasta, nome_arquivo)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            nome = proc.info['name'].lower()
            pid = proc.info['pid']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_info'].rss / (1024 * 1024)  # Convertendo para MB

            if nome in blacklist:
                processos_suspeitos.append({
                    'pid': pid,
                    'nome': nome,
                    'cpu': cpu,
                    'mem': mem
                })

            if cpu > limite_cpu or mem > limite_mem_mb:
                processos_pesados.append({
                    'pid': pid,
                    'nome': nome,
                    'cpu': cpu,
                    'mem': mem
                })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        'suspeitos': processos_suspeitos,
        'pesados': processos_pesados
    }
