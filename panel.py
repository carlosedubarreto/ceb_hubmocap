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
        # row.prop(hubmocap_prop, "module_gvhmr", text="GVHMR", toggle=True)


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






            

            ## TODO: Adicionar checagem para verificar se falta instalar o 4DHumans (se ja tiver instalado, esconder)
            


        #####################################
        ### Options for GVHMR
        #####################################

        if hubmocap_prop.module_gvhmr:        
            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text="GVHMR")


        
        
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