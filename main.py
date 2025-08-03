from util import SingleInstance
import sys

if __name__ == "__main__":
    instance = SingleInstance("Global\\MinhaAppUnica")

    if instance.is_running():
        print("A aplicação já está em execução.")
        sys.exit(0)

    print("Aplicação iniciada. Nenhuma outra instância detectada.")
    input("Pressione Enter para encerrar...")