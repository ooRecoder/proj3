import psutil

def get_memory_info():
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    return {
        "RAM Total": f"{ram.total / (1024**3):.2f} GB",
        "RAM Disponível": f"{ram.available / (1024**3):.2f} GB",
        "RAM Usada": f"{ram.used / (1024**3):.2f} GB",
        "Uso da RAM (%)": f"{ram.percent}%",
        "Swap Total": f"{swap.total / (1024**3):.2f} GB",
        "Swap Usado": f"{swap.used / (1024**3):.2f} GB",
        "Swap Livre": f"{swap.free / (1024**3):.2f} GB",
        "Uso do Swap (%)": f"{swap.percent}%",
    }
