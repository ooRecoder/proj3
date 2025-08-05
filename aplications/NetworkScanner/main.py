from .ui.main_window import NetworkScannerApp

def NetworkScanner():
    app = NetworkScannerApp()
    app.mainloop()

if __name__ == "__main__":
    NetworkScanner()
