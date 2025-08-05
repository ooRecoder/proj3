from .gui.main import App
from util import executar_como_admin

def VerifyServices():
    executar_como_admin()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    VerifyServices()
