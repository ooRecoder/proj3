import json
import psutil
import os

def carregar_servicos_criticos(pasta: str, nome_arquivo: str) -> dict:
    raiz_projeto = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    caminho_absoluto = os.path.join(raiz_projeto, pasta, nome_arquivo)
    with open(caminho_absoluto, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    # Opcional: normalizar para lowercase os nomes dos serviços em cada categoria
    categorias_normalizadas = {}
    for categoria, servicos in dados.items():
        categorias_normalizadas[categoria] = [s.lower() for s in servicos]
    return categorias_normalizadas


def obter_status_servico(servico_nome: str) -> str:
    try:
        servico = psutil.win_service_get(servico_nome)
        info = servico.as_dict()
        return info['status'].upper()  # Ex: 'RUNNING', 'STOPPED'
    except Exception:
        return "NÃO ENCONTRADO"

def verificar_servicos_criticos(pasta: str, nome_arquivo: str) -> dict:
    categorias = carregar_servicos_criticos(pasta, nome_arquivo)
    resultado = {}

    for categoria, servicos in categorias.items():
        resultado[categoria] = {}
        for servico in servicos:
            status = obter_status_servico(servico)
            resultado[categoria][servico] = status

    return resultado
