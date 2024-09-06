import bpy
import mathutils

# Define the path to your .obj file
obj_file_path = "/Users/joseph/PycharmProjects/HTTYD-point-printer/working_files/test.obj"

# Ensure the scene is clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import the .obj file
bpy.ops.import_scene.obj(filepath=obj_file_path)

# Get the imported object (assuming it's the only selected object after import)
imported_object = bpy.context.selected_objects[0]

# Enter edit mode
bpy.context.view_layer.objects.active = imported_object
bpy.ops.object.mode_set(mode='EDIT')

# Select all geometry
bpy.ops.mesh.select_all(action='SELECT')

# Separate by loose parts
bpy.ops.mesh.separate(type='LOOSE')

# Return to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Get all separated objects
separated_objects = bpy.context.selected_objects

# Define the diameter of the spheres
sphere_diameter = 1.5

# Function to add a sphere around the center of an object
def add_sphere_around_object(obj, diameter):
    # Calculate the object's bounding box center
    obj_center = obj.location
    bbox_center = sum((mathutils.Vector(b) for b in obj.bound_box), mathutils.Vector()) / 8
    global_bbox_center = obj.matrix_world @ bbox_center

    # Add a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=diameter / 2, location=global_bbox_center)

    # Get the newly created sphere
    sphere = bpy.context.object

    # Optionally parent the sphere to the object
    # sphere.parent = obj

# Loop through each separated object and add a sphere around it
for obj in separated_objects:
    add_sphere_around_object(obj, sphere_diameter)

print("OBJ file imported, separated, and spheres added around each part.")
