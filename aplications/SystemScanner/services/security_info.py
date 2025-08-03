import wmi

def get_security_info():
    security_info = {}

    # Verifica outros antivírus via WMI (opcional)
    try:
        c = wmi.WMI(namespace="root\\SecurityCenter2")
        for av in c.AntiVirusProduct():
            name = av.displayName
            # Para antivírus diferentes do Defender, pode manter a lógica simples
            security_info[f"Antivírus: {name}"] = "Ativo"
    except Exception as e:
        security_info["Antivírus (WMI)"] = f"Erro: {e}"

    # Firewall (mantém a verificação WMI simples)
    try:
        c = wmi.WMI(namespace="root\\SecurityCenter2")
        for fw in c.FirewallProduct():
            name = fw.displayName
            enabled = "Ativo" if fw.productEnabled else "Inativo"
            security_info[f"Firewall: {name}"] = enabled
    except Exception as e:
        security_info["Firewall"] = f"Erro: {e}"

    return security_info
