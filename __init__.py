import bpy
from bpy.props import (PointerProperty)
from .hub_mocap import *
from . panel import *


bl_info = {
    "name" : "CEB Hub Mocap",
    "author" : "Carlos Barreto",
    "description" : "",
    "blender" : (4, 4, 0),
    "version" : (0, 8, 0),
    "location" : "UI > SidePanel",
    "warning" : "",
    "category" : "General"
}



classes = (CEB_HubMocapSettings,TL_PT_CEB_HUB_Mocap_Panel,module_4dhumans_Execute,setup_smpl,OPS_OT_update_char_number,ImportCharacter
           ,gvhmr_download_github
           ,WM_OT_AsyncDownload
           ,OT_AsyncUnzip
    ,OPS_OT_run_python_task,
    OPS_OT_run_subprocess,
    OPS_OT_cancel_task,
    ShowHamerData, OpenFolderOperator,UpdtTotCharacterPHMR, download_github_generic, Smooth2, setup_last_part,
    MONITOR_OT_RefreshData
    )

def register():
    
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.hubmocap_prop = PointerProperty(type=CEB_HubMocapSettings)

    bpy.types.Scene.zip_progress_val = bpy.props.FloatProperty(
        name="Progress", 
        default=0.0, 
        min=0.0, 
        max=100.0, 
        subtype='PERCENTAGE'
    )
    bpy.types.Scene.zip_status_msg = bpy.props.StringProperty(
        name="Status", 
        default="Ready"
    )

    bpy.types.Scene.dl_progress = bpy.props.FloatProperty(
        name="Progress", default=0.0, min=0.0, max=100.0, subtype='PERCENTAGE'
    )
    bpy.types.Scene.dl_status = bpy.props.StringProperty(
        name="Status", default="Idle"
    )

    bpy.types.Scene.proc_progress = bpy.props.FloatProperty(
        name="Progress", default=0.0, min=0.0, max=100.0, subtype='PERCENTAGE'
    )
    bpy.types.Scene.proc_status = bpy.props.StringProperty(
        name="Status", default="Idle"
    )

    ##### System Resources
    ### Start
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
    path_addon = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(path_addon, 'blender_system_monitor.py')
    if script_path:
        resource_data["monitor_script_path"] = script_path

     # Check if libraries are already installed (non-blocking)
    def initial_check():
        # if check_libraries():
        # if bpy.context.scene.hubmocap_prop.bool_show_system_resources:
        with data_lock_rm:
            resource_data["libraries_installed"] = True
        start_update_thread()
        # else:
        #     with data_lock_rm:
        #         resource_data["libraries_installed"] = False
    
    thread_rm = threading.Thread(target=initial_check, daemon=True)
    thread_rm.start()
    
    # Register timer
    if not bpy.app.timers.is_registered(monitor_timer):
        bpy.app.timers.register(monitor_timer, first_interval=1.0)

    if not bpy.app.timers.is_registered(redraw_timer):
        bpy.app.timers.register(redraw_timer, first_interval=0.5)

    ### End
    ##### System Resources
    

def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls) 
    del bpy.types.Scene.hubmocap_prop
    del bpy.types.Scene.dl_progress
    del bpy.types.Scene.dl_status
    del bpy.types.Scene.zip_progress_val
    del bpy.types.Scene.zip_status_msg
    del bpy.types.Scene.proc_progress
    del bpy.types.Scene.proc_status

    # Unregister timers
    if bpy.app.timers.is_registered(monitor_timer):
        bpy.app.timers.unregister(monitor_timer)
    
    if bpy.app.timers.is_registered(redraw_timer):
        bpy.app.timers.unregister(redraw_timer)

    
    



if __name__ == "__main__":
    register()
    