import bpy
import os
# from os.path import join
# import sys
import textwrap

from .hub_mocap import *




from bpy.props import (StringProperty,
                        BoolProperty,
                        FloatProperty,
                        IntProperty,
                        EnumProperty,
                        PointerProperty
                        )
from bpy.types import (PropertyGroup)


def get_folder_items(self, context):
    """
    Scans the BASE_FOLDER_PATH and generates the EnumProperty items list.
    """
    hubmocap_prop = context.scene.hubmocap_prop
    path_prompthmr = hubmocap_prop.path_prompthmr

    if hubmocap_prop.module_prompthmr:
        path_code_phmr = os.path.join(path_prompthmr,'PromptHMR_Portable','PromptHMR-main') 
        base_file = os.path.join(path_code_phmr,'results')
    elif hubmocap_prop.module_gvhmr:
        path_gvhmr = hubmocap_prop.path_gvhmr
        path_code_gvhmr = os.path.join(path_gvhmr,'gvhmr','GVHMR-main')
        base_file = os.path.join(path_code_gvhmr,'outputs','demo')
    elif hubmocap_prop.module_hamer:
        path_hamer = hubmocap_prop.path_hamer
        path_code_hamer = os.path.join(path_hamer,'Hamer_Portable','hamer')
        base_file = os.path.join(path_code_hamer,'demo_out')
    # elif hubmocap_prop.module_hamer and :
    BASE_FOLDER_PATH = base_file
    items = []
    
    # Check if the path exists
    if not os.path.isdir(BASE_FOLDER_PATH):
        print(f"Error: Base folder not found at {BASE_FOLDER_PATH}")
        # Return a fallback option if the directory doesn't exist
        return [('NONE', "Folder Not Found", "The configured path is invalid.", 'CANCEL', 0)]

    try:
        # Scan the directory contents
        for i, entry in enumerate(os.scandir(BASE_FOLDER_PATH)):
            # Check if the entry is a directory (folder)
            if entry.is_dir():
                folder_name = entry.name
                
                # EnumProperty item structure: (identifier, name, description, icon, value)
                # The identifier and name are set to the folder_name for simplicity.
                items.append((
                    folder_name, 
                    folder_name, 
                    f"Select {folder_name} as the active project folder.",
                    'FILE_FOLDER', 
                    i
                ))
    except Exception as e:
        print(f"An error occurred while scanning folders: {e}")
        # Return a fallback option in case of permission/reading errors
        return [('ERROR', "Scan Error", "Could not read directory contents.", 'ERROR', 0)]

    if not items:
        # Return a fallback option if the directory is empty
        return [('NONE', "No Folders Found", "The directory is empty.", 'INFO', 0)]

    return items

def get_folder_items_in_hamer(self, context):
    """
    Scans the BASE_FOLDER_PATH and generates the EnumProperty items list.
    """
    hubmocap_prop = context.scene.hubmocap_prop
    enum_hamer_body = hubmocap_prop.enum_hamer_body
    if enum_hamer_body == 'phmr':
        path_prompthmr = hubmocap_prop.path_prompthmr
        path_code_phmr = os.path.join(path_prompthmr,'PromptHMR_Portable','PromptHMR-main') 
        base_file = os.path.join(path_code_phmr,'results')
    elif enum_hamer_body == 'gvhmr':
        path_gvhmr = hubmocap_prop.path_gvhmr
        
        path_code_gvhmr = os.path.join(path_gvhmr,'gvhmr','GVHMR-main')
        base_file = os.path.join(path_code_gvhmr,'outputs','demo')

    # elif hubmocap_prop.module_hamer and :
    BASE_FOLDER_PATH = base_file
    items = []
    
    # Check if the path exists
    if not os.path.isdir(BASE_FOLDER_PATH):
        print(f"Error: Base folder not found at {BASE_FOLDER_PATH}")
        # Return a fallback option if the directory doesn't exist
        return [('NONE', "Folder Not Found", "The configured path is invalid.", 'CANCEL', 0)]

    try:
        # Scan the directory contents
        for i, entry in enumerate(os.scandir(BASE_FOLDER_PATH)):
            # Check if the entry is a directory (folder)
            if entry.is_dir():
                folder_name = entry.name
                
                # EnumProperty item structure: (identifier, name, description, icon, value)
                # The identifier and name are set to the folder_name for simplicity.
                items.append((
                    folder_name, 
                    folder_name, 
                    f"Select {folder_name} as the active project folder.",
                    'FILE_FOLDER', 
                    i
                ))
    except Exception as e:
        print(f"An error occurred while scanning folders: {e}")
        # Return a fallback option in case of permission/reading errors
        return [('ERROR', "Scan Error", "Could not read directory contents.", 'ERROR', 0)]

    if not items:
        # Return a fallback option if the directory is empty
        return [('NONE', "No Folders Found", "The directory is empty.", 'INFO', 0)]

    return items

def updt_tot_char_phmr(self,context):
    import pickle
    hubmocap_prop = context.scene.hubmocap_prop
    path_prompthmr = hubmocap_prop.path_prompthmr
    path_code_phmr = os.path.join(path_prompthmr,'PromptHMR_Portable','PromptHMR-main') 
    base_file = os.path.join(path_code_phmr,'results',hubmocap_prop.enum_list_phmr_folder)
    file_og = os.path.join(base_file,'results.pkl')
    path_phmr_pkl = os.path.join(base_file,'results_world_blender.pkl')
    if not os.path.exists(path_phmr_pkl):

        command = f'../python_embedded/python convert_to_pkl_blender.py --input {file_og}'
        current_folder = os.getcwd()
        os.chdir(path_code_phmr)
        print('inside suproc: ',os.getcwd())
        print('cmd: ',command)
        subprocess.run(command.split(' '))
        os.chdir(current_folder)

    with open(path_phmr_pkl, 'rb') as f:
        data = pickle.load(f)


    hubmocap_prop.int_tot_character_prompthmr = len(data)

def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)   # 7 pix on 1 character
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)


###################################
##### Updt functions for 
##### Button to select the module
##### Unselect other buttons
def updt_button_4dhumans(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.module_4dhumans:
        hubmocap_prop.module_gvhmr = False
        hubmocap_prop.module_prompthmr = False
        hubmocap_prop.module_hamer = False

def updt_button_gvhmr(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.module_gvhmr:
        hubmocap_prop.module_4dhumans = False
        hubmocap_prop.module_prompthmr = False
        hubmocap_prop.module_hamer = False

def updt_button_prompthmr(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.module_prompthmr:
        hubmocap_prop.module_4dhumans = False
        hubmocap_prop.module_gvhmr = False
        hubmocap_prop.module_hamer = False

def updt_button_hamer(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.module_hamer:
        hubmocap_prop.module_4dhumans = False
        hubmocap_prop.module_gvhmr = False
        hubmocap_prop.module_prompthmr = False


#################################


#################################
##### Updt functions for
##### 4D humans Register and Download PKL model
def updt_button_4dhumans_register(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPLify_register:
        hubmocap_prop.SMPLify_download = False

def updt_button_4dhumans_download(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPLify_download:
        hubmocap_prop.SMPLify_register = False
#################################


def updt_button_gvhmr_register(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPL_gvhmr_register:
        hubmocap_prop.SMPL_and_SMPLX_download = False

def updt_button_gvhmr_smpl_and_smplx_download(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPL_and_SMPLX_download:
        hubmocap_prop.SMPL_gvhmr_register = False
#################################

def updt_button_SMPL_download_user_and_pass(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPL_download_user_and_pass:
        hubmocap_prop.SMPLX_download_user_and_pass = False

def updt_button_SMPLX_download_user_and_pass(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.SMPLX_download_user_and_pass:
        hubmocap_prop.SMPL_download_user_and_pass = False        
#################################


###### Hamer Mano Register and Download Buttons
##### 4D humans Register and Download PKL model
def updt_button_hamer_mano_register(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.mano_register:
        hubmocap_prop.mano_download = False

def updt_button_hamer_mano_download(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.mano_download:
        hubmocap_prop.mano_register = False
#################################


def updt_path_4dhumans(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.path_4dhumans != hubmocap_prop.path_4dhumans:
        hubmocap_prop.path_4dhumans = self.path_4dhumans

def updt_custom_venv_name(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    
    custom_venv_name = hubmocap_prop.path_4dhumans
    path_addon = os.path.dirname(os.path.abspath(__file__))
    custom_path_txt = os.path.join(path_addon,'venv_path_4dhumans.txt')
    with open(custom_path_txt, "wt") as fout_custom:
        fout_custom.write(custom_venv_name)

def updt_custom_gvhmr_venv_name(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    
    custom_venv_name = hubmocap_prop.path_gvhmr
    path_addon = os.path.dirname(os.path.abspath(__file__))
    custom_path_txt = os.path.join(path_addon,'venv_path_gvhmr.txt')
    with open(custom_path_txt, "wt") as fout_custom:
        fout_custom.write(custom_venv_name)

def updt_custom_prompthmr_venv_name(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    
    custom_venv_name = hubmocap_prop.path_prompthmr
    path_addon = os.path.dirname(os.path.abspath(__file__))
    custom_path_txt = os.path.join(path_addon,'venv_path_prompthmr.txt')
    with open(custom_path_txt, "wt") as fout_custom:
        fout_custom.write(custom_venv_name)

def updt_custom_hamer_venv_name(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    
    custom_venv_name = hubmocap_prop.path_prompthmr
    path_addon = os.path.dirname(os.path.abspath(__file__))
    custom_path_txt = os.path.join(path_addon,'venv_path_hamer.txt')
    with open(custom_path_txt, "wt") as fout_custom:
        fout_custom.write(custom_venv_name)

def gvhmr_video_path(context):

    hubmocap_prop = context.scene.hubmocap_prop
    path_gvhmr = hubmocap_prop.path_gvhmr
    path_code = os.path.join(path_gvhmr,'gvhmr','GVHMR-main')
    if hubmocap_prop.bool_current_video_gvhmr: 
        video_gvhmr = os.path.splitext(os.path.basename(hubmocap_prop.path_gvhmr_video_input))[0]
        base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
    else:
        video_gvhmr = hubmocap_prop.enum_list_gvhmr_folder
        if video_gvhmr == 'NONE':
            base_file = os.path.join(path_code,'outputs','demo')
        else:
            base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
    return base_file

class TL_PT_CEB_HUB_Mocap_Panel(bpy.types.Panel):
    bl_idname = "TL_PT_CEB_HUB_Mocap_Panel"
    bl_label = "HUB Mocap"
    bl_category = "CEB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    
    def draw(self, context):


        layout = self.layout
        scene = context.scene
        hubmocap_prop = context.scene.hubmocap_prop

        col = layout.column(align=True)
        row = col.row(align=True)
        # col.separator()
        row.prop(hubmocap_prop, "module_4dhumans", text="4DHumans", toggle=True)
        row.prop(hubmocap_prop, "module_gvhmr", text="GVHMR", toggle=True)
        row.prop(hubmocap_prop, "module_prompthmr", text="PromptHMR", toggle=True)
        row = col.row(align=True)
        row.prop(hubmocap_prop, "module_hamer", text="HaMeR", toggle=True)
        


        #####################################
        ### Options for 4DHumans
        #####################################


        if hubmocap_prop.module_4dhumans:
            col = layout.box().column(align=True)
            col = col.column(align=True)
            col.label(text="4DHumans Project links")
            row = col.row(align=True)
            op = row.operator("wm.url_open", text="Github")
            op.url = "https://github.com/shubham-goel/4D-Humans"

            op = row.operator("wm.url_open", text="License")
            op.url = "https://github.com/shubham-goel/4D-Humans?tab=MIT-1-ov-file#readme"

            col = layout.box().column(align=True)
            row = col.row(align=True)
            # col.label(text="4DHumans")
            col.prop(hubmocap_prop, "path_4dhumans_video_input", text="Video")

            #################################################################
            ######
            # col = layout.column(align=True)

            # Status header
            col_alert = col.column(align=True)
            if RUNNER.status_text.startswith("Running"):
                col_alert.alert = True
            else:
                col_alert.alert = False
            col_alert.label(text=f"Status: {RUNNER.status_text}")
            # col.label(text=f"Task: {RUNNER.task_name or '-'}")
            col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

            # Last log line
            if RUNNER.last_log:
                col.label(text=f"Last: {RUNNER.last_log[:100]}")

            # Controls
            row_subproc = col.row(align=True)
            if RUNNER.status_text.startswith("Running") or not os.path.exists(hubmocap_prop.path_4dhumans_video_input) :
                row_subproc.enabled = False
            else:
                row_subproc.enabled = True
            # row.operator(OPS_OT_run_python_task.bl_idname, text="Run Python Task")
            subproc = row_subproc.operator(OPS_OT_run_subprocess.bl_idname, text="Run")
            subproc.module='4dhumans'
            # row.operator(OPS_OT_cancel_task.bl_idname, text="Cancel") #disabled because it was not working
            ##################################################################
            path_4dhumans = hubmocap_prop.path_4dhumans
            base_file = os.path.join(path_4dhumans,'4dhumans','4D-Humans-main','outputs','results')
            file_converted = os.path.join(base_file,'demo_video.pkl')
            
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            if os.path.exists(file_converted):
                col.enabled = True
            else:
                col.enabled = False
            if hubmocap_prop.int_tot_character ==0:
                row.label(text='Click "Update" -->')
            else:
                row.label(text='Characters : '+str(hubmocap_prop.int_tot_character))
            col.prop(hubmocap_prop, "int_character", text="Character")
            col.operator('hubmocap.import_character', text="Import Mocap")
            

            row_upt = row.column(align=True)
            if os.path.exists(file_converted):
                row_upt.enabled = True
            else:
                row_upt.enabled = False
            row_upt.operator(OPS_OT_update_char_number.bl_idname, text="Update")



            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            col.prop(hubmocap_prop, "module_4dhumans_install", text="Install Options",toggle=True)
            if hubmocap_prop.module_4dhumans_install:
                if hubmocap_prop.path_4dhumans == '':
                    col.alert = True
                else:
                    col.alert = False
                col.label(text="Path for 4DHumans")
                # col.prop(hubmocap_prop, "path_4dhumans", text="")
                
                col_alert = col.column(align=True)
                col_alert.prop(hubmocap_prop, "path_4dhumans", text="")
                if ' ' in hubmocap_prop.path_4dhumans:
                    col_alert.alert = True
                    col_alert.label(text=f"Video path with spaces,")
                    col_alert.label(text=f" please remove them!")
                else:
                    col_alert.alert = False


                ###################################
                ## Check if module is installed
                # box = layout.box()
                # col = box.column(align=True)
                # row = col.row(align=True)

                col.label(text="Get the Module")
                
                op = col.operator("wm.url_open", text="Gumroad (PAID)", icon='TAG')
                op.url = "https://carlosedubarreto.gumroad.com/l/py_embed_4dhumans"

                


                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                if hubmocap_prop.path_4dhumans == '':
                    col.enabled = False
                else:
                    col.enabled = True
                col.label(text="Unzipping 4DHumans")
                col.prop(hubmocap_prop, "path_4dhumans_zip", text="Zip File")
                
                col.operator("hubmocap.async_unzip", text="Start Unzip", icon='MOD_EXPLODE')
            
                # Draw the status text
                col.label(text=scene.zip_status_msg)
                
                # Draw the progress bar
                # We use 'factor' to tell Blender this float is a percentage (0-100)
                if scene.zip_progress_val > 0.0 and scene.zip_progress_val < 100.0:
                    col.enabled = True
                    col.prop(scene, "zip_progress_val", text="Progress", slider=True)
            # else:
            #     col.label(text="4DHumans is installed")
            ###################################



            #####################################
            ### Check if SMPL PKL exists
            path_4dhuman_smpl_file1 = os.path.join(hubmocap_prop.path_4dhumans,'4dhumans','.cache','4DHumans','data','smpl','SMPL_NEUTRAL.pkl')
            path_4dhuman_smpl_file2 = os.path.join(hubmocap_prop.path_4dhumans,'4dhumans','.cache','phalp','3D','models','smpl','SMPL_NEUTRAL.pkl')

            chk_4dhumans_smpl_file1 = os.path.exists(path_4dhuman_smpl_file1)
            chk_4dhumans_smpl_file2 = os.path.exists(path_4dhuman_smpl_file2)

            if hubmocap_prop.module_4dhumans_install:

                if not chk_4dhumans_smpl_file1 or not chk_4dhumans_smpl_file2:
                    box = layout.box()
                    col = box.column(align=True)
                    row = col.row(align=True)
                    
                    if not hubmocap_prop.SMPLify_register and not hubmocap_prop.SMPLify_download:
                        long_text1 = "You need to register to download the SMPLify PKL file. "
                        long_text2 = "If you are not registered, choose the REGISTER button to get to the SMPL register site."
                        long_text3 = "If you have a registration, choose the DOWNLOAD button and insert your email and password to download the SMPL PKL file."
                        _label_multiline(context, long_text1, col)
                        col.separator()
                        _label_multiline(context, long_text2, col)
                        col.separator()
                        _label_multiline(context, long_text3, col)
                    
                    ###########################
                    ## Download SMPLify PKL
                    row.prop(hubmocap_prop,'SMPLify_register',text="Register", icon='WORDWRAP_ON', toggle=True)
                    row.prop(hubmocap_prop,'SMPLify_download',text="Download", icon='EVENT_DOWN_ARROW', toggle=True)

                    if hubmocap_prop.SMPLify_register:
                        op = layout.operator("wm.url_open", text="Register on SMPLify", icon='GREASEPENCIL')
                        op.url = "https://smplify.is.tue.mpg.de/register.php"

                    if hubmocap_prop.SMPLify_download:
                        # hubmocap_prop.SMPLify_email
                        # hubmocap_prop.SMPLify_password

                        col.prop(hubmocap_prop,'SMPL_email',text="Email")
                        col.prop(hubmocap_prop,'SMPL_password',text="Password")

                        # col.operator("hubmocap.smplify_download", text="Download SMPL PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl = col.operator('hubmocap.async_download_post', text="Download SMPL PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=smplify&sfile=mpips_smplify_public_v2.zip&resume=1"

                        
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_4dhumans,'temp','mpips_smplify_public_v2.zip')

                        # layout.separator()
            
                        # Display Status
                        layout.label(text=f"Status: {scene.dl_status}")
                        
                        # Display Progress Bar
                        col = layout.column()
                        if scene.dl_status != 'Download Complete!':
                            col.prop(scene, "dl_progress", text="Progress", slider=True)
                        
                        col_setup = col.column(align=True) # Setup SMPL
                        if not os.path.exists(os.path.join(hubmocap_prop.path_4dhumans,'temp','mpips_smplify_public_v2.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl")
                        ssmpl.module_id = '4dhumans'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_4dhumans,'temp','mpips_smplify_public_v2.zip')
                        ssmpl.wanted_files = json.dumps(['smplify_public/code/models/basicModel_neutral_lbs_10_207_0_v1.0.0.pkl']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_4dhumans,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_4dhumans,'4dhumans','.cache')
                else:
                    col = layout.column(align=True)
                    row = col.row(align=True)
                    row.label(text="SMPLify PKL file is already Installed.")


          


        #####################################
        ### Options for GVHMR
        #####################################

        if hubmocap_prop.module_gvhmr:        
            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text="GVHMR")
            path_gvhmr = hubmocap_prop.path_gvhmr
            path_code = os.path.join(path_gvhmr,'gvhmr','GVHMR-main')


            col = layout.box().column(align=True)
            row = col.row(align=True)
            # col.label(text="4DHumans")
            # col.prop(hubmocap_prop, "path_gvhmr_video_input", text="Video")

            col_alert = col.column(align=True)
            col_alert.prop(hubmocap_prop, "path_gvhmr_video_input", text="Video")
            if ' ' in hubmocap_prop.path_gvhmr_video_input:
                col_alert.alert = True
                col_alert.label(text=f"Video path with spaces,")
                col_alert.label(text=f" please remove them!")
            else:
                col_alert.alert = False
                file_name = os.path.basename(hubmocap_prop.path_gvhmr_video_input)
                col_alert.label(text=f"File: {file_name}")


            #################################################################
            ######
            # col = layout.column(align=True)

            # Status header
            col_alert = col.column(align=True)
            if RUNNER.status_text.startswith("Running"):
                col_alert.alert = True
            else:
                col_alert.alert = False
            col_alert.label(text=f"Status: {RUNNER.status_text}")
            # col.label(text=f"Task: {RUNNER.task_name or '-'}")
            # col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

            # Last log line
            if RUNNER.last_log:
                col.label(text=f"Last: {RUNNER.last_log[:100]}")

            # video_gvhmr = os.path.splitext(os.path.basename(hubmocap_prop.path_gvhmr_video_input))[0]
            # base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
            base_file = gvhmr_video_path(context)

            #### Organizando para ver a quantidade de personagens, de acordo com a escolha, video atual ou o que ja foi executado
            ################################
            if hubmocap_prop.bool_current_video_gvhmr:
                if hubmocap_prop.int_tot_character_gvhmr == -1 or not os.path.exists(base_file):
                    col.label(text='Character: it will show after first exec')
                else:
                    col.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_gvhmr))
            else: # se for pegar videos antigos, listar quantos ja foram executados
                tot_char = 0
                list_files = os.listdir(base_file)
                for lf in list_files:
                    if '.pkl' in lf:
                        tot_char += 1
                col.label(text=f'Characters : '+str(tot_char))
                


            #################################
            row = col.row(align=True)
            row.prop(hubmocap_prop, "int_character_gvhmr", text="Character")
            row.prop(hubmocap_prop, 'int_fps_gvhmr', text='FPS')
            # Controls
            row_subproc = col.row(align=True)
            if RUNNER.status_text.startswith("Running") or not os.path.exists(hubmocap_prop.path_gvhmr_video_input) or ' ' in hubmocap_prop.path_gvhmr_video_input:
                row_subproc.enabled = False
            else:
                row_subproc.enabled = True
            # row.operator(OPS_OT_run_python_task.bl_idname, text="Run Python Task")
            subproc = row_subproc.operator(OPS_OT_run_subprocess.bl_idname, text="Run")
            subproc.module='gvhmr'
            ######################################

            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            # if hubmocap_prop.bool_current_video_gvhmr: # Tive que copiar esse codigo aqui pra cima, por que no trecho de baixo ele esta ligado com a impressao em tela dos aquivos gerados, e eu so precisava do caminho para  abrir a pasta no windows explorer
            #     video_gvhmr = os.path.splitext(os.path.basename(hubmocap_prop.path_gvhmr_video_input))[0]
            #     base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
            # else:
            #     video_gvhmr = hubmocap_prop.enum_list_gvhmr_folder
            #     if video_gvhmr == 'NONE':
            #         base_file = os.path.join(path_code,'outputs','demo')
            #     else:
            #         base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
            
            # troquei o codigo acima por essa funcao, ja que estou usando em varios lugares.
            base_file = gvhmr_video_path(context)


            row.label(text="Import Mocap")
            open_folder =row.operator('hubmocap.open_folder_explorer', icon='FILE_FOLDER', text='')
            open_folder.folder_path = base_file
            col.prop(hubmocap_prop,'bool_current_video_gvhmr')
            int_char = hubmocap_prop.int_character_gvhmr


            
            
            col.label(text='GVHM Files')

            if hubmocap_prop.bool_current_video_gvhmr:
                video_gvhmr = os.path.splitext(os.path.basename(hubmocap_prop.path_gvhmr_video_input))[0]
                base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
                if os.path.exists(base_file):
                    list_files = os.listdir(base_file)
                    for lf in list_files:
                        if '.pkl' in lf:
                            col.label(text=lf)
                else:
                    col_alert = col.column(align=True)
                    col_alert.alert = True
                    col_alert.label(text='No files Available yet')
                path_import_pkl = os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','outputs','demo',video_gvhmr,'hmr4d_results.pt'+'_person-'+str(int_char)+".pkl")
            else:
                col.prop(hubmocap_prop,'enum_list_gvhmr_folder')
                video_gvhmr = hubmocap_prop.enum_list_gvhmr_folder
                if video_gvhmr == 'NONE':
                    path_import_pkl = 'NONE'
                else:
                    base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
                    list_files = os.listdir(base_file)
                    for lf in list_files:
                        if '.pkl' in lf:
                            col.label(text=lf)
                    path_import_pkl = os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','outputs','demo',video_gvhmr,'hmr4d_results.pt'+'_person-'+str(int_char)+".pkl")

            col_enable = col.column(align=True)
            if os.path.exists(path_import_pkl):
                col_enable.enabled = True
            else:
                col_enable.enabled = False
            import_char = col_enable.operator('hubmocap.import_character', text="Import Mocap")
            import_char.option = 1 #gvhmr



            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            col.prop(hubmocap_prop, "module_gvhmr_install", text="Install Options",toggle=True)

            if hubmocap_prop.module_gvhmr_install:
                if hubmocap_prop.path_gvhmr == '':
                    col.alert = True
                else:
                    col.alert = False
                col.label(text="Path for GVHMR")
                # col.prop(hubmocap_prop, "path_gvhmr", text="")

                col_alert = col.column(align=True)
                col_alert.prop(hubmocap_prop, "path_gvhmr", text="")
                if ' ' in hubmocap_prop.path_gvhmr:
                    col_alert.alert = True
                    col_alert.label(text=f"Video path with spaces,")
                    col_alert.label(text=f" please remove them!")
                else:
                    col_alert.alert = False


                ##############################################
                ###### GVHMR Install Options

                ###################################
                ## Check if module is installed
                # box = layout.box()
                # col = box.column(align=True)
                # row = col.row(align=True)
                col.label(text="Get the Module")
                
                op = col.operator("wm.url_open", text="Gumroad (PAID)", icon='TAG')
                op.url = "https://carlosedubarreto.gumroad.com/l/py_embed_gvhmr"

                


                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                if hubmocap_prop.path_gvhmr == '':
                    col.enabled = False
                else:
                    col.enabled = True
                col.label(text="Unzipping GVHMR")
                col.prop(hubmocap_prop, "path_gvhmr_zip", text="Zip File")
                
                col.operator("hubmocap.async_unzip", text="Start Unzip", icon='MOD_EXPLODE')
            
                # Draw the status text
                col.label(text=scene.zip_status_msg)
                
                # Draw the progress bar
                # We use 'factor' to tell Blender this float is a percentage (0-100)
                if scene.zip_progress_val > 0.0 and scene.zip_progress_val < 100.0:
                    col.enabled = True
                    col.prop(scene, "zip_progress_val", text="Progress", slider=True)

                ####### Download GVHMR from github
                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                col_down_github = col.column(align=True)
                if os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main')):
                    col_down_github.enabled = False
                else:
                    col_down_github.enabled = True
                col_down_github.operator(gvhmr_download_github.bl_idname, text="Downlaod Github Code")

                col.label(text="Downloading Checkpoints")
                line1_txt = col.row(align=True)
                row_ckpt = line1_txt.row(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','dpvo','dpvo.pth')):
                    row_ckpt.label(text='[    ] dpvo')
                else:
                    row_ckpt.label(text='[ OK ] dpvo')

                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','gvhmr','gvhmr_siga24_release.ckpt')):
                    row_ckpt.label(text='[    ] gvhmr')
                else:
                    row_ckpt.label(text='[ OK ] gvhmr')


                line2_txt = col.row(align=True)
                row_ckpt = line2_txt.row(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','hmr2','epoch=10-step=25000.ckpt')):
                    row_ckpt.label(text='[    ] hmr2')
                else:
                    row_ckpt.label(text='[ OK ] hmr2')

                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','vitpose','vitpose-h-multi-coco.pth')):
                    row_ckpt.label(text='[    ] vitpose')
                else:
                    row_ckpt.label(text='[ OK ] vitpose')

                line3_txt = col.row(align=True)
                row_ckpt = line3_txt.row(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','yolo','yolov8x.pt')):
                    row_ckpt.label(text='[    ] yolo')
                else:
                    row_ckpt.label(text='[ OK ] yolo')


                ### DPVO
                line1 = col.row(align=True)
                row_sp_down_dpvo = line1.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','dpvo','dpvo.pth')):
                    row_sp_down_dpvo.enabled = True
                else:
                    row_sp_down_dpvo.enabled = False
                subproc = row_sp_down_dpvo.operator(OPS_OT_run_subprocess.bl_idname, text="DPVO")
                subproc.module='gvhmr_ckpt_dpvo'

                ### GVHMR
                row_sp_down_gvhmr = line1.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','gvhmr','gvhmr_siga24_release.ckpt')):
                    row_sp_down_gvhmr.enabled = True
                else:
                    row_sp_down_gvhmr.enabled = False
                subproc = row_sp_down_gvhmr.operator(OPS_OT_run_subprocess.bl_idname, text="GVHMR")
                subproc.module='gvhmr_ckpt_gvhmr'


                ### hmr2
                line2 = col.row(align=True)
                row_sp_down_hmr2 = line2.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','hmr2','epoch=10-step=25000.ckpt')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="HMR2")
                subproc.module='gvhmr_ckpt_hmr2'

                ### vitpose
                row_sp_down_vitpose = line2.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','vitpose','vitpose-h-multi-coco.pth')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="VITPOSE")
                subproc.module='gvhmr_ckpt_vitpose'


                ### yolo
                line3 = col.row(align=True)
                row_sp_down_yolo = line3.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','inputs','checkpoints','yolo','yolov8x.pt')):
                    row_sp_down_yolo.enabled = True
                else:
                    row_sp_down_yolo.enabled = False
                subproc = row_sp_down_yolo.operator(OPS_OT_run_subprocess.bl_idname, text="YOLO")
                subproc.module='gvhmr_ckpt_yolo'


                if RUNNER.status_text.startswith("Running"):

                    col.label(text=f"Status: {RUNNER.status_text}")
                    # col.label(text=f"Task: {RUNNER.task_name or '-'}")
                    # col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

                    # Last log line
                    if RUNNER.last_log:
                        col.label(text=f"Last: {RUNNER.last_log[:100]}")


                ### Download and place the SMPL / SMPLX files
                ####### Download GVHMR from github
                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                # col.label(text="Download SMPL / SMPLX files")

                if not hubmocap_prop.SMPL_gvhmr_register and not hubmocap_prop.SMPL_and_SMPLX_download:
                    long_text1 = "You need to register to download the SMPL and SMPLX PKL file. "
                    long_text2 = "If you are not registered, choose the REGISTER button to get to the SMPL register site."
                    long_text3 = "If you have a registration, choose the DOWNLOAD button and insert your email and password to download the SMPL PKL file."
                    _label_multiline(context, long_text1, col)
                    col.separator()
                    _label_multiline(context, long_text2, col)
                    col.separator()
                    _label_multiline(context, long_text3, col)
                
                ########################################
                ## Download SMPL and SMPLX PKL for GVHMR
                row.prop(hubmocap_prop,'SMPL_gvhmr_register',text="Register", icon='WORDWRAP_ON', toggle=True)
                row.prop(hubmocap_prop,'SMPL_and_SMPLX_download',text="Download", icon='EVENT_DOWN_ARROW', toggle=True)

                if hubmocap_prop.SMPL_gvhmr_register:
                    op = layout.operator("wm.url_open", text="Register on SMPL", icon='GREASEPENCIL')
                    op.url = "https://smpl.is.tue.mpg.de/register.php"

                    op = layout.operator("wm.url_open", text="Register on SMPLX", icon='GREASEPENCIL')
                    op.url = "https://smpl-x.is.tue.mpg.de/register.php"

                if hubmocap_prop.SMPL_and_SMPLX_download:
                    # hubmocap_prop.SMPLify_email
                    # hubmocap_prop.SMPLify_password
                    row = col.row(align=True)
                    row.prop(hubmocap_prop,'SMPL_download_user_and_pass',text="SMPL", icon='EVENT_DOWN_ARROW', toggle=True)
                    row.prop(hubmocap_prop,'SMPLX_download_user_and_pass',text="SMPLX", icon='EVENT_DOWN_ARROW', toggle=True)

                    if hubmocap_prop.SMPL_download_user_and_pass or hubmocap_prop.SMPLX_download_user_and_pass:
                        col.prop(hubmocap_prop,'SMPL_email',text="Email")
                        col.prop(hubmocap_prop,'SMPL_password',text="Password")

                    if hubmocap_prop.SMPL_download_user_and_pass:

                        down_smpl = col.operator('hubmocap.async_download_post', text="Download SMPL PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_python_v.1.1.0.zip&resume=1"
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_gvhmr,'temp','SMPL_python_v.1.1.0.zip')
                        ######################################
                        #### Setup SMPL
                        col_setup = col.column(align=True) 
                        if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'temp','SMPL_python_v.1.1.0.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl")
                        ssmpl.module_id = 'gvhmr_smpl'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_gvhmr,'temp','SMPL_python_v.1.1.0.zip')
                        ssmpl.wanted_files = json.dumps(['SMPL_python_v.1.1.0/smpl/models/basicmodel_f_lbs_10_207_0_v1.1.0.pkl',
                                                        'SMPL_python_v.1.1.0/smpl/models/basicmodel_m_lbs_10_207_0_v1.1.0.pkl',
                                                        'SMPL_python_v.1.1.0/smpl/models/basicmodel_neutral_lbs_10_207_0_v1.1.0.pkl']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_gvhmr,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_gvhmr,'GVHMR','GVHMR-main','inputs','checkpoints','body_models','smpl')

                    if hubmocap_prop.SMPLX_download_user_and_pass:
                        down_smpl = col.operator('hubmocap.async_download_post', text="Download SMPLX PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=smplx&sfile=models_smplx_v1_1.zip&resume=1"
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_gvhmr,'temp','models_smplx_v1_1.zip')

                        ######################################
                        #### Setup SMPLX
                        col_setup = col.column(align=True) 
                        if not os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'temp','models_smplx_v1_1.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl",text="Setup SMPLX")
                        ssmpl.module_id = 'gvhmr_smplx'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_gvhmr,'temp','models_smplx_v1_1.zip')
                        ssmpl.wanted_files = json.dumps(['models/smplx/SMPLX_FEMALE.npz',
                                                        'models/smplx/SMPLX_MALE.npz',
                                                        'models/smplx/SMPLX_NEUTRAL.npz']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_gvhmr,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_gvhmr,'GVHMR','GVHMR-main','inputs','checkpoints','body_models','smplx')




                    


                    # layout.separator()
        
                    # Display Status
                    layout.label(text=f"Status: {scene.dl_status}")
                    
                    # Display Progress Bar
                    col = layout.column()
                    if scene.dl_status != 'Download Complete!':
                        col.prop(scene, "dl_progress", text="Progress", slider=True)
                
        #####################################
        ### Options for PromptHMR
        #####################################
        if hubmocap_prop.module_prompthmr:        
            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text="PromptHMR")


            col = layout.box().column(align=True)
            row = col.row(align=True)
            # col.label(text="4DHumans")
            col_alert = col.column(align=True)
            col_alert.prop(hubmocap_prop, "path_prompthmr_video_input", text="Video")
            if ' ' in hubmocap_prop.path_prompthmr_video_input:
                col_alert.alert = True
                col_alert.label(text=f"Video path with spaces,")
                col_alert.label(text=f" please remove them!")
            else:
                col_alert.alert = False
                file_name = os.path.basename(hubmocap_prop.path_prompthmr_video_input)
                col_alert.label(text=f"File: {file_name}")




            #################################################################
            ######
            # col = layout.column(align=True)

            # Status header
            col_alert = col.column(align=True)
            if RUNNER.status_text.startswith("Running"):
                col_alert.alert = True
            else:
                col_alert.alert = False
            col_alert.label(text=f"Status: {RUNNER.status_text}")
            # col.label(text=f"Task: {RUNNER.task_name or '-'}")
            # col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

            # Last log line
            if RUNNER.last_log:
                col.label(text=f"Last: {RUNNER.last_log[:100]}")
            
            # if hubmocap_prop.int_tot_character_gvhmr == -1:
            #     col.label(text='Character: it will show after first exec')
            # else:
            #     col.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_gvhmr))
            # row = col.row(align=True)
            # row.prop(hubmocap_prop, "int_character_gvhmr", text="Character")
            # row.prop(hubmocap_prop, 'int_fps_gvhmr', text='FPS')
            # Controls
            row_subproc = col.row(align=True)
            if RUNNER.status_text.startswith("Running") or not os.path.exists(hubmocap_prop.path_prompthmr_video_input) or  ' ' in hubmocap_prop.path_prompthmr_video_input :
                row_subproc.enabled = False
            else:
                row_subproc.enabled = True
            # row.operator(OPS_OT_run_python_task.bl_idname, text="Run Python Task")
            subproc = row_subproc.operator(OPS_OT_run_subprocess.bl_idname, text="Run")
            subproc.module='prompthmr'
            ######################################

            path_prompthmr = hubmocap_prop.path_prompthmr
            path_code = os.path.join(path_prompthmr,'PromptHMR_Portable','PromptHMR-main') 

            if hubmocap_prop.bool_current_video_phmr:
                video_name = os.path.splitext(os.path.basename(hubmocap_prop.path_prompthmr_video_input))[0]
                base_file = os.path.join(path_code,'results',video_name)
            else:
                video_name = hubmocap_prop.enum_list_phmr_folder
                if video_name == 'NONE':
                    base_file = os.path.join(path_code,'results')
                else:
                    base_file = os.path.join(path_code,'results',video_name)


            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.label(text="Import Mocap")
            open_folder =row.operator('hubmocap.open_folder_explorer', icon='FILE_FOLDER', text='')
            open_folder.folder_path = base_file

            row = col.row(align=True)
            if hubmocap_prop.bool_current_video_phmr:
                if os.path.exists(os.path.join(base_file,'results.pkl')):
                    row.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_prompthmr))
                    row.operator('hubmocap.update_total_character_phmr', text='', icon='FILE_REFRESH', emboss=True)
                else:
                    row.label(text='Character: Run the process first')
            else:
                row.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_prompthmr))

            

            row = col.row(align=True)
            row.prop(hubmocap_prop, "int_character_prompthmr", text="Character")
            row.prop(hubmocap_prop, "int_fps_prompthmr", text="FPS")

            col.prop(hubmocap_prop,'bool_current_video_phmr', text='Work on Current Video')
            if not hubmocap_prop.bool_current_video_phmr:
                col.prop(hubmocap_prop,'enum_list_phmr_folder', text='Folder')
             
            ## Adicionar checagem para ver se o arquivo pkl necessario existe, se nao existir, desativar o botao

            col_import = col.column(align=True)
            if os.path.exists(os.path.join(base_file,'results.pkl')) and hubmocap_prop.int_character_prompthmr <= hubmocap_prop.int_tot_character_prompthmr:
                col_import.enabled = True
            else:
                col_import.enabled = False
            import_char = col_import.operator('hubmocap.import_character', text="Import Mocap")
            import_char.option = 2 #Prompthmr




            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            col.prop(hubmocap_prop, "module_phmr_install", text="Install Options",toggle=True)

            if hubmocap_prop.module_phmr_install:
                if hubmocap_prop.path_gvhmr == '':
                    col.alert = True
                else:
                    col.alert = False
                col.label(text="Path for PromptHMR")
                col.prop(hubmocap_prop, "path_prompthmr", text="")

                ##############################################
                ###### Hamer Install Options

                ###################################
                ## Check if module is installed
                # box = layout.box()
                # col = box.column(align=True)
                # row = col.row(align=True)
                col.label(text="Get the Module")
                
                op = col.operator("wm.url_open", text="Gumroad (PAID)", icon='TAG')
                op.url = "https://carlosedubarreto.gumroad.com/l/py_embeded_prompthmr" 



                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                if hubmocap_prop.path_prompthmr == '':
                    col.enabled = False
                else:
                    col.enabled = True
                col.label(text="Unzipping PromptHMR")
                col.prop(hubmocap_prop, "path_phmr_zip", text="Zip File")
                
                col.operator("hubmocap.async_unzip", text="Start Unzip", icon='MOD_EXPLODE')
            
                # Draw the status text
                col.label(text=scene.zip_status_msg)
                
                # Draw the progress bar
                # We use 'factor' to tell Blender this float is a percentage (0-100)
                if scene.zip_progress_val > 0.0 and scene.zip_progress_val < 100.0:
                    col.enabled = True
                    col.prop(scene, "zip_progress_val", text="Progress", slider=True)

                ####### Download PromptHMR from github
                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                col_down_github = col.column(align=True)
                if os.path.exists(os.path.join(hubmocap_prop.path_gvhmr,'PromptHMR_Portable','PromptHMR-main')):
                    col_down_github.enabled = False
                else:
                    col_down_github.enabled = True
                down_github = col_down_github.operator(download_github_generic.bl_idname, text="Downlaod Github Code")
                down_github.module = 'prompthmr'



                col.label(text="Downloading Checkpoints")
                line1_txt = col.row(align=True)
                row_ckpt = line1_txt.row(align=True)

                ### PMR1
                line1 = col.row(align=True)
                row_sp_down_dpvo = line1.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','phmr','checkpoint.ckpt')):
                    row_sp_down_dpvo.enabled = True
                else:
                    row_sp_down_dpvo.enabled = False
                subproc = row_sp_down_dpvo.operator(OPS_OT_run_subprocess.bl_idname, text="PHMR CKPT")
                subproc.module='phmr_ckpt_pmr1'

                ### PMR2
                row_sp_down_gvhmr = line1.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','phmr','config.yaml')):
                    row_sp_down_gvhmr.enabled = True
                else:
                    row_sp_down_gvhmr.enabled = False
                subproc = row_sp_down_gvhmr.operator(OPS_OT_run_subprocess.bl_idname, text="PHMR YAML")
                subproc.module='phmr_ckpt_pmr2'


                ### phmr_ckpt_pmr_vid1
                line2 = col.row(align=True)
                row_sp_down_hmr2 = line2.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','phmr_vid','prhmr_release_002.ckpt')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="PHMR VID CKPT")
                subproc.module='phmr_ckpt_pmr_vid1'

                ### phmr_ckpt_pmr_vid2
                row_sp_down_vitpose = line2.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','phmr_vid','prhmr_release_002.yaml')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="PHMR VID YAML")
                subproc.module='phmr_ckpt_pmr_vid2'


                ### phmr_ckpt_sam2_1
                line3 = col.row(align=True)
                row_sp_down_hmr2 = line3.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','sam2_ckpts','keypoint_rcnn_5ad38f.pkl')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="SAM2 PKL")
                subproc.module='phmr_ckpt_sam2_1'

                ### phmr_ckpt_sam2_2
                row_sp_down_vitpose = line3.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','sam2_ckpts','sam2_hiera_tiny.pt')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="SAM2 PT")
                subproc.module='phmr_ckpt_sam2_2'


                ### phmr_ckpt_camcalib
                line4 = col.row(align=True)
                row_sp_down_hmr2 = line4.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','camcalib_sa_biased_l2.ckpt')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="CAMCALIB")
                subproc.module='phmr_ckpt_camcalib'

                ### phmr_ckpt_droidcalib
                row_sp_down_vitpose = line4.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','droidcalib.pth')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="DROIDCALIB")
                subproc.module='phmr_ckpt_droidcalib'


                ### phmr_ckpt_vitpose
                line5 = col.row(align=True)
                row_sp_down_hmr2 = line5.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','vitpose-h-coco_25.pth')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="VITPOSE")
                subproc.module='phmr_ckpt_vitpose'

                ### phmr_ckpt_samvit
                row_sp_down_vitpose = line5.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','pretrain','sam_vit_h_4b8939.pth')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="SAM VIT")
                subproc.module='phmr_ckpt_samvit'


                ### phmr_ckpt_bm_j_regressor
                line6 = col.row(align=True)
                row_sp_down_hmr2 = line6.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models','J_regressor_h36m.npy')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="J Regressor")
                subproc.module='phmr_ckpt_bm_j_regressor'

                ### phmr_ckpt_bm_smplmean
                row_sp_down_vitpose = line6.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models','smpl_mean_params.npz')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="SMPL Mean")
                subproc.module='phmr_ckpt_bm_smplmean'

                ### phmr_ckpt_bm_smplx2smpl_joint
                line7 = col.row(align=True)
                row_sp_down_hmr2 = line7.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models','smplx2smpl_joints.npy')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="SMPLX2SMPL Joint")
                subproc.module='phmr_ckpt_bm_smplx2smpl_joint'

                ### phmr_ckpt_bm_smplx2smpl
                row_sp_down_vitpose = line7.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models', 'smplx2smpl.pkl')):
                    row_sp_down_vitpose.enabled = True
                else:
                    row_sp_down_vitpose.enabled = False
                subproc = row_sp_down_vitpose.operator(OPS_OT_run_subprocess.bl_idname, text="SMPLX2SMPL")
                subproc.module='phmr_ckpt_bm_smplx2smpl'


                ### phmr_ckpt_bm_smplx_neutral_array
                line8 = col.row(align=True)
                row_sp_down_hmr2 = line8.column(align=True)
                if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models', 'smplx','SMPLX_neutral_array_f32_slim.npz')):
                    row_sp_down_hmr2.enabled = True
                else:
                    row_sp_down_hmr2.enabled = False
                subproc = row_sp_down_hmr2.operator(OPS_OT_run_subprocess.bl_idname, text="SMPLX Neutral Array")
                subproc.module='phmr_ckpt_bm_smplx_neutral_array'


                if RUNNER.status_text.startswith("Running"):

                    col.label(text=f"Status: {RUNNER.status_text}")
                    # col.label(text=f"Task: {RUNNER.task_name or '-'}")
                    # col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

                    # Last log line
                    if RUNNER.last_log:
                        col.label(text=f"Last: {RUNNER.last_log[:100]}")


                ### Download and place the SMPL / SMPLX files
                ####### Download GVHMR from github
                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                # col.label(text="Download SMPL / SMPLX files")

                if not hubmocap_prop.SMPL_gvhmr_register and not hubmocap_prop.SMPL_and_SMPLX_download:
                    long_text1 = "You need to register to download the SMPL and SMPLX PKL file. "
                    long_text2 = "If you are not registered, choose the REGISTER button to get to the SMPL register site."
                    long_text3 = "If you have a registration, choose the DOWNLOAD button and insert your email and password to download the SMPL PKL file."
                    _label_multiline(context, long_text1, col)
                    col.separator()
                    _label_multiline(context, long_text2, col)
                    col.separator()
                    _label_multiline(context, long_text3, col)
                
                ########################################
                ## Download SMPL and SMPLX PKL for GVHMR
                row.prop(hubmocap_prop,'SMPL_gvhmr_register',text="Register", icon='WORDWRAP_ON', toggle=True)
                row.prop(hubmocap_prop,'SMPL_and_SMPLX_download',text="Download", icon='EVENT_DOWN_ARROW', toggle=True)

                if hubmocap_prop.SMPL_gvhmr_register:
                    op = layout.operator("wm.url_open", text="Register on SMPL", icon='GREASEPENCIL')
                    op.url = "https://smpl.is.tue.mpg.de/register.php"

                    op = layout.operator("wm.url_open", text="Register on SMPLX", icon='GREASEPENCIL')
                    op.url = "https://smpl-x.is.tue.mpg.de/register.php"

                if hubmocap_prop.SMPL_and_SMPLX_download:
                    # hubmocap_prop.SMPLify_email
                    # hubmocap_prop.SMPLify_password
                    row = col.row(align=True)
                    row.prop(hubmocap_prop,'SMPL_download_user_and_pass',text="SMPL", icon='EVENT_DOWN_ARROW', toggle=True)
                    row.prop(hubmocap_prop,'SMPLX_download_user_and_pass',text="SMPLX", icon='EVENT_DOWN_ARROW', toggle=True)

                    if hubmocap_prop.SMPL_download_user_and_pass or hubmocap_prop.SMPLX_download_user_and_pass:
                        col.prop(hubmocap_prop,'SMPL_email',text="Email")
                        col.prop(hubmocap_prop,'SMPL_password',text="Password")

                    if hubmocap_prop.SMPL_download_user_and_pass:

                        down_smpl = col.operator('hubmocap.async_download_post', text="Download SMPL PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=smpl&sfile=SMPL_python_v.1.1.0.zip&resume=1"
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_prompthmr,'temp','SMPL_python_v.1.1.0.zip')
                        ######################################
                        #### Setup SMPL
                        col_setup = col.column(align=True) 
                        if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'temp','SMPL_python_v.1.1.0.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl")
                        ssmpl.module_id = 'gvhmr_smpl'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_prompthmr,'temp','SMPL_python_v.1.1.0.zip')
                        ssmpl.wanted_files = json.dumps(['SMPL_python_v.1.1.0/smpl/models/basicmodel_f_lbs_10_207_0_v1.1.0.pkl',
                                                        'SMPL_python_v.1.1.0/smpl/models/basicmodel_m_lbs_10_207_0_v1.1.0.pkl',
                                                        'SMPL_python_v.1.1.0/smpl/models/basicmodel_neutral_lbs_10_207_0_v1.1.0.pkl']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_prompthmr,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models', 'smpl')

                    if hubmocap_prop.SMPLX_download_user_and_pass:
                        down_smpl = col.operator('hubmocap.async_download_post', text="Download SMPLX PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=smplx&sfile=models_smplx_v1_1.zip&resume=1"
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_prompthmr,'temp','models_smplx_v1_1.zip')

                        ######################################
                        #### Setup SMPLX
                        col_setup = col.column(align=True) 
                        if not os.path.exists(os.path.join(hubmocap_prop.path_prompthmr,'temp','models_smplx_v1_1.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl",text="Setup SMPLX")
                        ssmpl.module_id = 'gvhmr_smplx'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_prompthmr,'temp','models_smplx_v1_1.zip')
                        ssmpl.wanted_files = json.dumps(['models/smplx/SMPLX_FEMALE.npz',
                                                        'models/smplx/SMPLX_MALE.npz',
                                                        'models/smplx/SMPLX_NEUTRAL.npz']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_prompthmr,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_prompthmr,'PromptHMR_Portable','PromptHMR-main','data','body_models', 'smplx')




                    


                    # layout.separator()
        
                    # Display Status
                    layout.label(text=f"Status: {scene.dl_status}")
                    
                    # Display Progress Bar
                    col = layout.column()
                    if scene.dl_status != 'Download Complete!':
                        col.prop(scene, "dl_progress", text="Progress", slider=True)
        
        
        #####################################
        ### Options for HaMeR
        #####################################
        if hubmocap_prop.module_hamer:        
            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text="HaMeR")


            col = layout.box().column(align=True)
            row = col.row(align=True)
            col_alert = col.column(align=True)
            col_alert.prop(hubmocap_prop, "path_hamer_video_input", text="Video")
            if ' ' in hubmocap_prop.path_hamer_video_input:
                col_alert.alert = True
                col_alert.label(text=f"Video path with spaces,")
                col_alert.label(text=f" please remove them!")
            else:
                col_alert.alert = False
                file_name = os.path.basename(hubmocap_prop.path_hamer_video_input)
                col_alert.label(text=f"File: {file_name}")


            #################################################################
            ######
            # col = layout.column(align=True)

            # Status header
            col_alert = col.column(align=True)
            if RUNNER.status_text.startswith("Running"):
                col_alert.alert = True
            else:
                col_alert.alert = False
            col_alert.label(text=f"Status: {RUNNER.status_text}")
            # col.label(text=f"Task: {RUNNER.task_name or '-'}")
            # col.label(text=f"Progress: {int(RUNNER.progress * 100)}%")

            # Last log line
            if RUNNER.last_log:
                col.label(text=f"Last: {RUNNER.last_log[:100]}")
            
            # if hubmocap_prop.int_tot_character_gvhmr == -1:
            #     col.label(text='Character: it will show after first exec')
            # else:
            #     col.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_gvhmr))
            # row = col.row(align=True)
            # row.prop(hubmocap_prop, "int_character_gvhmr", text="Character")
            # row.prop(hubmocap_prop, 'int_fps_gvhmr', text='FPS')
            # Controls
            row_subproc = col.row(align=True)
            if RUNNER.status_text.startswith("Running") or not os.path.exists(hubmocap_prop.path_hamer_video_input) :
                row_subproc.enabled = False
            else:
                row_subproc.enabled = True
            # row.operator(OPS_OT_run_python_task.bl_idname, text="Run Python Task")
            subproc = row_subproc.operator(OPS_OT_run_subprocess.bl_idname, text="Run")
            subproc.module='hamer'
            ######################################


            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            # row.prop(hubmocap_prop, "int_character_hamer", text="Char HaMeR")
            col.prop(hubmocap_prop, "int_fps_hamer", text="FPS")
            col.prop(hubmocap_prop,'bool_current_video_hamer', text='Work on Current Video')
            if not hubmocap_prop.bool_current_video_hamer:
                # TODO: Colocar enum que mostra as pastas do Hamer
                col.prop(hubmocap_prop,'enum_list_hamer_folder', text='Folder')

            
            if hubmocap_prop.int_tot_hamer_frames == -1:
                col.label(text='Total Hamer Frames: ?')
                row = col.row(align=True)
                row.label(text='Total Left H: ?')
                row.label(text='Total Right H: ?')
            else:
                col.label(text='Total Hamer Frames: '+str(hubmocap_prop.int_tot_hamer_frames))
                row = col.row(align=True)
                row.label(text='Total Left H: '+str(hubmocap_prop.int_tot_hamer_lh_character))
                row.label(text='Total Right H: '+str(hubmocap_prop.int_tot_hamer_rh_character))
            row = col.row(align=True)
            row.prop(hubmocap_prop,"int_hamer_lh_character", text="Left H")
            row.prop(hubmocap_prop,"int_hamer_rh_character", text="Right H")

            
            col_get_hamer_info = col.column(align=True)
            path_hamer = hubmocap_prop.path_hamer
            path_code_hamer = os.path.join(path_hamer,'Hamer_Portable','hamer') 

            if hubmocap_prop.bool_current_video_hamer:
                video_name = os.path.splitext(os.path.basename(hubmocap_prop.path_hamer_video_input))[0]
                base_file = os.path.join(path_code_hamer,'demo_out',video_name,'result_000_00000.pkl')
                if os.path.exists(base_file):
                    col_get_hamer_info.enabled = True
                else:
                    col_get_hamer_info.enabled = False

            else:
                video_name = hubmocap_prop.enum_list_hamer_folder
                if video_name == 'NONE':
                    col_get_hamer_info.enabled = False
                else:
                    base_file = os.path.join(path_code_hamer,'demo_out',video_name,'result_000_00000.pkl')
                    if os.path.exists(base_file):
                        col_get_hamer_info.enabled = True
                    else:
                        col_get_hamer_info.enabled = False



            if hubmocap_prop.int_tot_hamer_frames == -1:
                col_get_hamer_info.alert = True
            else:
                col_get_hamer_info.alert = False
            col_get_hamer_info.operator('hubmocap.show_hamer_data')
            # col.

            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            col.label(text='Import Mocap')
            col.prop(hubmocap_prop,'enum_hamer_body', text='Body')
            if hubmocap_prop.enum_hamer_body == 'gvhmr':
                col.prop(hubmocap_prop,'enum_list_hamer_gvhmr_folder', text='Folder')
                col.prop(hubmocap_prop,"int_character_gvhmr", text="Character GVHMR")
                col.label(text='GVHM Files')
                path_gvhmr = hubmocap_prop.path_gvhmr
                video_gvhmr = hubmocap_prop.enum_list_hamer_gvhmr_folder
                path_code = os.path.join(path_gvhmr,'gvhmr','GVHMR-main')
                base_file = os.path.join(path_code,'outputs','demo',video_gvhmr)
                list_files = os.listdir(base_file)
                for lf in list_files:
                    if '.pkl' in lf:
                        col.label(text=lf)
            
            if hubmocap_prop.enum_hamer_body =='phmr':
                path_prompthmr = hubmocap_prop.path_prompthmr
                path_code_phmr = os.path.join(path_prompthmr,'PromptHMR_Portable','PromptHMR-main') 

                col.prop(hubmocap_prop,'enum_list_hamer_phmr_folder', text='Folder')
                col.label(text='Total of Character: '+str(hubmocap_prop.int_tot_character_prompthmr), icon='INFO')
                base_file = os.path.join(path_code_phmr,'results',hubmocap_prop.enum_list_hamer_phmr_folder)
                path_phmr_pkl = os.path.join(base_file,'results_world_blender.pkl')


            if hubmocap_prop.enum_hamer_body == 'no_body':
                col.label(text='No body')

            col.separator()
            col.prop(hubmocap_prop,'bool_hamer_load_new_body', text='Load new Body')
             

            import_char = col.operator('hubmocap.import_character', text="Import Hand Mocap")
            import_char.option = 3 #hamer
            
            col.label(text='Smooth Hands')
            col_armature = col.column(align=True)
            bpy.context.object
            if context.object.type == 'ARMATURE' or ( context.object.parent and context.object.parent.type == 'ARMATURE'):
                col_armature.enabled = True
            else:
                col_armature.enabled = False
            col_armature.operator('hubmocap.smooth2',text='Complete (Graph + Smooth)').option = 0
            row = col_armature.row(align=True)
            row.operator('hubmocap.smooth2',text='Only Grapth').option = 1
            row.operator('hubmocap.smooth2',text='Only Smooth').option = 2




            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            col.prop(hubmocap_prop, "module_hamer_install", text="Install Options",toggle=True)

            if hubmocap_prop.module_hamer_install:
                if hubmocap_prop.path_hamer == '':
                    col.alert = True
                else:
                    col.alert = False
                col.label(text="Path for HaMeR")
                col.prop(hubmocap_prop, "path_hamer", text="")


                ##############################################
                ###### Hamer Install Options

                ###################################
                ## Check if module is installed
                # box = layout.box()
                # col = box.column(align=True)
                # row = col.row(align=True)
                col.label(text="Get the Module")
                
                op = col.operator("wm.url_open", text="Gumroad (PAID)", icon='TAG')
                op.url = "https://carlosedubarreto.gumroad.com/l/py_embed_hamer" 

                


                box = layout.box()
                col = box.column(align=True)
                row = col.row(align=True)
                if hubmocap_prop.path_gvhmr == '':
                    col.enabled = False
                else:
                    col.enabled = True
                col.label(text="Unzipping HaMeR")
                col.prop(hubmocap_prop, "path_hamer_zip", text="Zip File")
                
                col.operator("hubmocap.async_unzip", text="Start Unzip", icon='MOD_EXPLODE')
            
                # Draw the status text
                col.label(text=scene.zip_status_msg)
                
                # Draw the progress bar
                # We use 'factor' to tell Blender this float is a percentage (0-100)
                if scene.zip_progress_val > 0.0 and scene.zip_progress_val < 100.0:
                    col.enabled = True
                    col.prop(scene, "zip_progress_val", text="Progress", slider=True)

                # ####### Download HaMeR from github
                # box = layout.box()
                # col = box.column(align=True)
                # row = col.row(align=True)

                #####################################
                ### Check if SMPL PKL exists
                path_hamer_mano_right = os.path.join(hubmocap_prop.path_hamer,'Hamer_Portable','hamer','_DATA','data','mano','MANO_RIGHT.pkl')


                chk_hamer_mano_right = os.path.exists(path_hamer_mano_right)
            

                if not chk_hamer_mano_right:
                    box = layout.box()
                    col = box.column(align=True)
                    row = col.row(align=True)
                    
                    if not hubmocap_prop.mano_register and not hubmocap_prop.mano_download:
                        long_text1 = "You need to register to download the MANO PKL file. "
                        long_text2 = "If you are not registered, choose the REGISTER button to get to the MANO register site."
                        long_text3 = "If you have a registration, choose the DOWNLOAD button and insert your email and password to download the MANO PKL file."
                        _label_multiline(context, long_text1, col)
                        col.separator()
                        _label_multiline(context, long_text2, col)
                        col.separator()
                        _label_multiline(context, long_text3, col)
                    
                    ###########################
                    ## Download MANO PKL
                    row.prop(hubmocap_prop,'mano_register',text="Register", icon='WORDWRAP_ON', toggle=True)
                    row.prop(hubmocap_prop,'mano_download',text="Download", icon='EVENT_DOWN_ARROW', toggle=True)

                    if hubmocap_prop.mano_register:
                        op = layout.operator("wm.url_open", text="Register on MANO", icon='GREASEPENCIL')
                        op.url = "https://mano.is.tue.mpg.de/register.php"

                    if hubmocap_prop.mano_download:
                        # hubmocap_prop.SMPLify_email
                        # hubmocap_prop.SMPLify_password

                        col.prop(hubmocap_prop,'SMPL_email',text="Email")
                        col.prop(hubmocap_prop,'SMPL_password',text="Password")

                        # col.operator("hubmocap.smplify_download", text="Download SMPL PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl = col.operator('hubmocap.async_download_post', text="Download MANO PKL", icon='EVENT_DOWN_ARROW')
                        down_smpl.url = "https://download.is.tue.mpg.de/download.php?domain=mano&resume=1&sfile=mano_v1_2.zip&resume=1"
                        
                        
                        down_smpl.target_path = os.path.join(hubmocap_prop.path_hamer,'temp','mano_v1_2.zip')

                        # layout.separator()
            
                        # Display Status
                        layout.label(text=f"Status: {scene.dl_status}")
                        
                        # Display Progress Bar
                        col = layout.column()
                        if scene.dl_status != 'Download Complete!':
                            col.prop(scene, "dl_progress", text="Progress", slider=True)
                        
                        col_setup = col.column(align=True) # Setup SMPL
                        if not os.path.exists(os.path.join(hubmocap_prop.path_hamer,'temp','mano_v1_2.zip')):
                            col_setup.enabled = False
                        ssmpl = col_setup.operator("hubmocap.setup_smpl")
                        ssmpl.module_id = 'hamer'
                        ssmpl.zip_path = os.path.join(hubmocap_prop.path_hamer,'temp','mano_v1_2.zip')
                        ssmpl.wanted_files = json.dumps(['mano_v1_2/models/MANO_RIGHT.pkl']) #
                        ssmpl.tmp_folder = os.path.join(hubmocap_prop.path_hamer,'temp')
                        ssmpl.extract_to = os.path.join(hubmocap_prop.path_hamer,'Hamer_Portable','hamer','_DATA','data','mano')
                else:
                    col = layout.column(align=True)
                    row = col.row(align=True)
                    row.label(text="MANO PKL file is already Installed.")


        ######################################
        #### links to web and social media
        box_web = layout.box()
        box_web.label(text="Web")
        op = box_web.operator("wm.url_open", text="Support me on Patreon", icon='FUND')
        op.url = "https://www.patreon.com/c/cebstudios"
        op = box_web.operator("wm.url_open", text="Discord", icon='INTERNET')
        op.url = "https://discord.gg/BRuu43Nv2J"
        #######################################




class CEB_HubMocapSettings(PropertyGroup):

    ##############################################
    ##### Module buttons
    module_4dhumans: BoolProperty(
        name="4DHumans",
        description="View 4DHumans options",
        default=False,
        update=updt_button_4dhumans
    ) # type: ignore
    module_gvhmr: BoolProperty(
        name="GVHMR",
        description="View GVHMR options",
        default=False,
        update=updt_button_gvhmr
    ) # type: ignore

    module_prompthmr: BoolProperty(
        name="PromptHMR",
        description="View PromptHMR options",
        default=False,
        update=updt_button_prompthmr
    ) # type: ignore

    module_hamer: BoolProperty(
        name="Hamer",
        description="View Hamer options",
        default=False,
        update=updt_button_hamer
    ) # type: ignore

    ##### Install button

    module_4dhumans_install: BoolProperty(
        name="4DHumans Install",
        description="View 4DHumans Install Controls",
        default=False,
    ) # type: ignore

    module_gvhmr_install: BoolProperty(
        name="GVHMR Install",
        description="View GVHMR Install Controls",
        default=False,
    ) # type: ignore
    ##############################################

    #######################################################
    ####### Setting Path for Module 4D Human
    #######################################################
    path_addon = os.path.dirname(os.path.abspath(__file__))
    path_venv_path_txt = os.path.join(path_addon,'venv_path_4dhumans.txt')
    env_has_path_txt = 0
    if os.path.exists(path_venv_path_txt):
        with open(path_venv_path_txt, "rt") as fin:
            for line in fin:
                env_has_path_txt = 1
                path_txt = line
            if env_has_path_txt ==0:
                path_txt = ''
    else:
        path_txt = ''

    path_4dhumans: StringProperty(
        name="4DHumans Module",
        description="Path to 4DHumans Module",
        default=path_txt,
        subtype="FILE_PATH",
        update=updt_custom_venv_name
    ) # type: ignore

    path_4dhumans_zip: StringProperty(
        name="4DHumans Zip",
        description="Path to 4DHumans Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    path_4dhumans_video_input: StringProperty(
        name="4DHumans Video Input",
        description="Path to 4DHumans Video Input",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore
    int_tot_character: IntProperty(name='Total of Characters',default=0,min=0) # type: ignore
    int_character: IntProperty(name='Character',default=1, min=1) # type: ignore


    #######################################################
    ####### Setting Path for Module GVHMR
    #######################################################
    bool_current_video_gvhmr: BoolProperty(name='Work on Current Video',default=True) # type: ignore
    int_tot_character_gvhmr: IntProperty(name='Total of Characters',default=-1) # type: ignore
    int_character_gvhmr: IntProperty(name='Character',default=1, min=1) # type: ignore
    int_fps_gvhmr: IntProperty(name='FPS',default=30) # type: ignore
    path_addon = os.path.dirname(os.path.abspath(__file__))
    path_venv_path_gvhmr_txt = os.path.join(path_addon,'venv_path_gvhmr.txt')
    env_has_path_gvhmr_txt = 0
    if os.path.exists(path_venv_path_gvhmr_txt):
        with open(path_venv_path_gvhmr_txt, "rt") as fin:
            for line in fin:
                env_has_path_gvhmr_txt = 1
                path_gvhmr_txt = line
            if env_has_path_gvhmr_txt ==0:
                path_gvhmr_txt = ''
    else:
        path_gvhmr_txt = ''

    path_gvhmr: StringProperty(
        name="GVHMR Module",
        description="Path to GVHMR Module",
        default=path_gvhmr_txt,
        subtype="FILE_PATH",
        update=updt_custom_gvhmr_venv_name
    ) # type: ignore

    path_gvhmr_zip: StringProperty(
        name="GVHMR Zip",
        description="Path to GVHMR Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    path_gvhmr_video_input: StringProperty(
        name="GVHMR Video Input",
        description="Path to GVHMR Video Input",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    path_gvhmr_prev_video_input: StringProperty(
        name="GVHMR Prev Video Input",
        description="Prev Video Input",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore #variable created to detect if a new video is selected, the process that erases the output folder will clean it
    ## This was done to be able to run multple characters withlut erasing the previous ones, since it was using the same video

    enum_list_gvhmr_folder: EnumProperty(
        name="Select a Mocap",
        description="Choose from available options",
        items= get_folder_items,
        # update=updt_tot_char_phmr
        # default='' # Optional: set a default value
    )# type: ignore

    #######################################################
    ####### Setting Path for Module PromptHMR
    #######################################################
    bool_current_video_phmr: BoolProperty(name='Work on Current Video',default=True, update= updt_tot_char_phmr) # type: ignore
    int_tot_character_prompthmr: IntProperty(name='Total of Characters',default=-1) # type: ignore #int_tot_character_gvhmr: IntProperty(name='Total of Characters',default=-1) # type: ignore
    int_character_prompthmr: IntProperty(name='Character',default=1, min=1) # type: ignore
    int_fps_prompthmr: IntProperty(name='FPS',default=30) # type: ignore
    path_addon = os.path.dirname(os.path.abspath(__file__))
    path_venv_path_prompthmr_txt = os.path.join(path_addon,'venv_path_prompthmr.txt')
    env_has_path_prompthmr_txt = 0
    if os.path.exists(path_venv_path_prompthmr_txt):
        with open(path_venv_path_prompthmr_txt, "rt") as fin:
            for line in fin:
                env_has_path_prompthmr_txt = 1
                path_prompthmr_txt = line
            if env_has_path_prompthmr_txt ==0:
                path_prompthmr_txt = ''
    else:
        path_prompthmr_txt = ''

    path_prompthmr: StringProperty(
        name="PromptHMR Module",
        description="Path to PromptHMR Module",
        default=path_prompthmr_txt,
        subtype="FILE_PATH",
        update=updt_custom_prompthmr_venv_name
    ) # type: ignore

    path_phmr_zip: StringProperty(
        name="PromptHMR Zip",
        description="Path to PromptHMR Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    path_prompthmr_video_input: StringProperty(
        name="PrmptHMR Video Input",
        description="Path to PromptHMR Video Input",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    enum_list_phmr_folder: EnumProperty(
        name="Select a Mocap",
        description="Choose from available options",
        items= get_folder_items,
        update=updt_tot_char_phmr
        # default='' # Optional: set a default value
    )# type: ignore

    module_phmr_install: BoolProperty(
        name="PromptHMR Install",
        description="View PromptHMR Install Controls",
        default=False,
    ) # type: ignore

    path_phmr_zip: StringProperty(
        name="PromptHMR Zip",
        description="Path to PromptHMR Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore


    #######################################################
    ####### Setting Path for Module HaMeR
    #######################################################
    bool_current_video_hamer: BoolProperty(name='Work on Current Video',default=True)#, update= updt_tot_char_phmr) # type: ignore
    int_tot_character_hamer: IntProperty(name='Total of Characters',default=-1) # type: ignore #int_tot_character_gvhmr: IntProperty(name='Total of Characters',default=-1) # type: ignore
    int_character_hamer: IntProperty(name='Character',default=1, min=1) # type: ignore
    int_fps_hamer: IntProperty(name='FPS',default=30) # type: ignore
    path_addon = os.path.dirname(os.path.abspath(__file__))
    path_venv_path_hamer_txt = os.path.join(path_addon,'venv_path_hamer.txt')
    env_has_path_hamer_txt = 0
    if os.path.exists(path_venv_path_hamer_txt):
        with open(path_venv_path_hamer_txt, "rt") as fin:
            for line in fin:
                env_has_path_hamer_txt = 1
                path_hamer_txt = line
            if env_has_path_hamer_txt ==0:
                path_hamer_txt = ''
    else:
        path_hamer_txt = ''

    path_hamer: StringProperty(
        name="HaMeR Module",
        description="Path to HaMeR Module",
        default=path_hamer_txt,
        subtype="FILE_PATH",
        update=updt_custom_hamer_venv_name
    ) # type: ignore

    path_hamer_zip: StringProperty(
        name="HaMeR Zip",
        description="Path to HaMeR Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    path_hamer_video_input: StringProperty(
        name="HaMeR Video Input",
        description="Path to HaMeR Video Input",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore



    enum_hamer_body: EnumProperty(
            name="Select an Option",
            description="Choose from available options",
            items= [
                    ('no_body', "No Body", "Loads only hands motion"),
                    ('gvhmr', "GVHMR", "Loads GVHMR motion with hands"),
                    ('phmr', "PromptHMR", "Loads PromptHMR motion with hands"),
                    ],
            default='no_body' # Optional: set a default value
    )# type: ignore

    bool_hamer_load_new_body: BoolProperty(
        name="Load New Body",
        description="Load a new body if true, if false laod the animation on the selected character",
        default=True,
    ) # type: ignore

    int_tot_hamer_frames: IntProperty(name='Total of Frames',default=-1) # type: ignore
    int_tot_hamer_lh_character: IntProperty(name='Total of Characters for Left Hand',default=-1) # type: ignore
    int_tot_hamer_rh_character: IntProperty(name='Total of Characters for Right Hand',default=-1) # type: ignore
    int_hamer_lh_character: IntProperty(name='Character for Left Hand',default=1, min=1) # type: ignore
    int_hamer_rh_character: IntProperty(name='Character for Right Hand',default=1, min=1) # type: ignore

    enum_list_hamer_folder: EnumProperty(
        name="Select a Mocap",
        description="Choose from available options",
        items= get_folder_items,
        # update=updt_tot_char_phmr
        # default='' # Optional: set a default value
    )# type: ignore

    enum_list_hamer_phmr_folder: EnumProperty(
        name="Select a Mocap",
        description="Choose from available options",
        items= get_folder_items_in_hamer,
        update=updt_tot_char_phmr
        # default='' # Optional: set a default value
    )# type: ignore

    enum_list_hamer_gvhmr_folder: EnumProperty(
        name="Select a Mocap",
        description="Choose from available options",
        items= get_folder_items_in_hamer,
        # update=updt_tot_char_phmr
        # default='' # Optional: set a default value
    )# type: ignore

    module_hamer_install: BoolProperty(
        name="Hamer Install",
        description="View Hamer Install Controls",
        default=False,
    ) # type: ignore

    path_hamer_zip: StringProperty(
        name="Hamer Zip",
        description="Path to Hamer Zip",
        default='',
        subtype="FILE_PATH",
    ) # type: ignore

    mano_register: BoolProperty(
        name="Register",
        description="Show register link to Mano page",
        default=False,
        update=updt_button_hamer_mano_register
    ) # type: ignore
    mano_download: BoolProperty(
        name="Download",
        description="Show email and password input to download  the Mano pkl model",
        default=False,
        update=updt_button_hamer_mano_download
    ) # type: ignore


    #########################################
    ## Buttons for the SMPLify download part
    SMPLify_register: BoolProperty(
        name="Register",
        description="Show register link to SMPLify page",
        default=False,
        update=updt_button_4dhumans_register
    ) # type: ignore
    SMPLify_download: BoolProperty(
        name="Download",
        description="Show email and password input to download  the SMPLify pkl model",
        default=False,
        update=updt_button_4dhumans_download
    ) # type: ignore

    SMPL_gvhmr_register: BoolProperty(
        name="Register",
        description="Show register link to SMPL and SMPLX page",
        default=False,
        update=updt_button_gvhmr_register
    ) # type: ignore


    SMPL_and_SMPLX_download: BoolProperty(
        name="Download",
        description="Show email and password input to download  the SMPL and SMPLX pkl model",
        default=False,
        update=updt_button_gvhmr_smpl_and_smplx_download
    ) # type: ignore

    SMPL_download_user_and_pass: BoolProperty(
        name="SMPL",
        description="Show email and password input to download  the SMPL pkl model",
        default=False,
        update=updt_button_SMPL_download_user_and_pass
    ) # type: ignore

    SMPLX_download_user_and_pass: BoolProperty(
        name="SMPLX",
        description="Show email and password input to download  SMPLX pkl model",
        default=False,
        update=updt_button_SMPLX_download_user_and_pass
    ) # type: ignore


    # TODO: Tenho que trocar o update function pois esta o que copeid do 4d humans
    # SMPL_download: BoolProperty(
    #     name="Download",
    #     description="Show email and password input to download  the SMPL pkl model",
    #     default=False,
    #     update=updt_button_4dhumans_download
    # ) # type: ignore
    # SMPLX_download: BoolProperty(
    #     name="Download",
    #     description="Show email and password input to download  the SMPLX pkl model",
    #     default=False,
    #     update=updt_button_4dhumans_download
    # ) # type: ignore

    SMPL_email: StringProperty(
        name="Email",
        description="Email",
        default="",
    ) # type: ignore
    SMPL_password: StringProperty(
        name="Password",
        description="Password",
        default="",
        subtype="PASSWORD",
    ) # type: ignore

    download_status: StringProperty(
        name="Download Status",
        description="Download Status",
        default="",
    ) # type: ignore