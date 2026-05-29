# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_SRD_BLN_01] & [REQ_SRD_BLN_02] Headless Blender bpy template
Executed in background to generate parameterized procedural mesh and material, exporting to FBX
"""

import bpy
import sys
from mathutils import Vector

def clear_scene():
    """
    Clears all existing mesh and material objects from the startup scene.
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Delete unused materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def generate_mesh(shape: str, size: float, segments: int = 32) -> bpy.types.Object:
    """
    Generates a primitive geometric shape based on parameters.
    """
    if shape == "cube":
        bpy.ops.mesh.primitive_cube_add(size=size)
        obj = bpy.context.active_object
        obj.name = "SM_Proc_Cube"
    elif shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=size / 2.0, segments=segments, rings=segments)
        obj = bpy.context.active_object
        obj.name = "SM_Proc_Sphere"
    elif shape == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=size / 2.0, depth=size, vertices=segments)
        obj = bpy.context.active_object
        obj.name = "SM_Proc_Cylinder"
    else:
        # Fallback to primitive cube
        bpy.ops.mesh.primitive_cube_add(size=size)
        obj = bpy.context.active_object
        obj.name = "SM_Proc_Mesh"
        
    return obj

def create_pbr_material(albedo_color, metallic: float, roughness: float) -> bpy.types.Material:
    """
    Creates a parameterized PBR material using Principled BSDF node nodes.
    """
    mat = bpy.data.materials.new(name="M_Proc_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Retrieve Principled BSDF shader node
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Set base color (RGBA)
        bsdf.inputs['Base Color'].default_value = (
            float(albedo_color[0]),
            float(albedo_color[1]),
            float(albedo_color[2]),
            float(albedo_color[3])
        )
        # Set metallic property
        bsdf.inputs['Metallic'].default_value = float(metallic)
        # Set roughness property
        bsdf.inputs['Roughness'].default_value = float(roughness)
        
    return mat

def align_pivot_to_bottom_center(obj: bpy.types.Object):
    """
    Aligns the object's origin pivot point to its absolute bottom-center coordinate.
    Ensures perfect pivot grounding when spawned inside Unreal Engine 5 level.
    """
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Calculate bounding box corners in world coordinates
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    # Compute bottom Z limit and X-Y plane center
    min_z = min(corner.z for corner in bbox)
    center_x = sum(corner.x for corner in bbox) / 8.0
    center_y = sum(corner.y for corner in bbox) / 8.0
    
    # Set scene 3D Cursor to the calculated bottom-center point
    bpy.context.scene.cursor.location = (center_x, center_y, min_z)
    
    # Translate origin to the cursor location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

def export_fbx(filepath: str):
    """
    Exports selected meshes as FBX with Z-up Y-forward mapping bake.
    """
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        global_scale=1.0,
        axis_forward='-Z',  # Blender -Z forward converts to Unreal forward
        axis_up='Y',        # Blender Y up converts to Unreal Z up
        bake_space_transform=True,
        use_mesh_modifiers=True,
        mesh_smooth_groups=True
    )

def main():
    # Variables will be dynamically prepended here by generator.py
    # e.g. CONFIG_DATA = {...}
    try:
        config = CONFIG_DATA
    except NameError:
        # Test fallback configurations
        config = {
            "shape": "cube",
            "size": 1.0,
            "albedo": [0.7, 0.7, 0.7, 1.0],
            "metallic": 0.0,
            "roughness": 0.5,
            "output_path": "C:/Temp/SM_Proc_Mesh_Default.fbx"
        }

    # 1. Clear default scene
    clear_scene()
    
    # 2. Build geometric primitive mesh
    obj = generate_mesh(config["shape"], float(config["size"]))
    
    # 3. Unwrap UV coordinates automatically using Smart Project
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # 4. Generate PBR parameters material and append to object
    material = create_pbr_material(config["albedo"], config["metallic"], config["roughness"])
    obj.data.materials.append(material)
    
    # 5. Align pivot origin to bottom center for grounded spawn
    align_pivot_to_bottom_center(obj)
    
    # 6. Bake space transformations and export Z-up FBX model
    export_fbx(config["output_path"])
    print("SUCCESS_PROCEDURAL_EXPORT")

if __name__ == "__main__":
    main()
