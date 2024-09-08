import bpy
import math
import mathutils
import os
import sys

"""
This script needs to be run in Blender, either as a subprocess in an existing script,
from the command line, or in the "Scripting" tab.
"""

args = sys.argv[sys.argv.index("--") + 1:]
print(args)

# Define the path to your .obj file
obj_file_path = args[0]

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

# Create a new material for the spheres
sphere_material = bpy.data.materials.new(name="SphereMaterial")
sphere_material.use_nodes = True
nodes = sphere_material.node_tree.nodes
links = sphere_material.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add Principled BSDF node
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = 0, 0

# Add Material Output node
material_output = nodes.new(type='ShaderNodeOutputMaterial')
material_output.location = 200, 0

# Link nodes
links.new(bsdf.outputs['BSDF'], material_output.inputs['Surface'])

# Function to add a sphere around the center of an object
def add_sphere_around_object(obj, diameter):
    # Calculate the object's bounding box center
    bbox_center = sum((mathutils.Vector(b) for b in obj.bound_box), mathutils.Vector()) / 8
    global_bbox_center = obj.matrix_world @ bbox_center

    # Add a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=diameter / 2, location=global_bbox_center)

    # Get the newly created sphere
    sphere = bpy.context.object

    # Assign the material to the sphere
    if sphere.data.materials:
        sphere.data.materials[0] = sphere_material
    else:
        sphere.data.materials.append(sphere_material)

for obj in separated_objects:
    add_sphere_around_object(obj, sphere_diameter)

# Enable transparency in render settings
bpy.context.scene.render.film_transparent = True

# Add a basic light to the scene
bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))

# Enable Freestyle for outlines
bpy.context.scene.render.use_freestyle = True

# Get the first view layer
view_layer = bpy.context.scene.view_layers[0]

# Create a new line set for Freestyle
lineset = view_layer.freestyle_settings.linesets.new(name="LineSet")
lineset.select_silhouette = True
lineset.select_border = True
lineset.select_crease = True
lineset.select_edge_mark = True

# Merge all objects into a single object
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
bpy.ops.object.join()

# Calculate the bounding box of the entire merged model
merged_object = bpy.context.active_object
min_x, min_y, min_z = (float('inf'),) * 3
max_x, max_y, max_z = (float('-inf'),) * 3

for vert in merged_object.bound_box:
    v_world = merged_object.matrix_world @ mathutils.Vector(vert)
    min_x = min(min_x, v_world.x)
    min_y = min(min_y, v_world.y)
    min_z = min(min_z, v_world.z)
    max_x = max(max_x, v_world.x)
    max_y = max(max_y, v_world.y)
    max_z = max(max_z, v_world.z)

# Calculate the center and size of the bounding box
center = mathutils.Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2))
#center = mathutils.Vector((0,0,0))
size = mathutils.Vector((max_x - min_x, max_y - min_y, max_z - min_z))

# Print bounding box information for debugging
print(f"Bounding Box Min: ({min_x}, {min_y}, {min_z})")
print(f"Bounding Box Max: ({max_x}, {max_y}, {max_z})")
print(f"Bounding Box Center: {center}")
print(f"Bounding Box Size: {size}")

# Add a grid below the model
grid_size_x = max_x - min_x
grid_size_y = max_y - min_y
grid_location = (center.x, center.y, min_z - 0.01)
print(f"Grid Size: ({grid_size_x}, {grid_size_y}), Grid Location: {grid_location}")

# Create the grid
bpy.ops.mesh.primitive_plane_add(size=1, location=grid_location)
grid = bpy.context.object
grid.scale = (20, 20, 1)
#grid.scale = (grid_size_x / 2, grid_size_y / 2, 1)

# Add a material to the grid to make it more visible
grid_material = bpy.data.materials.new(name="GridMaterial")
grid_material.use_nodes = True
grid_nodes = grid_material.node_tree.nodes
grid_links = grid_material.node_tree.links

# Clear default nodes
for node in grid_nodes:
    grid_nodes.remove(node)

# Add Principled BSDF node
grid_bsdf = grid_nodes.new(type='ShaderNodeBsdfPrincipled')
grid_bsdf.location = 0, 0
grid_bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)  # Light gray

# Add Material Output node
grid_material_output = grid_nodes.new(type='ShaderNodeOutputMaterial')
grid_material_output.location = 200, 0

# Link nodes
grid_links.new(grid_bsdf.outputs['BSDF'], grid_material_output.inputs['Surface'])

# Assign the material to the grid
grid.data.materials.append(grid_material)

# Function to set up the camera and render the scene
def render_view(view_name, camera_location, camera_rotation, output_directory, distance_factor=5):
    # Calculate the distance based on the bounding box size
    distance = max(size) * distance_factor

    # Adjust the camera location based on the distance
    adjusted_camera_location = center + mathutils.Vector(camera_location).normalized() * distance

    # Print camera location for debugging
    print(f"Rendering {view_name} with camera location: {adjusted_camera_location}")

    # Create a new camera
    bpy.ops.object.camera_add(location=adjusted_camera_location, rotation=camera_rotation)
    camera = bpy.context.object
    bpy.context.scene.camera = camera

    # Optional: Adjust camera field of view (FOV)
    # camera.data.lens = 50  # Default is 50mm, adjust as necessary

    # Set render resolution and file format
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'  # Ensure alpha channel is used

    # Define the output file path
    output_file_path = os.path.join(output_directory, view_name + ".png")
    bpy.context.scene.render.filepath = output_file_path

    # Render the scene
    bpy.ops.render.render(write_still=True)

    # Delete the camera after rendering
    bpy.data.objects.remove(camera, do_unlink=True)

# Define camera locations and rotations for each view
views = [
    ("front_view", (0, -1, 0), (math.radians(90), 0, 0)),
    ("back_view", (0, 1, 0), (math.radians(-90), math.radians(180), 0)),
    ("Lside_view", (1, 0, 0), (math.radians(90), 0, math.radians(90))),
    ("Rside_view", (-1, 0, 0), (math.radians(90), 0, math.radians(-90))),
    ("top_view", (0, 0, 1), (0, 0, 0)),
    ("isometric_view", (1, -1, 1), (math.radians(55), 0, math.radians(45)))
]

# Specify the output directory explicitly
output_directory = "/Users/joseph/PycharmProjects/HTTYD-point-printer/working_files/rendered_views"

# Make sure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Render each view
for view_name, camera_location, camera_rotation in views:
    render_view(view_name, camera_location, camera_rotation, output_directory)

print("OBJ file imported, separated, spheres added, grid added, and views rendered.")
