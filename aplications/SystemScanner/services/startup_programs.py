import winreg
import os

def get_startup_programs():
    entries = {}

    def read_run_key(root, path, origem):
        try:
            with winreg.OpenKey(root, path) as key:
                for i in range(winreg.QueryInfoKey(key)[1]):
                    name, value, _ = winreg.EnumValue(key, i)
                    entries[name] = f"{value} [{origem}]"
        except FileNotFoundError:
            pass

    read_run_key(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "Registro (Usuário)")
    read_run_key(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "Registro (Sistema)")

    startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
    if os.path.exists(startup_folder):
        for item in os.listdir(startup_folder):
            path = os.path.join(startup_folder, item)
            name = os.path.splitext(item)[0]
            entries[name] = f"{path} [Pasta de Inicialização]"

    return dict(sorted(entries.items(), key=lambda x: x[0].lower()))
