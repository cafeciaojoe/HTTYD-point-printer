# ask_name_and_file.py

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

    # Create a new folder named after the user and the current time
    new_folder = os.path.join(directory, f"{name}_{current_time}")
    os.makedirs(new_folder, exist_ok=True)

    # Copy the selected file to the new folder
    source_path = os.path.join(directory, selected_file)
    destination_path = os.path.join(new_folder, selected_file)
    shutil.copy2(source_path, destination_path)

    print(f"The file '{selected_file}' has been copied to the folder '{new_folder}'.")

    # Ask if the user wants to delete the original file
    delete_original = input("Do you want to delete the original file? (yes/no): ").strip().lower()
    if delete_original in ['yes', 'y']:
        os.remove(source_path)
        print(f"The original file '{selected_file}' has been deleted.")
    else:
        print("The original file has not been deleted.")

#convert the file into a csv






if __name__ == "__main__":
    main()
