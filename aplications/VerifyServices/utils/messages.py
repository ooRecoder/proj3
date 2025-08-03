from tkinter import messagebox

def sucesso(msg): messagebox.showinfo("Sucesso", msg)
def erro(msg): messagebox.showerror("Erro", msg)
def alerta(msg): messagebox.showwarning("Aviso", msg)
