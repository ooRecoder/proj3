from tkinter import ttk
from ..services.process import listar_processos, finalizar_processo

def criar_aba_processos(frame):
    global tree

    tree = ttk.Treeview(frame, columns=("PID", "Nome", "Usuário"), show="headings")
    for col in ("PID", "Nome", "Usuário"):
        tree.heading(col, text=col)
    tree.pack(fill='both', expand=True)

    btns = ttk.Frame(frame)
    btns.pack(pady=5)
    ttk.Button(btns, text="Atualizar", command=lambda: listar_processos(tree)).pack(side='left', padx=5)
    ttk.Button(btns, text="Finalizar Processo", command=lambda: finalizar_processo(tree)).pack(side='left')
