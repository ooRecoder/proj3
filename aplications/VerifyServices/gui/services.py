import subprocess
from tkinter import messagebox

from ..core.service_checker import verificar_servicos_criticos

def carregar_servicos():
    return verificar_servicos_criticos('config', 'cs.json')

def reiniciar_servico(nome_servico, callback_recarregar):
    try:
        # Verifica o status do serviço
        resultado_query = subprocess.run(
            ["sc", "query", nome_servico],
            capture_output=True, text=True, check=True
        )
        status_linhas = resultado_query.stdout.splitlines()
        status = ""
        for linha in status_linhas:
            if "STATE" in linha:
                status = linha.strip()
                break

        if "RUNNING" in status:
            print(f"Serviço '{nome_servico}' está em execução. Parando...")
            subprocess.run(["sc", "stop", nome_servico], check=True, capture_output=True, text=True)
        else:
            print(f"Serviço '{nome_servico}' já está parado.")

        print(f"Iniciando serviço: {nome_servico}")
        subprocess.run(["sc", "start", nome_servico], check=True, capture_output=True, text=True)

        messagebox.showinfo("Serviço reiniciado", f"Serviço '{nome_servico}' reiniciado com sucesso.")
        callback_recarregar()

    except subprocess.CalledProcessError as e:
        print("Erro ao reiniciar o serviço:")
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        messagebox.showerror("Erro ao reiniciar", f"Não foi possível reiniciar '{nome_servico}'.\n\n{e.stderr}")

def parar_servico(nome_servico, callback_recarregar):
    try:
        # Tenta parar o serviço diretamente
        resultado = subprocess.run(
            ["sc", "stop", nome_servico],
            check=True, capture_output=True, text=True
        )
        print("Stop output:", resultado.stdout)
        messagebox.showinfo("Serviço parado", f"Serviço '{nome_servico}' parado com sucesso.")
        callback_recarregar()
    except subprocess.CalledProcessError as e:
        # Se o erro for 1062 (serviço já parado), tratar separadamente
        if "1062" in e.stderr:
            messagebox.showinfo("Serviço já parado", f"Serviço '{nome_servico}' já está parado.")
            callback_recarregar()
        else:
            print("Erro ao parar o serviço:")
            print("stdout:", e.stdout)
            print("stderr:", e.stderr)
            messagebox.showerror("Erro ao parar", f"Não foi possível parar '{nome_servico}'.\n\n{e.stderr}")
