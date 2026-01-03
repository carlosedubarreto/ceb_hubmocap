bl_info = {
    "name": "System Resource Monitor (Subprocess)",
    "author": "Your Name",
    "version": (1, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Monitor Tab",
    "description": "Monitor CPU, RAM, GPU, and VRAM usage using subprocess",
    "category": "System",
}

import bpy
import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path
from bpy.app.handlers import persistent

# Global variables to store resource data
resource_data = {
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
    "libraries_installed": False,
    "error_message": "",
    "monitor_script_path": None
}

# The monitoring script that will be run as subprocess
MONITOR_SCRIPT = '''
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
        data["cpu_percent"] = psutil.cpu_percent(interval=0.5)
        
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
'''

def create_monitor_script():
    """Create the monitoring script file"""
    global resource_data
    
    # Create script in temp directory
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, "blender_system_monitor.py")
    
    try:
        with open(script_path, 'w') as f:
            f.write(MONITOR_SCRIPT)
        resource_data["monitor_script_path"] = script_path
        return script_path
    except Exception as e:
        resource_data["error_message"] = f"Failed to create monitor script: {str(e)}"
        return None

# def install_libraries():
#     """Install required libraries into system Python"""
#     python_exe = sys.executable
    
#     try:
#         # Install psutil
#         result1 = subprocess.run(
#             [python_exe, "-m", "pip", "install", "psutil", "--user"],
#             capture_output=True,
#             text=True,
#             timeout=60
#         )
        
#         # Install pynvml for NVIDIA GPU monitoring
#         result2 = subprocess.run(
#             [python_exe, "-m", "pip", "install", "nvidia-ml-py", "--user"],
#             capture_output=True,
#             text=True,
#             timeout=60
#         )
        
#         if result1.returncode == 0 and result2.returncode == 0:
#             return True, "Libraries installed successfully!"
#         else:
#             error_msg = ""
#             if result1.returncode != 0:
#                 error_msg += f"psutil: {result1.stderr}\n"
#             if result2.returncode != 0:
#                 error_msg += f"nvidia-ml-py: {result2.stderr}"
#             return False, f"Installation failed:\n{error_msg}"
            
#     except subprocess.TimeoutExpired:
#         return False, "Installation timeout - please try again"
#     except Exception as e:
#         return False, f"Installation failed: {str(e)}"

def check_libraries():
    """Check if required libraries are available by running a test"""
    if not resource_data["monitor_script_path"]:
        create_monitor_script()
    
    if not resource_data["monitor_script_path"]:
        return False
    
    try:
        python_exec = r"D:\_Code\Meu\_GITHUB\CEB_HubMocap_prj\ceb_hubmocap\python_3.11.9-embed-amd64\python.exe"
        result = subprocess.run(
            [python_exec, resource_data["monitor_script_path"]],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            # If we got data back and no import errors, libraries are available
            if "cpu_percent" in data:
                return True
        return False
    except:
        return False

def update_resource_data():
    """Update resource usage data using subprocess"""
    global resource_data
    
    if not resource_data["monitor_script_path"]:
        create_monitor_script()
    
    if not resource_data["monitor_script_path"]:
        return 2.0
    
    try:
        # Run the monitoring script
        python_exec = r"D:\_Code\Meu\_GITHUB\CEB_HubMocap_prj\ceb_hubmocap\python_3.11.9-embed-amd64\python.exe"
        result = subprocess.run(
            [python_exec, resource_data["monitor_script_path"]],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            
            # Update resource data
            resource_data["cpu_percent"] = data.get("cpu_percent", 0.0)
            resource_data["ram_used"] = data.get("ram_used", 0.0)
            resource_data["ram_total"] = data.get("ram_total", 0.0)
            resource_data["ram_percent"] = data.get("ram_percent", 0.0)
            resource_data["gpu_percent"] = data.get("gpu_percent", 0.0)
            resource_data["vram_used"] = data.get("vram_used", 0.0)
            resource_data["vram_total"] = data.get("vram_total", 0.0)
            resource_data["vram_percent"] = data.get("vram_percent", 0.0)
            resource_data["gpu_temp"] = data.get("gpu_temp", 0.0)
            resource_data["gpu_name"] = data.get("gpu_name", "N/A")
            
            if data.get("error"):
                resource_data["error_message"] = data["error"]
            else:
                resource_data["error_message"] = ""
                
        else:
            resource_data["error_message"] = f"Monitor script error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        resource_data["error_message"] = "Monitor script timeout"
    except json.JSONDecodeError as e:
        resource_data["error_message"] = f"JSON decode error: {str(e)}"
    except Exception as e:
        resource_data["error_message"] = f"Error: {str(e)}"
    
    return 2.0

# class MONITOR_OT_InstallLibraries(bpy.types.Operator):
#     """Install required Python libraries for monitoring"""
#     bl_idname = "monitor.install_libraries"
#     bl_label = "Install Required Libraries"
#     bl_options = {'REGISTER'}
    
#     def execute(self, context):
#         success, message = install_libraries()
#         if success:
#             self.report({'INFO'}, message)
#             # Test libraries after installation
#             if check_libraries():
#                 resource_data["libraries_installed"] = True
#                 self.report({'INFO'}, "Libraries verified successfully!")
#         else:
#             self.report({'ERROR'}, message)
#         return {'FINISHED'}

class MONITOR_OT_RefreshData(bpy.types.Operator):
    """Manually refresh resource data"""
    bl_idname = "monitor.refresh_data"
    bl_label = "Refresh"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if check_libraries():
            update_resource_data()
            self.report({'INFO'}, "Data refreshed")
        else:
            self.report({'WARNING'}, "Libraries not installed")
        return {'FINISHED'}

class MONITOR_OT_TestLibraries(bpy.types.Operator):
    """Test if libraries are properly installed"""
    bl_idname = "monitor.test_libraries"
    bl_label = "Test Libraries"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        if check_libraries():
            self.report({'INFO'}, "Libraries are working correctly!")
            resource_data["libraries_installed"] = True
        else:
            self.report({'ERROR'}, "Libraries not working - please install them")
            resource_data["libraries_installed"] = False
        return {'FINISHED'}

class MONITOR_PT_SystemPanel(bpy.types.Panel):
    """System Resource Monitor Panel"""
    bl_label = "System Monitor"
    bl_idname = "MONITOR_PT_system"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Monitor'
    
    def draw(self, context):
        layout = self.layout
        
        if not resource_data.get("libraries_installed", False):
            box = layout.box()
            box.label(text="Setup Required", icon='ERROR')
            box.operator("monitor.install_libraries", icon='IMPORT')
            box.operator("monitor.test_libraries", icon='VIEWZOOM')
            if resource_data.get("error_message"):
                box.label(text="Error:", icon='ERROR')
                # Split long error messages
                error_lines = resource_data["error_message"].split('\n')
                for line in error_lines[:3]:  # Show first 3 lines
                    box.label(text=line[:50])  # Truncate long lines
            return
        
        # CPU Section
        box = layout.box()
        box.label(text="CPU", icon='SYSTEM')
        row = box.row()
        row.label(text=f"Usage: {resource_data['cpu_percent']:.1f}%")
        row = box.row()
        row.prop(context.scene, "monitor_cpu_progress", text="", slider=True)
        
        # RAM Section
        box = layout.box()
        box.label(text="RAM", icon='MEMORY')
        row = box.row()
        row.label(text=f"{resource_data['ram_used']:.2f} / {resource_data['ram_total']:.2f} GB")
        row = box.row()
        row.label(text=f"Usage: {resource_data['ram_percent']:.1f}%")
        row = box.row()
        row.prop(context.scene, "monitor_ram_progress", text="", slider=True)
        
        # GPU Section
        box = layout.box()
        box.label(text="GPU", icon='SHADING_RENDERED')
        if resource_data['gpu_name'] != "N/A":
            row = box.row()
            row.label(text=resource_data['gpu_name'][:30])  # Truncate long names
        row = box.row()
        row.label(text=f"Usage: {resource_data['gpu_percent']:.1f}%")
        row = box.row()
        row.prop(context.scene, "monitor_gpu_progress", text="", slider=True)
        if resource_data['gpu_temp'] > 0:
            row = box.row()
            row.label(text=f"Temp: {resource_data['gpu_temp']:.0f}°C", icon='LIGHT_SUN')
        
        # VRAM Section
        box = layout.box()
        box.label(text="VRAM", icon='TEXTURE')
        row = box.row()
        row.label(text=f"{resource_data['vram_used']:.2f} / {resource_data['vram_total']:.2f} GB")
        row = box.row()
        row.label(text=f"Usage: {resource_data['vram_percent']:.1f}%")
        row = box.row()
        row.prop(context.scene, "monitor_vram_progress", text="", slider=True)
        
        # Controls
        layout.separator()
        row = layout.row()
        row.operator("monitor.refresh_data", icon='FILE_REFRESH')
        row.operator("monitor.test_libraries", icon='VIEWZOOM')
        
        # Error message
        if resource_data["error_message"]:
            box = layout.box()
            box.label(text="Status:", icon='INFO')
            error_lines = resource_data["error_message"].split('|')
            for line in error_lines:
                box.label(text=line.strip()[:50])

def update_progress_bars(scene):
    """Update progress bar properties based on resource data"""
    scene.monitor_cpu_progress = resource_data['cpu_percent']
    scene.monitor_ram_progress = resource_data['ram_percent']
    scene.monitor_gpu_progress = resource_data['gpu_percent']
    scene.monitor_vram_progress = resource_data['vram_percent']

@persistent
def monitor_timer():
    """Timer function to update resource data"""
    if resource_data.get("libraries_installed", False):
        update_resource_data()
        
        # Update progress bars
        if bpy.context.scene:
            update_progress_bars(bpy.context.scene)
    
    return 2.0  # Update every 2 seconds

classes = (
    # MONITOR_OT_InstallLibraries,
    MONITOR_OT_RefreshData,
    MONITOR_OT_TestLibraries,
    MONITOR_PT_SystemPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Add progress bar properties
    bpy.types.Scene.monitor_cpu_progress = bpy.props.FloatProperty(
        name="CPU",
        min=0.0,
        max=100.0,
        default=0.0,
        subtype='PERCENTAGE'
    )
    bpy.types.Scene.monitor_ram_progress = bpy.props.FloatProperty(
        name="RAM",
        min=0.0,
        max=100.0,
        default=0.0,
        subtype='PERCENTAGE'
    )
    bpy.types.Scene.monitor_gpu_progress = bpy.props.FloatProperty(
        name="GPU",
        min=0.0,
        max=100.0,
        default=0.0,
        subtype='PERCENTAGE'
    )
    bpy.types.Scene.monitor_vram_progress = bpy.props.FloatProperty(
        name="VRAM",
        min=0.0,
        max=100.0,
        default=0.0,
        subtype='PERCENTAGE'
    )
    
    # Create monitor script
    create_monitor_script()
    
    # Check if libraries are already installed
    resource_data["libraries_installed"] = check_libraries()
    
    # Register timer
    if not bpy.app.timers.is_registered(monitor_timer):
        bpy.app.timers.register(monitor_timer, first_interval=1.0)
    
    # Initial data update if libraries available
    if resource_data["libraries_installed"]:
        update_resource_data()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    # Remove progress bar properties
    del bpy.types.Scene.monitor_cpu_progress
    del bpy.types.Scene.monitor_ram_progress
    del bpy.types.Scene.monitor_gpu_progress
    del bpy.types.Scene.monitor_vram_progress
    
    # Unregister timer
    if bpy.app.timers.is_registered(monitor_timer):
        bpy.app.timers.unregister(monitor_timer)
    
    # Clean up monitor script
    if resource_data["monitor_script_path"] and os.path.exists(resource_data["monitor_script_path"]):
        try:
            os.remove(resource_data["monitor_script_path"])
        except:
            pass

if __name__ == "__main__":
    register()