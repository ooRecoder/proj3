import sys
import webbrowser
from ..getAbsolutPath import get_absolute_path

try:
    from scapy.all import ARP, Ether, srp, conf
except ImportError:
    print("[ERRO] Scapy não está instalado. Instale usando 'pip install scapy'")
    sys.exit(1)


def check_pcap_installed():
    """
    Verifica se o libpcap/Npcap está disponível.
    Se não estiver, redireciona o usuário para a página de download.
    """
    if not conf.use_pcap:
        print("[ERRO] Npcap/WinPcap não encontrado!")
        print("É necessário instalar o Npcap para continuar.")
        print("Abrindo página de download...")
        webbrowser.open("https://nmap.org/npcap/")
        sys.exit(1)


def ping_sweep(network_range):
    """
    Faz ping sweep em uma faixa de IPs.
    Retorna uma lista de IPs ativos.
    """
    print(f"[+] Iniciando Ping Sweep em {network_range} ...")
    active_hosts = []

    # Cria pacote ARP
    arp = ARP(pdst=network_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Envia pacotes e coleta respostas
    result = srp(packet, timeout=2, verbose=0)[0]

    for sent, received in result:
        active_hosts.append({'ip': received.psrc, 'mac': received.hwsrc})

    print(f"[+] {len(active_hosts)} dispositivos encontrados.")
    return active_hosts


def get_vendor(mac_address, oui_file=get_absolute_path('./resources/oui.txt')):
    """
    Consulta o arquivo OUI para identificar o fabricante do MAC Address.
    """
    mac_prefix = mac_address.upper()[0:8].replace(':', '-')
    vendor_found = "Fabricante desconhecido"

    try:
        with open(oui_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for i in range(len(lines)):
                if mac_prefix in lines[i]:
                    # Pega a linha que tem o nome do fabricante
                    vendor_line = lines[i].split('\t')[-1].strip()
                    vendor_found = vendor_line
                    break
    except FileNotFoundError:
        vendor_found = "Arquivo OUI não encontrado."

    return vendor_found


def scan_network(network_range):
    """
    Scanner de rede principal. Retorna lista com IP, MAC e Fabricante.
    """
    devices = ping_sweep(network_range)

    for device in devices:
        vendor = get_vendor(device['mac'])
        device['vendor'] = vendor

    return devices


if __name__ == "__main__":
    check_pcap_installed()  # Verifica se Npcap está instalado

    # Exemplo: '192.168.1.0/24'
    network = input("Digite o range de rede (ex: 192.168.1.0/24): ")
    result = scan_network(network)

    print("\nDispositivos Encontrados:")
    print(f"{'IP':<15} {'MAC':<17} {'Fabricante'}")
    print("-" * 50)
    for device in result:
        print(f"{device['ip']:<15} {device['mac']:<17} {device['vendor']}")
