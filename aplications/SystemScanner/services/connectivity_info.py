import subprocess
import platform
import requests

def test_ping(host="8.8.8.8", count=1, timeout=2):
    param_count = "-n" if platform.system().lower() == "windows" else "-c"
    param_timeout = "-w" if platform.system().lower() == "windows" else "-W"
    
    try:
        result = subprocess.run(
            ["ping", param_count, str(count), param_timeout, str(timeout), host],
            capture_output=True, text=True
        )
        success = result.returncode == 0
        output = result.stdout.splitlines()
        if success:
            summary = next((line for line in output if "tempo" in line or "time" in line), "Ping bem-sucedido")
        else:
            summary = "Falha no ping"
        return {"Ping para 8.8.8.8": summary}
    except Exception as e:
        return {"Ping para 8.8.8.8": f"Erro: {str(e)}"}

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        if response.status_code == 200:
            return {"IP Público": response.text.strip()}
        else:
            return {"IP Público": "Falha ao obter"}
    except Exception:
        return {"IP Público": "Offline ou sem acesso"}

def get_connectivity_info():
    info = {}
    info.update(test_ping())
    info.update(get_public_ip())
    return info
