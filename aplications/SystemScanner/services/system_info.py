import platform
import os
import time
import locale
import getpass
import psutil
from datetime import datetime
import subprocess

def check_windows_activation():
    try:
        cmd = [
            "powershell",
            "-Command",
            "(Get-CimInstance -Class SoftwareLicensingProduct | Where-Object {$_.PartialProductKey} | Select-Object -ExpandProperty LicenseStatus)"
        ]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        status = output.decode().strip()
        if status == "1":
            return "Sim"
        else:
            return "Não"
    except Exception:
        return "Desconhecido"

def get_system_info():
    info = {}

    info["Sistema Operacional"] = platform.system()
    info["Versão Detalhada"] = platform.version()
    info["Arquitetura"] = platform.machine()
    info["Nome do Host"] = platform.node()
    info["Usuário Atual"] = getpass.getuser()
    info["Diretório do Sistema"] = os.environ.get("SystemRoot", "Desconhecido")
    info["Idioma do Sistema"] = locale.getdefaultlocale()[0] or "Desconhecido"

    boot_time = time.time() - psutil.boot_time()
    horas = int(boot_time // 3600)
    minutos = int((boot_time % 3600) // 60)
    info["Uptime (desde boot)"] = f"{horas}h {minutos}min"

    info["Data/Hora Atual"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # info["Windows Ativado"] = check_windows_activation()

    return info