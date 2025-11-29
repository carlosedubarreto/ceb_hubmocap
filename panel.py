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

def updt_button_gvhmr(self,context):
    hubmocap_prop = context.scene.hubmocap_prop
    if self.module_gvhmr:
        hubmocap_prop.module_4dhumans = False
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
            if hubmocap_prop.path_4dhumans == '':
                col.alert = True
            else:
                col.alert = False
            col.label(text="Path for 4DHumans")
            col.prop(hubmocap_prop, "path_4dhumans", text="")


            ###################################
            ## Check if module is installed
            # box = layout.box()
            # col = box.column(align=True)
            # row = col.row(align=True)
            col.prop(hubmocap_prop, "module_4dhumans_install", text="Install Options",toggle=True)

            if hubmocap_prop.module_4dhumans_install:
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


            col = layout.box().column(align=True)
            row = col.row(align=True)
            # col.label(text="4DHumans")
            col.prop(hubmocap_prop, "path_gvhmr_video_input", text="Video")

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
            
            if hubmocap_prop.int_tot_character_gvhmr == -1:
                col.label(text='Character: it will show after first exec')
            else:
                col.label(text=f'Characters : '+str(hubmocap_prop.int_tot_character_gvhmr))
            row = col.row(align=True)
            row.prop(hubmocap_prop, "int_character_gvhmr", text="Character")
            row.prop(hubmocap_prop, 'int_fps_gvhmr', text='FPS')
            # Controls
            row_subproc = col.row(align=True)
            if RUNNER.status_text.startswith("Running") or not os.path.exists(hubmocap_prop.path_gvhmr_video_input) :
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
            # if os.path.exists(file_converted):
            #     col.enabled = True
            # else:
            #     col.enabled = False
            # if hubmocap_prop.int_tot_character ==0:
            #     row.label(text='Click "Update" -->')
            # else:
            #     row.label(text='Characters : '+str(hubmocap_prop.int_tot_character))
            # col.prop(hubmocap_prop, "int_character", text="Character")
            int_char = hubmocap_prop.int_character_gvhmr
            path_import_pkl = os.path.join(hubmocap_prop.path_gvhmr,'gvhmr','GVHMR-main','outputs','demo','video','hmr4d_results.pt'+'_person-'+str(int_char)+".pkl")
            if os.path.exists(path_import_pkl):
                col.enabled = True
            else:
                col.enabled = False
            import_char = col.operator('hubmocap.import_character', text="Import Mocap")
            import_char.option = 1 #gvhmr



            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            if hubmocap_prop.path_gvhmr == '':
                col.alert = True
            else:
                col.alert = False
            col.label(text="Path for GVHMR")
            col.prop(hubmocap_prop, "path_gvhmr", text="")


            ###################################
            ## Check if module is installed
            # box = layout.box()
            # col = box.column(align=True)
            # row = col.row(align=True)
            col.prop(hubmocap_prop, "module_gvhmr_install", text="Install Options",toggle=True)

            if hubmocap_prop.module_gvhmr_install:
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