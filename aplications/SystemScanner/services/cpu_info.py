import psutil
import cpuinfo
import platform

def get_cpu_info():
    cpu = cpuinfo.get_cpu_info()

    freq = psutil.cpu_freq()
    freq_info = {
        "Frequência Atual (MHz)": f"{freq.current:.2f}" if freq else "Não disponível",
        "Frequência Mínima (MHz)": f"{freq.min:.2f}" if freq else "Não disponível",
        "Frequência Máxima (MHz)": f"{freq.max:.2f}" if freq else "Não disponível",
    }

    temp_str = "Não disponível"
    if platform.system() != "Windows":
        try:
            temps = psutil.sensors_temperatures()
            cpu_temps = temps.get('coretemp') or temps.get('cpu-thermal') or temps.get('acpitz') or []
            if cpu_temps:
                temp_values = [t.current for t in cpu_temps if t.current is not None]
                if temp_values:
                    temp_str = f"{sum(temp_values)/len(temp_values):.1f} °C"
        except Exception:
            temp_str = "Não disponível"

    # Instruções suportadas (flags)
    flags = cpu.get('flags', [])
    flags_str = ", ".join(flags) if flags else "Não disponível"

    info = {
        "Processador": cpu.get('brand_raw', 'Não disponível'),
        "Núcleos (físicos/lógicos)": f"{psutil.cpu_count(logical=False)} / {psutil.cpu_count()}",
        **freq_info,
        "Temperatura CPU": temp_str,
        "Instruções Suportadas": flags_str,
    }

    return info
