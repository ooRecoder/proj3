from tkinter import ttk
from .process import criar_aba_processos
from .services import criar_aba_servicos

def criar_janela(root):
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    frame_proc = ttk.Frame(notebook)
    frame_serv = ttk.Frame(notebook)

    notebook.add(frame_proc, text="Processos")
    notebook.add(frame_serv, text="Serviços")

    criar_aba_processos(frame_proc)
    criar_aba_servicos(frame_serv)
