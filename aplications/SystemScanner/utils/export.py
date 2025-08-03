import os

def export_data(data: dict, filename="relatorio.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for section, values in data.items():
            f.write(f"[{section}]\n")
            for key, value in values.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")

def export_section(section: str, data: dict, filename=None):
    filename = filename or f"{section.lower()}_info.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"[{section}]\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
