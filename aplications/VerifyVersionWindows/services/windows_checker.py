import os

def eh_midia_windows(diretorio):
    caminho_sources = os.path.join(diretorio, 'sources')
    setup = os.path.join(caminho_sources, 'setup.exe')
    install = os.path.join(caminho_sources, 'install.wim')
    install_esd = os.path.join(caminho_sources, 'install.esd')
    
    return os.path.exists(setup) and (os.path.exists(install) or os.path.exists(install_esd))
