try:
    import GPUtil

    def get_gpu_info():
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return {
                    "GPU": gpus[0].name,
                    "Uso da GPU (%)": f"{gpus[0].load * 100:.0f}%"
                }
            else:
                return {"GPU": "Nenhuma detectada"}
        except:
            return {"GPU": "Erro ao obter"}
except ImportError:
    def get_gpu_info():
        return {"GPU": "GPUtil não instalado"}
