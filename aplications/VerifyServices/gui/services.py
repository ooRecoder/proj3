from tkinter import ttk
from ..services.services import listar_servicos, controlar_servico

def criar_aba_servicos(frame):
    global tree

    tree = ttk.Treeview(frame, columns=("Nome", "Status"), show="headings")
    tree.heading("Nome", text="Nome do Serviço")
    tree.heading("Status", text="Status")
    tree.pack(fill='both', expand=True)

    btns = ttk.Frame(frame)
    btns.pack(pady=5)

    ttk.Button(btns, text="Atualizar", command=lambda: listar_servicos(tree)).pack(side='left', padx=5)
    ttk.Button(btns, text="Iniciar", command=lambda: controlar_servico(tree, "start")).pack(side='left', padx=5)
    ttk.Button(btns, text="Parar", command=lambda: controlar_servico(tree, "stop")).pack(side='left', padx=5)

    listar_servicos(tree)
