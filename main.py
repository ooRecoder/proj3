from util import SingleInstance
from aplications import VVW, SystemScanner, VerifyServices
import sys
from app import escolher_opcao

if __name__ == "__main__":
    instance = SingleInstance("Global\\MinhaAppUnica")

    if instance.is_running():
        print("A aplicação já está em execução.")
        sys.exit(0)

    opcao = escolher_opcao()
    if opcao == "1":
        VVW()
    elif opcao == "2":
        SystemScanner()
    elif opcao == "3":
        print("Comming Soon")
    else:
        print("Encerrando aplicação.")
        sys.exit(0)