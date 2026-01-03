import sys
import json

def get_system_info():
    data = {
        "cpu_percent": 0.0,
        "ram_used": 0.0,
        "ram_total": 0.0,
        "ram_percent": 0.0,
        "gpu_percent": 0.0,
        "vram_used": 0.0,
        "vram_total": 0.0,
        "vram_percent": 0.0,
        "gpu_temp": 0.0,
        "gpu_name": "N/A",
        "error": None
    }
    
    try:
        import psutil
        
        # CPU Usage
        data["cpu_percent"] = psutil.cpu_percent(interval=0.1)
        
        # RAM Usage
        ram = psutil.virtual_memory()
        data["ram_used"] = ram.used / (1024**3)  # Convert to GB
        data["ram_total"] = ram.total / (1024**3)
        data["ram_percent"] = ram.percent
        
    except ImportError as e:
        data["error"] = f"psutil not available: {str(e)}"
        return data
    except Exception as e:
        data["error"] = f"Error getting CPU/RAM info: {str(e)}"
    
    # GPU Usage (NVIDIA)
    try:
        import pynvml
        pynvml.nvmlInit()
        
        # Get first GPU
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        
        # GPU Name
        data["gpu_name"] = pynvml.nvmlDeviceGetName(handle)
        if isinstance(data["gpu_name"], bytes):
            data["gpu_name"] = data["gpu_name"].decode('utf-8')
        
        # GPU Utilization
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        data["gpu_percent"] = utilization.gpu
        
        # VRAM Usage
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        data["vram_used"] = mem_info.used / (1024**3)
        data["vram_total"] = mem_info.total / (1024**3)
        data["vram_percent"] = (mem_info.used / mem_info.total) * 100
        
        # GPU Temperature
        try:
            data["gpu_temp"] = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        except:
            data["gpu_temp"] = 0.0
        
        pynvml.nvmlShutdown()
        
    except ImportError:
        data["error"] = "pynvml (nvidia-ml-py) not installed"
    except Exception as e:
        if data["error"]:
            data["error"] += f" | GPU error: {str(e)}"
        else:
            data["error"] = f"GPU monitoring error: {str(e)}"
    
    return data

if __name__ == "__main__":
    result = get_system_info()
    print(json.dumps(result))