import bpy
import math
import mathutils
import os
import sys
import csv

"""
This script needs to be run in Blender, either as a subprocess in an existing script,
from the command line, or in the "Scripting" tab.
"""

args = sys.argv[sys.argv.index("--") + 1:]
print(args)

# Define the path to your .csv file
csv_file_path = args[0]

# Ensure the scene is clear
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Define the diameter of the spheres
sphere_diameter = .3

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

# Function to add a sphere at a given location
def add_sphere_at_location(location, diameter):
    # Add a UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=diameter / 2, location=location)

    # Get the newly created sphere
    sphere = bpy.context.object

    # Assign the material to the sphere
    if sphere.data.materials:
        sphere.data.materials[0] = sphere_material
    else:
        sphere.data.materials.append(sphere_material)

# Read the CSV file and add spheres at each point
with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        x, y, z = map(float, row)
        add_sphere_at_location((x, y, z), sphere_diameter)

# Add a triangular prism at (0, 0, 0) and rotate it to point in the positive X direction
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.1, depth=0.15, location=(.2, 0, 0))
prism = bpy.context.object
prism.rotation_euler = (0, math.radians(90), 0)

# Add four torus objects scaled to 0.1 in x, y, z
torus_locations = [(0.1, 0.1, 0), (-0.1, 0.1, 0), (-0.1, -0.1, 0), (0.1, -0.1, 0)]
for loc in torus_locations:
    bpy.ops.mesh.primitive_torus_add(location=loc)
    torus = bpy.context.object
    torus.scale = (0.1, 0.1, 0.1)

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

# Create a new line style
linestyle = bpy.data.linestyles.new(name="LineStyle")
lineset.linestyle = linestyle

# Set the line thickness
linestyle.thickness = 4.0  # Adjust the thickness value as needed

# Get the first view layer
view_layer = bpy.context.scene.view_layers[0]

# Create a new line set for Freestyle
lineset = view_layer.freestyle_settings.linesets.new(name="LineSet")
lineset.select_silhouette = True
lineset.select_border = True
lineset.select_crease = True
lineset.select_edge_mark = True

# Set up the compositor to add a white background
bpy.context.scene.use_nodes = True
nodes = bpy.context.scene.node_tree.nodes
links = bpy.context.scene.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Add Render Layers node
render_layers = nodes.new(type='CompositorNodeRLayers')
render_layers.location = 0, 0

# Add Alpha Over node
alpha_over = nodes.new(type='CompositorNodeAlphaOver')
alpha_over.location = 200, 0
alpha_over.inputs[1].default_value = (1, 1, 1, 1)  # Set background to white

# Add Composite node
composite = nodes.new(type='CompositorNodeComposite')
composite.location = 400, 0

# Link nodes
links.new(render_layers.outputs['Image'], alpha_over.inputs[2])
links.new(alpha_over.outputs['Image'], composite.inputs['Image'])

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

# Calculate the absolute maximum value for each axis
abs_max_x = max(abs(min_x), abs(max_x))
abs_max_y = max(abs(min_y), abs(max_y))
abs_max_z = max(abs(min_z), abs(max_z))

# Define the new bounding box extents
min_x = -abs_max_x
max_x = abs_max_x
min_y = -abs_max_y
max_y = abs_max_y
min_z = -abs_max_z
max_z = abs_max_z

# Calculate the center and size of the bounding box
center = mathutils.Vector(((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2))
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

# Function to set up the camera and render the scene
def render_view(view_name, camera_location, camera_rotation, output_directory, distance_factor=1.75):
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
    bpy.context.scene.render.resolution_x = 900
    bpy.context.scene.render.resolution_y = 600
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
    ("Isometric", (1, -1, 1), (math.radians(52.5), 0, math.radians(45))),
    ("Right", (0, -1, 0), (math.radians(90), 0, 0)),
    ("Front", (1, 0, 0), (math.radians(90), 0, math.radians(90))),
    ("Back", (-1, 0, 0), (math.radians(90), 0, math.radians(-90))),
    ("Left", (0, 1, 0), (math.radians(-90), math.radians(180), 0)),
    ("Top", (0, 0, 1), (0, 0, 0))
]

# Specify the output directory explicitly
file_output_directory = os.path.dirname(csv_file_path)
render_folder = 'rendered_views'
render_output_directory = os.path.join(file_output_directory, render_folder)

# Make sure the output directory exists
if not os.path.exists(render_output_directory):
    os.makedirs(render_output_directory)

# Render each view
for view_name, camera_location, camera_rotation in views:
    render_view(view_name, camera_location, camera_rotation, render_output_directory)

blender_file_name, csv_file_ext = os.path.splitext(os.path.basename(csv_file_path))
blender_file_name = blender_file_name + ".blend"

# Save the Blender file
blender_file_path = os.path.join(file_output_directory, blender_file_name)
bpy.ops.wm.save_as_mainfile(filepath=blender_file_path)

print(f"Blender file saved to: {blender_file_path}")

print("CSV file imported, spheres added, cube added, grid added, and views rendered.")