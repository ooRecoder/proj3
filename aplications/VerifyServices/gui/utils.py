import tkinter as tk
from tkinter import ttk

def criar_frame_com_scroll(parent):
    """
    Cria um frame com canvas, frame interno e scrollbar vertical.
    Retorna: (container, canvas, inner_frame, scrollbar)
    """
    container = ttk.Frame(parent)
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner_frame = ttk.Frame(canvas)

    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=inner_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack(fill='both', expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return container, canvas, inner_frame, scrollbar
