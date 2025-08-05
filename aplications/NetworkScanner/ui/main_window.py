import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ..services import scanner, report, oui_updater
from .components import RangeInput, ResultsTable, ExportButtons

class NetworkScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scanner de Rede Avançado")
        self.geometry("700x400")

        # Components
        self.range_input = RangeInput(self)
        self.range_input.pack(pady=10)

        self.scan_button = ttk.Button(self, text="Iniciar Scanner", command=self.start_scan)
        self.scan_button.pack(pady=10)

        self.results_table = ResultsTable(self)
        self.results_table.pack(expand=True, fill="both", pady=10)

        self.export_buttons = ExportButtons(self, self.export_result)
        self.export_buttons.pack(pady=5)

        self.devices = []

    def start_scan(self):
        network_range = self.range_input.get_range()
        if not network_range:
            messagebox.showerror("Erro", "Por favor, informe um range de rede.")
            return

        self.scan_button.config(state="disabled")
        self.results_table.clear()
        self.update()

        oui_updater.check_and_update_oui()
        self.devices = scanner.scan_network(network_range)

        if not self.devices:
            messagebox.showinfo("Resultado", "Nenhum dispositivo encontrado.")
        else:
            self.results_table.insert_devices(self.devices)

        self.scan_button.config(state="normal")

    def export_result(self, filetype):
        if not self.devices:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar.")
            return

        file = filedialog.asksaveasfilename(defaultextension=f".{filetype}",
                                             filetypes=[(f"{filetype.upper()} files", f"*.{filetype}")])

        if file:
            if filetype == 'txt':
                report.export_to_txt(self.devices, file)
            elif filetype == 'csv':
                report.export_to_csv(self.devices, file)
            messagebox.showinfo("Exportação", f"Relatório exportado para {file}.")
