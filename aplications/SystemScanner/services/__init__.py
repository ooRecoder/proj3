from .cpu_info import get_cpu_info
from .memory_info import get_memory_info
from .disk_info import get_disk_info
from .network_info import get_network_info
from .gpu_info import get_gpu_info
from .system_info import get_system_info
from .inventory_info import get_inventory_info
from .security_info import get_security_info
from .process_service_info import get_top_processes_by_memory, get_services_status
from .installed_programs import get_installed_programs
from .startup_programs import get_startup_programs
from .connectivity_info import get_connectivity_info

def get_process_and_service_info():
    return {
        "Top Processos RAM": get_top_processes_by_memory(),
        "Serviços": get_services_status()
    }


def get_full_system_info():
    return {
        "Sistema": get_system_info(),
        "CPU": get_cpu_info(),
        "Memória": get_memory_info(),
        "Disco": get_disk_info(),
        "Rede": get_network_info(),
        "GPU": get_gpu_info(),
        "Inventário": get_inventory_info(),
        "Segurança": get_security_info(),
        "Processos e Serviços": get_process_and_service_info(),
        "Programas Instalados": get_installed_programs(),
        "Inicialização Automática": get_startup_programs(),
        "Conectividade Externa": get_connectivity_info(),
    }
