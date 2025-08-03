import psutil
import wmi

def get_disk_info():
    c = wmi.WMI()
    disk_info = {}

    # Busca informações dos discos físicos
    for disk in c.Win32_DiskDrive():
        model = disk.Model.strip()
        media_type = getattr(disk, 'MediaType', 'Desconhecido')
        size_gb = int(disk.Size) / (1024**3) if disk.Size else 0
        key = f"Disco: {model}"
        disk_info[key] = {
            "Modelo": model,
            "Tipo": media_type,
            "Tamanho (GB)": f"{size_gb:.2f} GB",
        }

    # Adiciona informações das partições
    partitions_info = {}
    for part in psutil.disk_partitions(all=False):
        usage = psutil.disk_usage(part.mountpoint)
        partitions_info[f"Partição ({part.device})"] = {
            "Ponto de montagem": part.mountpoint,
            "Sistema de arquivos": part.fstype,
            "Tamanho total": f"{usage.total / (1024**3):.2f} GB",
            "Espaço usado": f"{usage.used / (1024**3):.2f} GB",
            "Espaço livre": f"{usage.free / (1024**3):.2f} GB",
            "Uso (%)": f"{usage.percent}%",
        }

    # Mescla as duas informações (discos e partições)
    disk_info.update(partitions_info)
    return disk_info
