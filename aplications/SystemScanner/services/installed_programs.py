import winreg

def get_installed_programs():
    def read_key(hive, subkey):
        programs = {}
        try:
            with winreg.OpenKey(hive, subkey) as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        sub = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub) as item:
                            name = winreg.QueryValueEx(item, "DisplayName")[0]
                            version = ""
                            publisher = ""

                            for j in range(winreg.QueryInfoKey(item)[1]):
                                try:
                                    v_name, v_data, _ = winreg.EnumValue(item, j)
                                    if v_name == "DisplayVersion":
                                        version = v_data
                                    elif v_name == "Publisher":
                                        publisher = v_data
                                except OSError:
                                    continue

                            formatted = f"{version} ({publisher})" if version or publisher else "Desconhecido"
                            programs[name] = formatted
                    except OSError:
                        continue
        except FileNotFoundError:
            pass
        return programs

    result = {}
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    for hive, path in reg_paths:
        result.update(read_key(hive, path))

    return dict(sorted(result.items(), key=lambda x: x[0].lower()))
