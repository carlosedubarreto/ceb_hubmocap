import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper,ExportHelper
from bpy.props import StringProperty,BoolProperty,IntProperty
import os
import sys
import zipfile
import threading
import time

import pickle
import shutil
import subprocess
import requests
import json


#######################################
####  Async Download Worker Thread ####

# --- 1. SHARED STATE ---
# We use this class to pass data between the Background Thread and Blender.
# NEVER write to bpy.data or bpy.context directly from the thread!
class TaskState:
    is_running = False
    progress = 0.0      # 0.0 to 1.0
    status = "Ready"    # Text message
    finished = False    # Signal to stop
    error = None        # Store error message if any

# Create a global instance
task_state = TaskState()

# --- 2. WORKER THREAD (Background) ---
def download_worker(url, payload, save_path):
    """
    This runs in the background. It performs the heavy network request.
    """
    task_state.is_running = True
    task_state.finished = False
    task_state.error = None
    task_state.progress = 0.0
    task_state.status = "Starting Request..."

    try:
        # We use POST as requested
        with requests.post(url, data=payload, stream=True) as response:
        # with requests.post(url, data=payload) as response:
            response.raise_for_status() # Check for 404/500 errors

            # Get total size
            total_len = response.headers.get('content-length')
            print(total_len)
            
            if total_len is None:
                task_state.status = "Downloading (Unknown Size)..."
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                task_state.progress = 1.0
            else:
                total_len = int(total_len)
                dl = 0
                task_state.status = "Downloading..."
                
                with open(save_path, 'wb') as f:
                    # Read in 8KB chunks
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            dl += len(chunk)
                            
                            # Update Shared State
                            task_state.progress = dl / total_len
                            # Optional: Slow down slightly for testing on fast internet
                            # time.sleep(0.001) 

        task_state.status = "Download Complete!"

    except Exception as e:
        task_state.error = str(e)
        task_state.status = "Error Occurred"
    
    finally:
        task_state.finished = True
        task_state.is_running = False

# --- 3. MODAL OPERATOR (Main Thread) ---
class WM_OT_AsyncDownload(bpy.types.Operator):
    bl_idname = "hubmocap.async_download_post"
    bl_label = "Download (Async)"

    url: StringProperty(name='Url of the file to download') # type: ignore
    target_path: StringProperty(name='Destination path') # type: ignore

    
    _timer = None

    def invoke(self, context, event):
        hubmocap_prop = context.scene.hubmocap_prop
        if task_state.is_running:
            self.report({'WARNING'}, "Download already in progress!")
            return {'CANCELLED'}

        # --- CONFIGURATION ---
        # Replace this with your actual URL and Payload
        target_url = self.url
        target_file = self.target_path
        
        # Data to send via POST
        payload = {"username": hubmocap_prop.SMPL_email,
           "password": hubmocap_prop.SMPL_password,
           }
        
        output_folder = os.path.dirname(target_file)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        
        # ---------------------

        # 1. Start the Thread
        thread = threading.Thread(target=download_worker, args=(target_url, payload, target_file))
        thread.daemon = True # Kills thread if Blender closes
        thread.start()

        # 2. Start the Timer (checks thread every 0.1s)
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'TIMER':
            # 3. Sync Thread Data to UI
            # We copy data from the 'task_state' object to the Scene properties
            context.scene.dl_progress = task_state.progress * 100 # Convert to percentage
            context.scene.dl_status = task_state.status
            
            # Force UI update
            context.area.tag_redraw()

            # 4. Check if finished
            if task_state.finished:
                if task_state.error:
                    self.report({'ERROR'}, f"Failed: {task_state.error}")
                else:
                    self.report({'INFO'}, "Download Finished Successfully!")

                # Cleanup
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}

        return {'PASS_THROUGH'}
    
#### END Async Download
#################################################


def read_pkl_data(context):
    
    hubmocap_prop = context.scene.hubmocap_prop
    path_4dhumans = hubmocap_prop.path_4dhumans

    #pegando a quantidade de characters
    base_file = os.path.join(path_4dhumans,'4dhumans','4D-Humans-main','outputs','results')
    file_converted = os.path.join(base_file,'demo_video.pkl')
    file = file_converted
    with open(file, 'rb') as handle:
        b = pickle.load(handle)
        
    num_character = 0
    for fframe, data in enumerate(b.items()):
        len_char = len(data[1]['smpl'])
        # print('len_char: ',len_char)
        if num_character < len_char:
            num_character = len_char
            # print('num_char:',num_character)
    hubmocap_prop.int_tot_character = num_character




###############################################
########## Async process to unzip a file

class ThreadState:
    progress = 0.0
    is_running = False
    finished = False
    message = ""
    error = None

# Initialize the state
thread_state = ThreadState()

def unzip_worker(zip_path, extract_to):
    """
    This function runs on a background thread.
    It updates the 'thread_state' object, NOT Blender data directly.
    """
    thread_state.is_running = True
    thread_state.finished = False
    thread_state.error = None
    thread_state.message = "Starting extraction..."
    thread_state.progress = 0.0
    
    try:
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Zip file not found: {zip_path}")

        os.makedirs(extract_to, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Get list of all files in zip
            file_list = zf.namelist()
            total_files = len(file_list)
            
            if total_files == 0:
                thread_state.progress = 1.0
                return

            # Iterate and extract one by one to calculate progress
            for i, file_name in enumerate(file_list):
                
                # Extract specific file
                zf.extract(file_name, extract_to)
                
                # Update progress (0.0 to 1.0)
                thread_state.progress = (i + 1) / total_files
                thread_state.message = f"Unzipping: {i+1}/{total_files}"
                
                # OPTIONAL: Slow down slightly just to see the progress bar 
                # if your test zip is too small. Remove this in production!
                # time.sleep(0.001) 

        thread_state.message = "Extraction Complete!"

    except Exception as e:
        thread_state.error = str(e)
        thread_state.message = "Error occurred."
        
    finally:
        thread_state.is_running = False
        thread_state.finished = True


class OT_AsyncUnzip(bpy.types.Operator):
    bl_idname = "hubmocap.async_unzip"
    bl_label = "Unzip File Async"

    _timer = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            # 1. SYNC: Read the thread state and update Blender UI properties
            # This runs on the main thread, so it is safe to touch bpy.data
            context.scene.zip_progress_val = thread_state.progress * 100
            context.scene.zip_status_msg = thread_state.message
            
            # Force UI redraw so the bar moves
            context.area.tag_redraw()

            # 2. CHECK: Is the thread done?
            if thread_state.finished:
                if thread_state.error:
                    self.report({'ERROR'}, thread_state.error)
                else:
                    self.report({'INFO'}, "Unzip Finished Successfully")
                
                # Clean up timer and finish
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        # Define paths
        hubmocap_prop = context.scene.hubmocap_prop
        
        # base_path = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else "/tmp"
        # zip_file = os.path.join(base_path, "test.zip")
        # output_dir = os.path.join(base_path, "unzipped_content")

        zip_file = hubmocap_prop.path_4dhumans_zip
        output_dir = hubmocap_prop.path_4dhumans

        # Reset state
        context.scene.zip_progress_val = 0.0
        
        # Start the thread
        # We use daemon=True so the thread dies if Blender closes
        t = threading.Thread(target=unzip_worker, args=(zip_file, output_dir), daemon=True)
        t.start()

        # Start the timer to watch the thread
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}
#### END Azync unzip
###################################################


class module_4dhumans_Execute(Operator):
    bl_idname = "hubmocap.4dhumans_execute"
    bl_label = "Execute 4D Human"
    bl_description = "Execute 4D Human"

    def execute(self,context):
        # path_addon = os.path.dirname(os.path.abspath(__file__))
        hubmocap_prop = context.scene.hubmocap_prop
        path_4dhumans = hubmocap_prop.path_4dhumans
        path_4dhumans_code = os.path.join(path_4dhumans,'4dhumans','4D-Humans-main')

        
        ### Trecho para copiar o arquivo de video 
        video = hubmocap_prop.path_4dhumans_video_input
        ### limpar pasta destino e copiar o caminho acima pra la
        video_destination = os.path.join(path_4dhumans_code,'example_data','videos')
        
        if os.path.exists(video_destination):
            shutil.rmtree(video_destination)
            os.makedirs(video_destination)
        else:
            os.makedirs(video_destination)

        # src = self.filepath
        src = video
        dst = os.path.join(video_destination,'video.mp4')

        shutil.copyfile(src,dst)
        
        
        
        output_folder = os.path.join(path_4dhumans_code,'outputs')

        
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
            os.makedirs(output_folder, exist_ok=True)
        else:
            os.makedirs(output_folder, exist_ok=True)

        path_folder = path_4dhumans_code
        current_folder = os.getcwd()
        os.chdir(path_folder)

        run = '../python_embedded/python track.py video.source="example_data/videos/video.mp4"'
        
        print('run: ',run)
        # subprocess.run(run) #Executa 
        os.chdir(current_folder)

        read_pkl_data(context)

        # fourd_prop.str_pklpath = ''

        return{'FINISHED'}


########################################
### Setup SMPLs files
class setup_smpl(Operator):
    bl_idname = "hubmocap.setup_smpl"
    bl_label = "Setup SMPL"
    bl_description = "Setup SMPL"

    module_id: StringProperty(name='Id for module to configure')# type: ignore # '4dhumans', 
    zip_path: StringProperty(name='Source zip file') # type: ignore
    wanted_files: StringProperty(name='File to extract') # type: ignore #List of names
    tmp_folder: StringProperty(name='Temporary folder') # type: ignore
    extract_to: StringProperty(name='Destination folder') # type: ignore

    def execute(self,context):
        hubmocap_prop = context.scene.hubmocap_prop

        if self.module_id=='4dhumans':
            zip_path = self.zip_path
            tmp_folder = self.tmp_folder
            extract_to = self.extract_to

            wanted_files = json.loads(self.wanted_files)

            shutil.unpack_archive(zip_path, tmp_folder)
            print("Unzip Done!")

            for file in wanted_files:
                shutil.move(os.path.join(tmp_folder,file),extract_to)

            shutil.rmtree(tmp_folder)
            print("Move Done!")

        return{'FINISHED'}
#######################################



    

##############################################
##### Async Execution of Subprocess
import queue
# Shared state for background execution and UI
class BackgroundRunner:
    def __init__(self):
        self.thread = None
        self.queue = queue.Queue()
        self.running = False
        self.cancel_requested = False
        self.timer_registered = False

        # Progress/Status fields for UI
        self.progress = 0.0         # 0.0..1.0
        self.status_text = "Idle"
        self.last_log = ""
        self.task_name = ""
        self._needs_redraw = False   # signal to redraw UI

    def _reset_ui(self):
        self.progress = 0.0
        self.status_text = "Idle"
        self.last_log = ""
        self.task_name = ""
        self._flag_redraw()

    def _flag_redraw(self):
        self._needs_redraw = True

    def _redraw_all_areas(self):
        # Safe to call from timer (main thread)
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            if not screen:
                continue
            for area in screen.areas:
                # Redraw all areas; panel is in VIEW_3D
                area.tag_redraw()
        self._needs_redraw = False

    # ---------- Python task runner ----------

    def start_python_task(self, func, *args, **kwargs):
        if self.running:
            print("Task already running.")
            return
        self.running = True
        self.cancel_requested = False
        self.task_name = func.__name__
        self.status_text = f"Running: {self.task_name}"
        self.progress = 0.0
        self._flag_redraw()

        def _run():
            try:
                func(self, *args, **kwargs)
            except Exception as e:
                self.queue.put(("error", f"Error: {e}"))
            finally:
                self.queue.put(("done", "Task finished."))
                self.running = False

        self.thread = threading.Thread(target=_run, daemon=True)
        self.thread.start()
        self._ensure_timer()

    # ---------- Subprocess runner ----------

    def start_subprocess(self, path, cmd):
        if self.running:
            print("Task already running.")
            return
        self.running = True
        self.cancel_requested = False
        self.task_name = "subprocess"
        # self.status_text = f"Running: {cmd}"
        self.status_text = "Running..."
        self.progress = 0.0
        self._flag_redraw()

        def _run():
            proc = None
            try:
                current_folder = os.getcwd()
                os.chdir(path)
                print('inside suproc: ',os.getcwd())
                print('cmd: ',cmd)
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                os.chdir(current_folder)
                # No fixed length: show activity and fake a spinner/progress pulse
                pulse = 0.0
                for line in proc.stdout:
                    if self.cancel_requested:
                        break
                    self.queue.put(("log", line.rstrip()))
                    # Pulse progress to show activity
                    pulse = (pulse + 0.05) % 1.0
                    self.queue.put(("progress", pulse))
                proc.wait()
                if self.cancel_requested and proc and proc.poll() is None:
                    proc.terminate()
                    self.queue.put(("log", "Process terminated by user."))
            except Exception as e:
                self.queue.put(("error", f"Subprocess error: {e}, command {cmd}, path {os.getcwd()}"))
            finally:
                self.queue.put(("done", "Subprocess finished."))
                self.running = False

        self.thread = threading.Thread(target=_run, daemon=True)
        self.thread.start()
        self._ensure_timer()

    # ---------- Control ----------

    def cancel(self):
        if self.running:
            self.cancel_requested = True
            self.queue.put(("log", "Cancel requested..."))
            self.status_text = "Canceling..."
            self._flag_redraw()

    def _ensure_timer(self):
        if not self.timer_registered:
            bpy.app.timers.register(self._timer_callback, first_interval=0.1)
            self.timer_registered = True

    def _timer_callback(self):
        # Pump messages from background to main thread
        pumped = False
        while True:
            try:
                kind, msg = self.queue.get_nowait()
            except queue.Empty:
                break
            pumped = True
            if kind == "log":
                self.last_log = msg
                print(msg)
                self._flag_redraw()
            elif kind == "error":
                self.last_log = msg
                print(msg)
                self.status_text = "Error"
                self._flag_redraw()
            elif kind == "progress":
                # msg expected as float 0..1
                try:
                    self.progress = max(0.0, min(1.0, float(msg)))
                except:
                    pass
                self._flag_redraw()
            elif kind == "done":
                self.last_log = msg
                print(msg)
                self.status_text = "Done"
                self.progress = 1.0
                self._flag_redraw()

        # Trigger UI redraw if needed
        if self._needs_redraw:
            self._redraw_all_areas()

        # Keep timer alive while running or messages still arriving
        if self.running or pumped:
            return 0.1
        else:
            # No longer running and queue drained; stop timer and reset UI state
            self.timer_registered = False
            return None


RUNNER = BackgroundRunner()


# Example long Python task (non-blocking) with real progress updates
def example_long_task(runner: BackgroundRunner, steps=30, delay=0.15):
    for i in range(1, steps + 1):
        if runner.cancel_requested:
            runner.queue.put(("log", "Canceled mid-task."))
            return
        # Simulate work
        time.sleep(delay)
        # Send progress and a short log line
        progress = i / steps
        runner.queue.put(("progress", progress))
        runner.queue.put(("log", f"Python task progress: {i}/{steps}"))
    # Schedule a safe Blender data update on main thread via timer
    def update_scene():
        cube = bpy.data.objects.get("Cube")
        if cube:
            cube.location.x += 0.1
            print("Moved Cube.x by +0.1")
        return None
    bpy.app.timers.register(update_scene)


class OPS_OT_run_python_task(bpy.types.Operator):
    bl_idname = "ops.run_python_task_nonblocking"
    bl_label = "Run Python Task (Non-Blocking)"
    bl_description = "Run a long Python task in background and stream output"

    steps: bpy.props.IntProperty(name="Steps", default=30, min=1, max=1000) # type: ignore
    delay: bpy.props.FloatProperty(name="Delay (s)", default=0.15, min=0.01, max=10.0) # type: ignore

    def execute(self, context):
        RUNNER.start_python_task(example_long_task, steps=self.steps, delay=self.delay)
        self.report({'INFO'}, "Started Python task in background.")
        return {'FINISHED'}


class OPS_OT_run_subprocess(bpy.types.Operator):
    bl_idname = "ops.run_subprocess_nonblocking"
    bl_label = "Run Subprocess (Non-Blocking)"
    bl_description = "Run an external command in background and stream output"

    module: bpy.props.StringProperty(
        name="Module",
        default="4dhumans",
        description="Mocap module to run"
    ) # type: ignore # '4dhumans', 'gvhmr'

    def execute(self, context):
        if self.module == '4dhumans':
            hubmocap_prop = context.scene.hubmocap_prop
            path_4dhumans = hubmocap_prop.path_4dhumans
            path_4dhumans_code = os.path.join(path_4dhumans,'4dhumans','4D-Humans-main')
           
            ### Trecho para copiar o arquivo de video 
            video = hubmocap_prop.path_4dhumans_video_input
            ### limpar pasta destino e copiar o caminho acima pra la
            video_destination = os.path.join(path_4dhumans_code,'example_data','videos')
            
            if os.path.exists(video_destination):
                shutil.rmtree(video_destination)
                os.makedirs(video_destination)
            else:
                os.makedirs(video_destination)

            # src = self.filepath
            src = video
            dst = os.path.join(video_destination,'video.mp4')
            shutil.copyfile(src,dst)
            output_folder = os.path.join(path_4dhumans_code,'outputs')
            
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
                os.makedirs(output_folder, exist_ok=True)
            else:
                os.makedirs(output_folder, exist_ok=True)


            ###### Clean the character number forcing the person to click the update button
            hubmocap_prop.int_tot_character = 0 ## its negative to use with a parameter on the panel to hide the number

            # os.chdir(path_4dhumans_code)
            command = '../python_embedded/python.exe track.py video.source="example_data/videos/video.mp4"'




        cmd_list = command.split()
        RUNNER.start_subprocess(path_4dhumans_code,cmd_list)
        # os.chdir(current_folder)
        self.report({'INFO'}, "Started subprocess in background.")
        return {'FINISHED'}


class OPS_OT_cancel_task(bpy.types.Operator):
    bl_idname = "ops.cancel_nonblocking_task"
    bl_label = "Cancel Background Task"
    bl_description = "Request cancellation of the running background task"

    def execute(self, context):
        RUNNER.cancel()
        self.report({'INFO'}, "Cancel requested.")
        return {'FINISHED'}
    
class OPS_OT_update_char_number(bpy.types.Operator):
    bl_idname = "hubmocap.updt_char_number"
    bl_label = "Update character number"
    bl_description = "Update character number"

    def execute(self, context):
        read_pkl_data(context)
        
        return {'FINISHED'}


class ImportCharacter(Operator):
    bl_idname = "hubmocap.import_character"
    bl_label = "Import character"
    bl_description = "Import character"
    bl_options = {'UNDO'}

    option: IntProperty(name='Option',default=0) # type: ignore 

    def execute(self,context):

        # from bpy import context

        import os
        # import sys
        # from os.path import join
        import math
        import numpy as np
        from mathutils import Matrix, Vector, Quaternion, Euler
        import json
        import pickle

        hubmocap_prop = context.scene.hubmocap_prop
        path_4dhumans = hubmocap_prop.path_4dhumans
        
        base_file = os.path.join(path_4dhumans,'4dhumans','4D-Humans-main','outputs','results')
        file = os.path.join(base_file,'demo_video.pkl')
       
        with open(file, 'rb') as handle:
            results = pickle.load(handle)

        smpl_model = 'basicModel_m_lbs_10_207_0_v1.0.2.fbx'

        #starts at 0
        character = hubmocap_prop.int_character-1


        part_match_custom_less2 = {'root': 'root', 'bone_00':  'Pelvis', 'bone_01':  'L_Hip', 'bone_02':  'R_Hip', 
                            'bone_03':  'Spine1', 'bone_04':  'L_Knee', 'bone_05':  'R_Knee', 'bone_06':  'Spine2', 
                            'bone_07':  'L_Ankle', 'bone_08':  'R_Ankle', 'bone_09':  'Spine3', 'bone_10':  'L_Foot', 
                            'bone_11':  'R_Foot', 'bone_12':  'Neck', 'bone_13':  'L_Collar', 'bone_14':  'R_Collar', 
                            'bone_15':  'Head', 'bone_16':  'L_Shoulder', 'bone_17':  'R_Shoulder', 'bone_18':  'L_Elbow', 
                            'bone_19':  'R_Elbow', 'bone_20':  'L_Wrist', 'bone_21':  'R_Wrist',
                            'bone_22':  'L_Hand', 'bone_23':  'R_Hand',
                            
                            }
        gender = 'n'


        def rodrigues2bshapes(body_pose):
            mat_rots = body_pose
            bshapes = np.concatenate([(mat_rot - np.eye(3)).ravel()
                                    for mat_rot in mat_rots[1:]])
            return(mat_rots, bshapes)

        # apply trans pose and shape to character
        def apply_trans_pose_shape(trans, body_pose, shape, ob, arm_ob, obname, scene, cam_ob, frame=None):

            # transform pose into rotation matrices (for pose) and pose blendshapes
            mrots, bsh = rodrigues2bshapes(body_pose)

            part_bones  = part_match_custom_less2
            trans = Vector((trans[0],trans[1]-2.2,0)) # o -2 é para tentar colocar o personagem no chao ao inves de ficar sob o chao
            # if fourd_prop.bool_fix_z:
            #     trans = Vector((trans[0],trans[1]-2.2,0)) # o -2 é para tentar colocar o personagem no chao ao inves de ficar sob o chao
            # else:
            #     trans = Vector((trans[0],trans[1]-2.2,trans[2]))
            arm_ob.pose.bones['m_avg_Pelvis'].location = trans
            arm_ob.pose.bones['m_avg_Pelvis'].keyframe_insert('location', frame=frame)
            
            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.w = 0.0
            arm_ob.pose.bones['m_avg_root'].rotation_quaternion.x = -1.0

            for ibone, mrot in enumerate(mrots):
                bone = arm_ob.pose.bones[obname+'_'+part_bones['bone_%02d' % ibone]]
                bone.rotation_quaternion = Matrix(mrot).to_quaternion()
                if frame is not None:
                    bone.keyframe_insert('rotation_quaternion', frame=frame)

            # apply shape blendshapes
            for ibshape, shape_elem in enumerate(shape):
                ob.data.shape_keys.key_blocks['Shape%03d' % ibshape].value = shape_elem
                if frame is not None:
                    ob.data.shape_keys.key_blocks['Shape%03d' % ibshape].keyframe_insert(
                        'value', index=-1, frame=frame)
        import os
        def init_scene(scene, params, gender='male', angle=0):

            path_addon = os.path.dirname(os.path.abspath(__file__))
            print('path:',path_addon)

            path_fbx = os.path.join(path_addon,smpl_model)
            bpy.ops.import_scene.fbx(filepath=path_fbx, axis_forward='-Y', axis_up='-Z', global_scale=100)

            obj_gender = 'm'
            obname = '%s_avg' % obj_gender
            ob = bpy.data.objects[obname]
            arm_obj = 'Armature'

            print('success load')
            
            # ob.data.use_auto_smooth = False  # autosmooth creates artifacts
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_all(action='DESELECT')
            cam_ob = ''
            ob.data.shape_keys.animation_data_clear()
            arm_ob = bpy.data.objects[arm_obj]
            arm_ob.animation_data_clear()
            
            return(ob, obname, arm_ob, cam_ob)





        ## Inicio da parte que roda
        # import joblib


        # results = joblib.load(file)
        params = []
        object_name = 'm_avg'
        obj_gender = 'm'
        scene = bpy.data.scenes['Scene']
        ob, obname, arm_ob, cam_ob= init_scene(scene, params, obj_gender)

        obj = bpy.context.window.scene.objects[object_name]
        bpy.context.view_layer.objects.active = ob

        obs = []
        for ob in bpy.context.scene.objects:
            if ob.type == 'ARMATURE':
                obs.append(ob)
        # armature = obs[len(obs)-1].name

        obs[len(obs)-1].select_set(True)
        view_layer = bpy.context.view_layer
        # Armature_obj = obs[len(obs)-1]
        view_layer.objects.active = arm_ob

        for fframe, data in enumerate(results.items()):
            # print('characters_index max:',len(data[1]['smpl'])-1)
            if character <= len(data[1]['smpl'])-1:
                scene.frame_set(fframe)
                # trans = [0.0, 0.0, 1.521]
                trans = data[1]['camera'][character]
                shape = data[1]['smpl'][character]['betas']
                global_orient = data[1]['smpl'][character]['global_orient']
                body_pose = data[1]['smpl'][character]['body_pose']
                final_body_pose = np.vstack([global_orient, body_pose])
                apply_trans_pose_shape(Vector(trans), final_body_pose, shape, obj,arm_ob, obname, scene, cam_ob, fframe)
                bpy.context.view_layer.update()
            else:
                print('skipping to the next')
            

        print('antes_arm_ob: ',arm_ob.name)
        print('antes_obj: ',obj.name)
        arm_ob.name = 'Finalized_Armature'
        obj.name='Finalized_Mesh'
        print('Depois_arm_ob: ',arm_ob.name)
        print('Depois_obj: ',obj.name)

        bpy.context.scene.frame_end = fframe




        #Criando copia para usar de referencia, a fazer bake para poder colocar na orientacao correta
        
        bpy.ops.object.duplicate(linked=False)
        armature_ref = bpy.context.selected_objects[0]
        armature_ref.name = 'TEMP_Armature_CH'+str(hubmocap_prop.int_character).zfill(2)


        #colocando o bone root na forma correta 
        
        
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.w = 1.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.x = 0.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.y = 0.0
        arm_ob.pose.bones['m_avg_root'].rotation_quaternion.z = 0.0


        arm_ob.pose.bones['m_avg_Pelvis'].constraints.new('COPY_LOCATION')
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Location"].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[0].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[0].subtarget = "m_avg_Pelvis"
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Location"].subtarget = "m_avg_Pelvis"

        
        arm_ob.pose.bones['m_avg_Pelvis'].constraints.new('COPY_ROTATION')
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Rotation"].target = armature_ref
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[1].target = armature_ref
        # arm_ob.pose.bones["m_avg_Pelvis"].constraints["Copy Rotation"].subtarget = "m_avg_Pelvis"
        arm_ob.pose.bones["m_avg_Pelvis"].constraints[1].subtarget = "m_avg_Pelvis"



        #bake
        # if bpy.context.active_object.mode != 'POSE':
        #     bpy.ops.object.mode_set(mode='POSE')
        # bpy.ops.pose.select_all(action='DESELECT') #clear

        # arm_ob.pose.bones['m_avg_Pelvis'].bone.select = True


        bpy.ops.object.select_all(action='DESELECT')
        arm_ob.select_set(True)


        start_frame = 0
        end_frame = context.scene.frame_end
        bpy.ops.nla.bake(frame_start=start_frame, frame_end=end_frame, 
                            only_selected=False, visual_keying=True, clear_constraints=True, 
                            clear_parents=False, use_current_action=True, clean_curves=False, bake_types={'POSE'})

        # bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        armature_ref.select_set(True)
        #remove a acao, que vai estar de cabexa pra baixo
        bpy.data.actions.remove(armature_ref.animation_data.action)
        bpy.ops.object.delete()

        
        arm_ob.select_set(True)
        bpy.context.view_layer.objects.active = arm_ob

        


        return{'FINISHED'}