import subprocess
import os

# Define the path to Blender executable
blender_executable = "/path/to/blender"

# Define the path to the .obj file
obj_file_path = "/path/to/your/file.obj"

# Define the path to the Blender script
blender_script_path = "/path/to/import_and_separate.py"

# Run Blender in background mode with the specified script and .obj file
subprocess.run([blender_executable, "-b", "--python", blender_script_path, "--", obj_file_path])

print("Blender script executed successfully.")
