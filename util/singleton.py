import sys
import win32event # type: ignore
import win32api # type: ignore
import winerror # type: ignore

class SingleInstance:
    """Evita múltiplas instâncias da aplicação no Windows."""
    def __init__(self, mutex_name="my_unique_application_name"):
        self.mutex_name = mutex_name
        self.mutex = win32event.CreateMutex(None, False, self.mutex_name)
        self.last_error = win32api.GetLastError()
        self.already_running = self.last_error == winerror.ERROR_ALREADY_EXISTS

    def is_running(self):
        return self.already_running

    def __del__(self):
        if hasattr(self, 'mutex') and self.mutex:
            win32api.CloseHandle(self.mutex)

# Exemplo de uso
if __name__ == "__main__":
    instance = SingleInstance("Global\\MinhaAppUnica")

    if instance.is_running():
        print("A aplicação já está em execução.")
        sys.exit(0)

    print("Aplicação iniciada. Nenhuma outra instância detectada.")
    # Sua lógica principal aqui (ex: iniciar a GUI)
    input("Pressione Enter para encerrar...")
