import subprocess
import os

def render_points(obj_path):
    # Define the path to Blender executable
    blender_executable = "/Applications/Blender.app/Contents/MacOS/Blender"

    # Define the path to the Blender script
    current_directory = os.getcwd()
    blender_script_path = os.path.join(current_directory,"obj_to_render.py")

    # Run Blender in background mode with the specified script and .obj file
    subprocess.run([blender_executable, "-b", "--python", blender_script_path, "--", obj_path])

    print("Blender script executed successfully.")

    return
