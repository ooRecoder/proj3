import wmi

def get_inventory_info():
    c = wmi.WMI()

    system_info = c.Win32_ComputerSystem()[0]
    bios_info = c.Win32_BIOS()[0]
    os_info = c.Win32_OperatingSystem()[0]

    product_id = getattr(os_info, 'SerialNumber', "Não disponível")
    serial_number = getattr(bios_info, 'SerialNumber', "Não disponível")
    uuid = getattr(system_info, 'UUID', "Não disponível")
    bios_release_date = bios_info.ReleaseDate.split('.')[0] if bios_info.ReleaseDate else "Não disponível"

    return {
        "Fabricante": system_info.Manufacturer,
        "Modelo": system_info.Model,
        "Número de Série": serial_number,
        "UUID": uuid,
        "Versão BIOS": bios_info.SMBIOSBIOSVersion,
        "Data da BIOS": bios_release_date,
        "Código do Produto Windows": product_id,
        "Sistema Operacional": f"{os_info.Caption} {os_info.Version}",
    }
