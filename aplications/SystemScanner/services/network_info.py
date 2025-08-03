import socket
import psutil

def get_network_info():
    info = {}

    # IP principal (interface usada para sair para a internet)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip_local = s.getsockname()[0]
            info["IP Principal (ativo)"] = ip_local
    except:
        info["IP Principal (ativo)"] = "Não disponível"

    # Gateway padrão
    gateways = psutil.net_if_stats()
    net_io = psutil.net_io_counters(pernic=True)
    net_addrs = psutil.net_if_addrs()
    gateways_info = psutil.net_if_stats()
    
    # Obter gateway padrão
    gws = psutil.net_if_stats()
    try:
        gateways = psutil.net_if_stats()
    except Exception:
        gateways = {}

    # Obter gateway padrão via netifaces (mais confiável)
    try:
        import netifaces
        default_gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        info["Gateway Padrão"] = default_gateway
    except ImportError:
        info["Gateway Padrão"] = "netifaces não instalado"
    except Exception:
        info["Gateway Padrão"] = "Não disponível"

    # DNS configurado (Windows)
    try:
        import winreg
        dns_servers = []
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
        key = winreg.OpenKey(reg, key_path)
        value, _ = winreg.QueryValueEx(key, "NameServer")
        if value:
            dns_servers = value.split(',')
        else:
            # fallback
            value, _ = winreg.QueryValueEx(key, "DhcpNameServer")
            dns_servers = value.split(',')
        info["DNS Configurado"] = ', '.join(dns_servers)
    except Exception:
        info["DNS Configurado"] = "Não disponível"

    # Interfaces e velocidades
    interfaces = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()
    for iface, stats in interfaces.items():
        if stats.isup:
            speed_mbps = stats.speed
            # Pega IPv4 para essa interface
            ip = None
            for addr in addrs.get(iface, []):
                if addr.family == socket.AF_INET:
                    ip = addr.address
                    break
            info[f"Interface: {iface} - IP"] = ip or "N/A"
            info[f"Interface: {iface} - Velocidade"] = f"{speed_mbps} Mbps" if speed_mbps else "Desconhecida"

    return info
