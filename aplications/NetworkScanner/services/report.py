import csv
def export_to_txt(devices, filename):
    """
    Exporta a lista de dispositivos para um arquivo .txt
    """
    with open(filename, 'w') as f:
        f.write(f"{'IP':<15} {'MAC':<17} {'Fabricante'}\n")
        f.write("-" * 50 + "\n")
        for device in devices:
            f.write(f"{device['ip']:<15} {device['mac']:<17} {device['vendor']}\n")
    print(f"[+] Relatório salvo em {filename}")


def export_to_csv(devices, filename):
    """
    Exporta a lista de dispositivos para um arquivo .csv
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'MAC', 'Fabricante']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for device in devices:
            writer.writerow({'IP': device['ip'], 'MAC': device['mac'], 'Fabricante': device['vendor']})
    print(f"[+] Relatório salvo em {filename}")
