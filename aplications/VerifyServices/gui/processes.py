from ..core.process_analizer import analisar_processos

def carregar_processos():
    return analisar_processos('config', 'sp.json')
