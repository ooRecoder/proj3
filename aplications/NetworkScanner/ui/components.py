import tkinter as tk
from tkinter import ttk

class RangeInput(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = ttk.Label(self, text="Range de Rede (ex: 192.168.1.0/24):")
        self.label.pack(side="left", padx=5)
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(side="left", padx=5)

    def get_range(self):
        return self.entry.get().strip()

class ResultsTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("IP", "MAC", "Fabricante"), show="headings")
        self.tree.heading("IP", text="IP")
        self.tree.heading("MAC", text="MAC")
        self.tree.heading("Fabricante", text="Fabricante")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", expand=True, fill="both")
        vsb.pack(side="right", fill="y")

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def insert_devices(self, devices):
        for device in devices:
            self.tree.insert("", tk.END, values=(device['ip'], device['mac'], device['vendor']))

class ExportButtons(ttk.Frame):
    def __init__(self, parent, export_callback):
        super().__init__(parent)
        self.export_txt_btn = ttk.Button(self, text="Exportar TXT", command=lambda: export_callback('txt'))
        self.export_txt_btn.pack(side="left", padx=5)

        self.export_csv_btn = ttk.Button(self, text="Exportar CSV", command=lambda: export_callback('csv'))
        self.export_csv_btn.pack(side="left", padx=5)
