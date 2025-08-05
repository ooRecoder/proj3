import os

def get_absolute_path(relative_path):
    """
    Converte um caminho relativo em caminho absoluto, 
    baseado no diretório do arquivo atual.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.normpath(os.path.join(base_path, relative_path))
    return absolute_path