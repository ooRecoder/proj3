import psutil

def listar_unidades_usb():
    unidades_usb = []
    particoes = psutil.disk_partitions(all=False)
    for p in particoes:
        if 'removable' in p.opts.lower():
            unidades_usb.append(p.device)
    return unidades_usb
