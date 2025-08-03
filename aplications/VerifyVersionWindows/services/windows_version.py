import os
import subprocess
import re
import unicodedata

def remover_acentos(texto):
    # Normaliza texto para remover acentuação (se desejar)
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def limpar_acentos_estranhos(texto):
    # Corrige caracteres específicos comuns no output do DISM
    substituicoes = {
        'Æ': 'ã',
        '‡': 'ç',
        '¡': 'á',
        '¢': 'ó',
        'ˆ': 'ê',
        '¤': 'ü',
        '¬': 'í',
        # Acrescente outros se identificar mais
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    return texto

def obter_versao_windows(pendrive, index=1):
    caminho_sources = os.path.join(pendrive, "sources")
    install_wim = os.path.join(caminho_sources, "install.wim")
    if not os.path.exists(install_wim):
        install_wim = os.path.join(caminho_sources, "install.esd")
        if not os.path.exists(install_wim):
            return "Arquivo install.wim/esd não encontrado."

    comando = [
        "dism",
        "/Get-WimInfo",
        f"/WimFile:{install_wim}",
        f"/index:{index}"
    ]

    try:
        resultado = subprocess.run(comando, capture_output=True)
        saida = resultado.stdout.decode("mbcs", errors="replace")
        saida = limpar_acentos_estranhos(saida)
        return formatar_saida_dism(saida)
    except Exception as e:
        return f"Erro ao executar DISM: {e}"

def formatar_saida_dism(saida):
    linhas = saida.splitlines()

    # Mapeamento flexível: várias formas possíveis para a mesma chave
    chaves_map = {
        "Nome": ["Nome", "Name"],
        "Descrição": ["Descrição", "Descricao", "Description"],
        "Edição": ["Edição", "Edicao", "Edition"],
        "Versão": ["Versão", "Versao", "Version"],
        "Arquitetura": ["Arquitetura", "Architecture"],
        "Tipo de Produto": ["Tipo de Produto", "Product Type"],
        "Instalação": ["Instalação", "Instalacao", "Installation"],
        "Tamanho": ["Tamanho", "Size"],
        "Criado": ["Criado", "Created"],
        "Modificado": ["Modificado", "Modified"],
        "Idiomas": ["Idiomas", "Languages"],
    }

    info = {}
    idiomas = []
    capturando_idiomas = False

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        # Captura a seção Idiomas (se houver)
        if linha.startswith("Idiomas:") or linha.startswith("Languages:"):
            capturando_idiomas = True
            continue

        if capturando_idiomas:
            # Sai do modo idiomas se linha não tiver formato esperado
            if re.match(r'^[a-z]{2}-[A-Z]{2}', linha) or linha == "":
                idiomas.append(linha.strip("- \t"))
                continue
            else:
                capturando_idiomas = False

        # Procura pares chave : valor, ignorando acentuação e espaços
        if ":" in linha:
            partes = linha.split(":", 1)
            chave_raw = partes[0].strip()
            valor = partes[1].strip()

            chave_sem_acento = remover_acentos(chave_raw).lower()

            # Verifica em chaves_map
            for chave_std, variantes in chaves_map.items():
                for var in variantes:
                    var_sem_acento = remover_acentos(var).lower()
                    if chave_sem_acento == var_sem_acento:
                        info[chave_std] = valor
                        break

    # Monta saída formatada
    resultado_formatado = [
        "🪟 Informações da Mídia de Instalação:\n",
        f"Nome: {info.get('Nome', 'N/D')}",
        f"Descrição: {info.get('Descrição', 'N/D')}",
        f"Edição: {info.get('Edição', 'N/D')}",
        f"Versão: {info.get('Versão', 'N/D')}",
        f"Arquitetura: {info.get('Arquitetura', 'N/D')}",
        f"Tipo de Produto: {info.get('Tipo de Produto', 'N/D')}",
        f"Instalação: {info.get('Instalação', 'N/D')}",
        f"Tamanho: {info.get('Tamanho', 'N/D')}",
        f"Criado em: {info.get('Criado', 'N/D')}",
        f"Modificado em: {info.get('Modificado', 'N/D')}",
    ]

    if idiomas:
        resultado_formatado.append(f"Idiomas: {', '.join(idiomas)}")

    resultado_formatado.append("\n✅ A operação foi concluída com êxito.")
    return "\n".join(resultado_formatado)
