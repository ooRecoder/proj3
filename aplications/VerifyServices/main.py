from tkinter import Tk
from .gui.main import criar_janela

def VerifyServices():
    root = Tk()
    root.title("Verificador de Processos e Serviços")
    root.geometry("800x600")
    criar_janela(root)
    root.mainloop()

if __name__ == "__main__":
    VerifyServices()
