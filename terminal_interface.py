# ask_name_and_file.py
import blender_subprocess
import blendplot_subprocess

import os
import shutil
from datetime import datetime
import string

def list_json_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

def main():
    # Ask for the user's name
    name = input("What is your name? ")
    print(f"Hello, {name}!")

    # Define the directory to search for .json files
    directory = "/Users/joseph"  # Updated directory

    # List all .json files in the specified directory
    json_files = list_json_files(directory)
    if not json_files:
        print("No .json files found in the directory.")
        return

    print("Which file is yours?")
    letters = string.ascii_lowercase
    for idx, file in enumerate(json_files):
        print(f"{letters[idx]}. {file}")

    # Ask the user to select a file
    while True:
        choice = input("Enter the letter corresponding to your file: ").lower()
        if choice in letters[:len(json_files)]:
            selected_file = json_files[letters.index(choice)]
            print(f"You selected: {selected_file}")
            break
        else:
            print(f"Please enter a letter between 'a' and '{letters[len(json_files) - 1]}'.")

    # Get the current time and format it
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a new filename by concatenating the selected file name with the current time
    file_name, file_extension = os.path.splitext(selected_file)
    new_file_name = f"{file_name}_{current_time}{file_extension}"

    # Create a new folder named after the user and the current time
    new_folder = os.path.join(directory, f"{name}_{current_time}")
    os.makedirs(new_folder, exist_ok=True)

    # Copy the selected file to the new folder with the new name
    source_path = os.path.join(directory, selected_file)
    destination_path = os.path.join(new_folder, new_file_name)
    shutil.copy2(source_path, destination_path)

    print(
        f"The file '{selected_file}' has been copied to the folder '{new_folder}' with the new name '{new_file_name}'.")

    #convert the file into a csv and use plend plot to greate an obj in a subprocess
    obj_path = blendplot_subprocess.create_obj(destination_path)

    blender_subprocess.render_points(obj_path)

if __name__ == "__main__":
    main()
