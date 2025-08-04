import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk, messagebox

from .services import carregar_servicos, reiniciar_servico, parar_servico
from .processes import carregar_processos
from .utils import criar_frame_com_scroll

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analisador de Serviços e Processos")
        self.geometry("800x550")

        self._setup_widgets()
        self.recarregar_dados()

    def _setup_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        self.reload_button = ttk.Button(top_frame, text="🔄 Recarregar Dados", command=self.recarregar_dados)
        self.reload_button.pack(side="left", padx=5)

        self.relatorio_button = ttk.Button(top_frame, text="📝 Gerar Relatório", command=self.gerar_relatorio)
        self.relatorio_button.pack(side="left", padx=5)

        self.tabControl = ttk.Notebook(self)
        self.servicos_tab = ttk.Frame(self.tabControl)
        self.suspeitos_tab = ttk.Frame(self.tabControl)
        self.pesados_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.servicos_tab, text='Serviços Críticos')
        self.tabControl.add(self.suspeitos_tab, text='Processos Suspeitos')
        self.tabControl.add(self.pesados_tab, text='Processos Pesados')
        self.tabControl.pack(expand=1, fill="both")

        self.categorias_notebook = ttk.Notebook(self.servicos_tab)
        self.categorias_notebook.pack(expand=1, fill='both')

        self.categoria_frames = {}
        self.servicos_widgets = []
        self.suspeitos_tree = None
        self.pesados_tree = None

    def recarregar_dados(self):
        # Limpa dados antigos
        for categoria, (container, _, _, _) in self.categoria_frames.items():
            container.destroy()
        self.categoria_frames.clear()
        self.categorias_notebook.destroy()

        self.categorias_notebook = ttk.Notebook(self.servicos_tab)
        self.categorias_notebook.pack(expand=1, fill='both')

        for widget in self.servicos_widgets:
            widget.destroy()
        self.servicos_widgets.clear()

        if self.suspeitos_tree:
            self.suspeitos_tree.destroy()
            self.suspeitos_tree = None
        if self.pesados_tree:
            self.pesados_tree.destroy()
            self.pesados_tree = None

        servicos = carregar_servicos()
        processos = carregar_processos()

        for categoria, lista_servicos in servicos.items():
            tab_frame = ttk.Frame(self.categorias_notebook)
            self.categorias_notebook.add(tab_frame, text=categoria)

            container, canvas, inner_frame, scrollbar = criar_frame_com_scroll(tab_frame)
            self.categoria_frames[categoria] = (container, canvas, inner_frame, scrollbar)

            for servico, status in lista_servicos.items():
                cor = "green" if status == "RUNNING" else "red"
                frame = tk.Frame(inner_frame)
                frame.pack(anchor="w", fill="x", padx=10, pady=2)

                lbl = tk.Label(frame, text=f"{servico:<25} -> {status}", fg=cor, font=("Consolas", 10))
                lbl.pack(side="left")

                # Botão sempre visível: Reiniciar
                btn_reiniciar = ttk.Button(frame, text="♻️ Reiniciar", command=lambda s=servico: reiniciar_servico(s, self.recarregar_dados))
                btn_reiniciar.pack(side="left", padx=5)
                self.servicos_widgets.append(btn_reiniciar)

                # Botão visível apenas se o serviço estiver em execução: Parar
                if status == "RUNNING":
                    btn_parar = ttk.Button(frame, text="🛑 Parar", command=lambda s=servico: parar_servico(s, self.recarregar_dados))
                    btn_parar.pack(side="left", padx=5)
                    self.servicos_widgets.append(btn_parar)

                self.servicos_widgets.append(lbl)
                self.servicos_widgets.append(frame)

        self.suspeitos_tree = self._criar_tabela(self.suspeitos_tab, processos['suspeitos'])
        self.pesados_tree = self._criar_tabela(self.pesados_tab, processos['pesados'])

    def _criar_tabela(self, tab, lista_processos):
        cols = ("PID", "Nome", "CPU (%)", "Memória (MB)")
        tree = ttk.Treeview(tab, columns=cols, show='headings')
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        for proc in lista_processos:
            tree.insert('', tk.END, values=(
                proc['pid'],
                proc['nome'],
                f"{proc['cpu']:.1f}",
                f"{proc['mem']:.1f}"
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)
        return tree

    def gerar_relatorio(self):
        servicos = carregar_servicos()
        processos = carregar_processos()

        caminho = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")],
            title="Salvar relatório como..."
        )
        if not caminho:
            return

        linhas = ["=== RELATÓRIO DE ANÁLISE ===\n"]

        linhas.append("\n-- Serviços Críticos --\n")
        for categoria, lista_servicos in servicos.items():
            linhas.append(f"[{categoria}]")
            for nome, status in lista_servicos.items():
                alerta = "⚠️" if status != "RUNNING" else ""
                linhas.append(f"{nome:<25} -> {status} {alerta}")
            linhas.append("")

        linhas.append("\n-- Processos Suspeitos --\n")
        for p in processos['suspeitos']:
            linhas.append(f"[SUSPEITO] {p['nome']} (PID {p['pid']}) - CPU: {p['cpu']}% | Mem: {p['mem']:.1f} MB")

        linhas.append("\n-- Processos Pesados --\n")
        for p in processos['pesados']:
            linhas.append(f"[PESADO]   {p['nome']} (PID {p['pid']}) - CPU: {p['cpu']}% | Mem: {p['mem']:.1f} MB")

        with open(caminho, 'w', encoding='utf-8') as f:
            f.write("\n".join(linhas))

        messagebox.showinfo("Relatório gerado", f"Relatório salvo em:\n{caminho}")

if __name__ == "__main__":
    app = App()
    app.mainloop()