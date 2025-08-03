def escolher_opcao():
    print("Selecione uma opção:")
    print("1 - Verificar Versão do Windows dos Pendrives Bootaveís")
    print("2 - System Scanner")
    print("3 - Verificador de Serviços")
    print("0 - Sair")
    while True:
        opcao = input("Digite a opção desejada: ").strip()
        if opcao in ("0", "1", "2", "3"):
            return opcao
        print("Opção inválida. Por favor, digite 0 ou 1.")