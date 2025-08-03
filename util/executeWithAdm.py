import ctypes
import sys

def executar_como_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True  # já está com privilégio admin
    else:
        # Reexecuta o script como administrador
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
        except Exception as e:
            print(f"Erro ao solicitar permissão de administrador: {e}")
        sys.exit()