from .services import scanner, report, oui_updater

def NetworkScanner():
    print("===== Scanner de Rede Avançado =====\n")

    # Verificar/Atualizar OUI database
    oui_updater.check_and_update_oui()

    network_range = input("Digite o range de rede (ex: 192.168.1.0/24): ")

    # Executa o Scanner
    devices = scanner.scan_network(network_range)

    if not devices:
        print("Nenhum dispositivo encontrado.")
        return

    # Exibir resultados
    print("\nDispositivos Encontrados:")
    print(f"{'IP':<15} {'MAC':<17} {'Fabricante'}")
    print("-" * 50)
    for device in devices:
        print(f"{device['ip']:<15} {device['mac']:<17} {device['vendor']}")

    # Exportar resultados
    choice = input("\nDeseja exportar o resultado? (txt/csv/nao): ").strip().lower()
    if choice == 'txt':
        report.export_to_txt(devices, 'resultado_scan.txt')
    elif choice == 'csv':
        report.export_to_csv(devices, 'resultado_scan.csv')
    else:
        print("Relatório não salvo.")


if __name__ == "__main__":
    NetworkScanner()
