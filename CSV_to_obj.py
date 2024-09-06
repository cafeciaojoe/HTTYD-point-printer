import json_to_CSV
import subprocess

file_path = 'working_files/Joseph_.json'

csv_path = json_to_CSV.create_csv(file_path)
obj_path = 'working_files/test.obj'

"""to use the blendplot package in a Python script, you can utilize the subprocess module to run terminal commands from within the script. Here’s an example of how you can achieve this:"""

# Define the command as a list
command = ['blendplot', csv_path, obj_path, 'x', 'y', 'z']

# Run the command
result = subprocess.run(command)

# Print the output and errors (if any)
print("Output:\n", result.stdout)
print("Errors:\n", result.stderr)




