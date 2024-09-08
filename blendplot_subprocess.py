import os.path

import json_to_CSV
import subprocess

def create_obj(json_file_path):
    csv_path = json_to_CSV.create_csv(json_file_path)

    directory = os.path.dirname(json_file_path)
    file_name = os.path.basename(json_file_path)
    file_name, file_extension = os.path.splitext(file_name)
    file_name = file_name + '.obj'
    obj_path = os.path.join(directory, file_name)

    """to use the blendplot package in a Python script, you can utilize the subprocess module to run terminal commands from within the script. Here’s an example of how you can achieve this:"""

    # Define the command as a list
    command = ['blendplot', csv_path, obj_path, 'x', 'y', 'z']

    # Run the command
    result = subprocess.run(command)

    # Print the output and errors (if any)
    print("Output:\n", result.stdout)
    print("Errors:\n", result.stderr)




