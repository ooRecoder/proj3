# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

from ..services.usb_detector import listar_unidades_usb
from ..services.windows_checker import eh_midia_windows
from ..services.windows_version import obter_versao_windows

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Verificador de Mídia de Instalação do Windows")
        self.geometry("700x450")
        self.configure(padx=15, pady=15)
        self.resizable(False, False)

        # Estilos
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=6)
        self.style.configure('TLabel', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        self.style.configure('Instrucao.TLabel', font=('Segoe UI', 9), foreground='gray25')

        self._criar_widgets()

    def _criar_widgets(self):
        # Frame superior: título e instrução
        topo = ttk.Frame(self)
        topo.pack(fill=tk.X, pady=(0, 12))

        label_titulo = ttk.Label(
            topo,
            text="Verificação de Pendrives Bootáveis do Windows",
            style='Title.TLabel'
        )
        label_titulo.pack(anchor='w')

        label_instrucao = ttk.Label(
            topo,
            text="Clique no botão para identificar mídias de instalação do Windows em pendrives conectados.",
            style='Instrucao.TLabel',
            wraplength=670,
            justify='left'
        )
        label_instrucao.pack(anchor='w', pady=(3,0))

        # Frame central: área de texto compacta com barra de rolagem
        frame_texto = ttk.Frame(self)
        frame_texto.pack(fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(
            frame_texto,
            wrap=tk.WORD,
            font=("Consolas", 10),
            height=14,
            state='disabled'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Cores para tags de texto
        self.text_area.tag_configure("sucesso", foreground="green4")
        self.text_area.tag_configure("erro", foreground="firebrick")
        self.text_area.tag_configure("info", foreground="royalblue")
        self.text_area.tag_configure("normal", foreground="black")

        # Frame inferior: botão centralizado com descrição
        frame_botao = ttk.Frame(self)
        frame_botao.pack(pady=15)

        self.botao_verificar = ttk.Button(
            frame_botao,
            text="Verificar Pendrives",
            command=self.verificar_pendrives,
            width=24
        )
        self.botao_verificar.pack()

        label_rodape = ttk.Label(
            frame_botao,
            text="Aguarde a análise e consulte os resultados na área acima.",
            style='Instrucao.TLabel'
        )
        label_rodape.pack(pady=(6,0))

    def inserir_texto(self, texto, tag="normal"):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, texto + "\n", tag)
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def verificar_pendrives(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.configure(state='disabled')

        # Abaixo chama as funções de verificação (deixe seu código original)
        unidades = listar_unidades_usb()

        if not unidades:
            self.inserir_texto("❌ Nenhum pendrive foi detectado.", "erro")
            return

        for unidade in unidades:
            self.inserir_texto(f"🔍 Verificando unidade: {unidade}", "info")
            if eh_midia_windows(unidade):
                self.inserir_texto("✅ Mídia de instalação do Windows detectada!", "sucesso")
                info = obter_versao_windows(unidade)
                self.inserir_texto(info, "normal")
            else:
                self.inserir_texto("❌ Não é uma mídia de instalação do Windows.", "erro")

            self.inserir_texto("-" * 70, "normal")
