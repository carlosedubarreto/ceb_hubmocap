import bpy
from bpy.props import (PointerProperty)
from .hub_mocap import *
from . panel import *


bl_info = {
    "name" : "CEB Hub Mocap",
    "author" : "Carlos Barreto",
    "description" : "",
    "blender" : (4, 4, 0),
    "version" : (0, 3, 0),
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
    ShowHamerData, OpenFolderOperator,UpdtTotCharacterPHMR, download_github_generic
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
    



if __name__ == "__main__":
    register()
    