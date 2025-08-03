import psutil
from ..utils.messages import alerta, sucesso, erro

def listar_processos(tree):
    tree.delete(*tree.get_children())
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            tree.insert('', 'end', values=(proc.info['pid'], proc.info['name'], proc.info['username']))
        except:
            continue

def finalizar_processo(tree):
    item = tree.focus()
    if not item:
        alerta("Selecione um processo.")
        return
    pid = tree.item(item)['values'][0]
    try:
        psutil.Process(pid).terminate()
        sucesso(f"Processo {pid} finalizado.")
        listar_processos(tree)
    except Exception as e:
        erro(f"Erro ao finalizar: {e}")
