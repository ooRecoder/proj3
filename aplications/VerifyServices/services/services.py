import subprocess
from ..utils.messages import sucesso, erro, alerta

def listar_servicos(tree):
    tree.delete(*tree.get_children())
    resultado = subprocess.run(["sc", "query", "type=", "service", "state=", "all"],
                               capture_output=True, text=True, shell=True)
    linhas = resultado.stdout.splitlines()
    nome = status = ""
    for linha in linhas:
        if "SERVICE_NAME:" in linha:
            nome = linha.split(":")[1].strip()
        elif "STATE" in linha:
            status = linha.split(":")[1].split()[1].strip()
            tree.insert('', 'end', values=(nome, status))

def controlar_servico(tree, acao):
    item = tree.focus()
    if not item:
        alerta("Selecione um serviço.")
        return
    nome = tree.item(item)['values'][0]
    try:
        subprocess.run(["net", acao, nome], capture_output=True, text=True, shell=True)
        sucesso(f"Serviço {nome} {acao}ado com sucesso.")
        listar_servicos(tree)
    except Exception as e:
        erro(f"Erro ao {acao} serviço: {e}")
