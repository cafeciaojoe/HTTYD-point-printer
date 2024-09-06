import bpy

# Function to import .obj file
def import_obj(file_path):
    # Import the .obj file
    bpy.ops.import_scene.obj(filepath=file_path)

# Your existing script starts here
def main():
    # Perform some initial operations
    print("Starting script...")

    # Path to your .obj file
    file_path = "/path/to/your/file.obj"

    # Import the .obj file
    import_obj(file_path)

    # Continue with other operations after importing
    print("Imported .obj file successfully.")

    # Example: Setting the location of the imported object
    for obj in bpy.context.selected_objects:
        obj.location = (0, 0, 0)

    # Example: Save the Blender file after importing and modifying
    output_file_path = "/path/to/save/your/file.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_file_path)
    print("Saved Blender file.")

# Execute the main function
if __name__ == "__main__":
    main()