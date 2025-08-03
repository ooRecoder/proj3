from .UI.main_window import MainWindow
from util import executar_como_admin

# Verify Version Windows
def VVW():
    executar_como_admin()
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    VVW()
