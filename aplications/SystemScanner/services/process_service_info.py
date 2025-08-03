import psutil
import time

def get_top_processes_by_memory(n=5):
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            mem = proc.info['memory_percent']
            procs.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs = sorted(procs, key=lambda p: p['memory_percent'], reverse=True)
    top_mem = procs[:n]
    return {f"{p['name']} (PID {p['pid']})": f"{p['memory_percent']:.2f}%" for p in top_mem}

def get_services_status():
    services_info = {}
    for service in psutil.win_service_iter():
        try:
            status = service.status()
            services_info[service.name()] = status
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return services_info
