import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..services import get_full_system_info
from ..utils.export import export_data, export_section

class InfoTab:
    def __init__(self, notebook, title, data):
        self.title = title
        self.frame = ttk.Frame(notebook)

        # Se a data for um dict normal (propriedade: valor)
        if self._is_simple_dict(data):
            self._init_simple_tree(data)
        else:
            # Se for dict com múltiplas subcategorias (ex: Processos e Serviços)
            self._init_complex_tree(data)

    def _is_simple_dict(self, data):
        # Verifica se todos os valores são strings, para definir dict simples
        return all(isinstance(v, str) for v in data.values())

    def _init_simple_tree(self, data):
        self.tree = ttk.Treeview(self.frame, columns=("Propriedade", "Valor"), show="headings")
        self.tree.heading("Propriedade", text="Propriedade")
        self.tree.heading("Valor", text="Valor")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.update(data)

    def _init_complex_tree(self, data):
        # Cria um notebook interno para subcategorias
        self.sub_notebook = ttk.Notebook(self.frame)
        self.sub_notebook.pack(fill="both", expand=True)

        self.trees = {}  # guarda trees por subcategoria

        for subcat, subdata in data.items():
            sub_frame = ttk.Frame(self.sub_notebook)
            tree = ttk.Treeview(sub_frame, columns=("Propriedade", "Valor"), show="headings")
            tree.heading("Propriedade", text="Propriedade")
            tree.heading("Valor", text="Valor")
            tree.pack(fill="both", expand=True, padx=5, pady=5)

            for key, value in subdata.items():
                tree.insert("", "end", values=(key, value))

            self.sub_notebook.add(sub_frame, text=subcat)
            self.trees[subcat] = tree

    def update(self, data):
        if hasattr(self, 'tree'):  # simples
            self.tree.delete(*self.tree.get_children())
            for key, value in data.items():
                self.tree.insert("", "end", values=(key, value))
        else:
            # complexo
            for subcat, subdata in data.items():
                tree = self.trees.get(subcat)
                if tree:
                    tree.delete(*tree.get_children())
                    for key, value in subdata.items():
                        tree.insert("", "end", values=(key, value))

    def get_data(self):
        if hasattr(self, 'tree'):
            return {self.tree.item(item)["values"][0]: self.tree.item(item)["values"][1] for item in self.tree.get_children()}
        else:
            result = {}
            for subcat, tree in self.trees.items():
                result[subcat] = {tree.item(item)["values"][0]: tree.item(item)["values"][1] for item in tree.get_children()}
            return result

def start_app():
    app = tk.Tk()
    app.title("Scanner de Informações do Sistema")
    app.geometry("900x650")

    data = get_full_system_info()

    notebook = ttk.Notebook(app)
    notebook.pack(fill="both", expand=True)

    tabs = {}
    for section, section_data in data.items():
        tab = InfoTab(notebook, section, section_data)
        notebook.add(tab.frame, text=section)
        tabs[section] = tab

    def atualizar_tudo():
        new_data = get_full_system_info()
        for section in tabs:
            tabs[section].update(new_data[section])

    def exportar_tudo():
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
        if caminho:
            full_data = {sec: tabs[sec].get_data() for sec in tabs}
            export_data(full_data, caminho)
            messagebox.showinfo("Exportação", "Todas as informações foram exportadas com sucesso.")

    def exportar_categoria():
        aba = notebook.tab(notebook.select(), "text")
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
        if caminho:
            export_section(aba, tabs[aba].get_data(), caminho)
            messagebox.showinfo("Exportação", f"A categoria '{aba}' foi exportada com sucesso.")

    btn_frame = ttk.Frame(app)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Atualizar Tudo", command=atualizar_tudo).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Exportar Tudo", command=exportar_tudo).grid(row=0, column=1, padx=5)
    ttk.Button(btn_frame, text="Exportar Categoria Atual", command=exportar_categoria).grid(row=0, column=2, padx=5)

    app.mainloop()
