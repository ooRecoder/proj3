def escolher_opcao():
    print("Selecione uma opção:")
    print("1 - Verificar Versão do Windows dos Pendrives Bootaveís")
    print("2 - System Scanner")
    print("4 - Backup Automações")
    print("5 - Scaneador da Rede")
    print("0 - Sair")
    while True:
        opcao = input("Digite a opção desejada: ").strip()
        if opcao in ("0", "1", "2", "4", "5"):
            return opcao
        print("Opção inválida. Por favor, digite 0 | 1 | 2 | 3 | 4 | 5.")