# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Procedural Serious Sam Egyptian Arena Generator
Generates a massive, atmospheric Serious Sam styled combat arena in the active level.
"""

import math
import unreal

def delete_existing_arena():
    """
    Cleans up any previously generated Serious Sam actors to allow clean regeneration.
    """
    editor_actors = unreal.EditorActorSubsystem()
    all_actors = editor_actors.get_all_level_actors()
    
    deleted_count = 0
    for actor in all_actors:
        actor_name = actor.get_actor_label()
        if "SeriousSam_" in actor_name:
            editor_actors.destroy_actor(actor)
            deleted_count += 1
            
    if deleted_count > 0:
        print(f"Cleaned up {deleted_count} existing arena actors.")

def spawn_static_mesh(mesh_path, location, scale, name, material_path=None):
    """
    Helper function to spawn a StaticMeshActor with a specific mesh and scale.
    """
    editor_actors = unreal.EditorActorSubsystem()
    
    # Spawn a standard StaticMeshActor
    actor = editor_actors.spawn_actor_from_class(unreal.StaticMeshActor, location, unreal.Rotator(0, 0, 0))
    if not actor:
        print(f"Failed to spawn actor: {name}")
        return None
        
    actor.set_actor_label(f"SeriousSam_{name}")
    actor.set_actor_scale3d(scale)
    
    # Load and set the Static Mesh component
    sm_component = actor.static_mesh_component
    loaded_mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if loaded_mesh:
        sm_component.set_static_mesh(loaded_mesh)
    else:
        print(f"Failed to load mesh: {mesh_path}")
        
    # Optional: Load and set custom material
    if material_path:
        loaded_mat = unreal.EditorAssetLibrary.load_asset(material_path)
        if loaded_mat:
            sm_component.set_material(0, loaded_mat)
            
    return actor

def spawn_light(light_class, location, intensity, color, name, radius=1000.0):
    """
    Helper function to spawn and configure lights.
    """
    editor_actors = unreal.EditorActorSubsystem()
    actor = editor_actors.spawn_actor_from_class(light_class, location, unreal.Rotator(-45, 45, 0))
    if not actor:
        return None
        
    actor.set_actor_label(f"SeriousSam_{name}")
    
    if light_class == unreal.PointLight:
        light_comp = actor.point_light_component
        light_comp.set_intensity(intensity)
        light_comp.set_light_color(color)
        light_comp.set_attenuation_radius(radius)
    elif light_class == unreal.DirectionalLight:
        light_comp = actor.directional_light_component
        light_comp.set_intensity(intensity)
        light_comp.set_light_color(color)
        light_comp.set_cast_shadows(True)
        
    return actor

def generate_arena():
    print("=========================================================")
    print("  LUDUS MAGNUS: GENERATING SERIOUS SAM EGYPTIAN ARENA   ")
    print("=========================================================")
    
    # 0. Clean up old elements
    delete_existing_arena()
    
    # Asset paths
    cube_mesh = "/Engine/BasicShapes/Cube.Cube"
    cylinder_mesh = "/Engine/BasicShapes/Cylinder.Cylinder"
    cone_mesh = "/Engine/BasicShapes/Cone.Cone"
    sphere_mesh = "/Engine/BasicShapes/Sphere.Sphere"
    
    # Standard materials
    grid_mat = "/Engine/EngineMaterials/M_Grid_Green.M_Grid_Green" # Standard green grid
    default_mat = "/Engine/EngineMaterials/DefaultMaterial.DefaultMaterial"
    
    # 1. Spawn Massive Arena Floor (120m x 120m)
    print("Spawning Arena Floor...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(0, 0, 0),
        scale=unreal.Vector(120, 120, 1),
        name="Arena_Floor",
        material_path=grid_mat
    )
    
    # 2. Spawn Perimeter Walls (Containment)
    print("Spawning Arena Boundary Walls...")
    wall_thickness = 2.0
    wall_height = 10.0
    half_size = 6000.0 # 60 meters in Unreal Units (1uu = 1cm)
    
    # North Wall
    spawn_static_mesh(cube_mesh, unreal.Vector(half_size, 0, 500), unreal.Vector(wall_thickness, 120, wall_height), "Wall_North")
    # South Wall
    spawn_static_mesh(cube_mesh, unreal.Vector(-half_size, 0, 500), unreal.Vector(wall_thickness, 120, wall_height), "Wall_South")
    # East Wall
    spawn_static_mesh(cube_mesh, unreal.Vector(0, half_size, 500), unreal.Vector(120, wall_thickness, wall_height), "Wall_East")
    # West Wall
    spawn_static_mesh(cube_mesh, unreal.Vector(0, -half_size, 500), unreal.Vector(120, wall_thickness, wall_height), "Wall_West")
    
    # 3. Spawn Central Egyptian Obelisk (Altar)
    print("Constructing Central Obelisk...")
    # Base
    spawn_static_mesh(cube_mesh, unreal.Vector(0, 0, 150), unreal.Vector(8, 8, 3), "Obelisk_Base")
    # Middle Column
    spawn_static_mesh(cube_mesh, unreal.Vector(0, 0, 750), unreal.Vector(4, 4, 10), "Obelisk_Column")
    # Cone Top
    spawn_static_mesh(cone_mesh, unreal.Vector(0, 0, 1350), unreal.Vector(4, 4, 4), "Obelisk_Pyramidion")
    # Golden glow on the Altar
    spawn_light(unreal.PointLight, unreal.Vector(0, 0, 1600), 50000.0, unreal.Color(255, 180, 0, 255), "Obelisk_Glow", radius=2000.0)

    # 4. Spawn 12 Giant Pillars in a circle (Radius: 35m) with warm torchlights
    print("Erecting 12 Ancient Pillars with Torches...")
    radius = 3500.0 # 35 meters
    num_pillars = 12
    for i in range(num_pillars):
        angle = (i * 2 * math.pi) / num_pillars
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        # Pillar Cylinder (Scale: 2m x 2m x 8m)
        spawn_static_mesh(
            mesh_path=cylinder_mesh,
            location=unreal.Vector(x, y, 400),
            scale=unreal.Vector(3, 3, 8),
            name=f"Pillar_{i+1}"
        )
        
        # Torch Base on top
        spawn_static_mesh(
            mesh_path=cone_mesh,
            location=unreal.Vector(x, y, 820),
            scale=unreal.Vector(2, 2, 0.5),
            name=f"TorchBase_{i+1}"
        )
        
        # Dynamic Fire Light (Orange/Red)
        spawn_light(
            light_class=unreal.PointLight,
            location=unreal.Vector(x, y, 880),
            intensity=35000.0,
            color=unreal.Color(255, 69, 0, 255), # Orange Red
            name=f"TorchLight_{i+1}",
            radius=1500.0
        )
        
    # 5. Spawn Hordes of "Headless Kamikaze" placeholders (Spheres/Cones rushing the player start)
    print("Spawning 8 Kamikaze Horde placeholders...")
    # These represent kamikaze monsters charging toward the arena center
    enemy_radius = 4800.0
    num_enemies = 8
    for i in range(num_enemies):
        angle = (i * 2 * math.pi) / num_enemies + 0.3
        x = enemy_radius * math.cos(angle)
        y = enemy_radius * math.sin(angle)
        
        # Red Glowing body (Sphere)
        spawn_static_mesh(
            mesh_path=sphere_mesh,
            location=unreal.Vector(x, y, 100),
            scale=unreal.Vector(1.5, 1.5, 1.5),
            name=f"Kamikaze_{i+1}_Body"
        )
        
        # Red Point Light representing internal rage/glow
        spawn_light(
            light_class=unreal.PointLight,
            location=unreal.Vector(x, y, 200),
            intensity=15000.0,
            color=unreal.Color(255, 0, 0, 255), # Pure Red
            name=f"KamikazeGlow_{i+1}",
            radius=800.0
        )
        
    # 6. Spawn Ammo and Health Item Pickups near the pillars
    print("Scattering Health and Ammo pick-ups...")
    pickup_radius = 2800.0
    for i in range(4):
        angle = (i * 2 * math.pi) / 4 + 0.785 # 45 degrees offset
        x = pickup_radius * math.cos(angle)
        y = pickup_radius * math.sin(angle)
        
        # Health Pack (Green Box)
        spawn_static_mesh(
            mesh_path=cube_mesh,
            location=unreal.Vector(x, y, 50),
            scale=unreal.Vector(1.0, 1.0, 1.0),
            name=f"HealthPickup_{i+1}"
        )
        spawn_light(
            light_class=unreal.PointLight,
            location=unreal.Vector(x, y, 120),
            intensity=8000.0,
            color=unreal.Color(0, 255, 0, 255), # Pure Green
            name=f"HealthGlow_{i+1}",
            radius=500.0
        )
        
        # Ammo Pack (Yellow Box)
        spawn_static_mesh(
            mesh_path=cube_mesh,
            location=unreal.Vector(-x, -y, 50),
            scale=unreal.Vector(1.2, 0.8, 0.6),
            name=f"AmmoPickup_{i+1}"
        )
        spawn_light(
            light_class=unreal.PointLight,
            location=unreal.Vector(-x, -y, 120),
            intensity=8000.0,
            color=unreal.Color(255, 255, 0, 255), # Pure Yellow
            name=f"AmmoGlow_{i+1}",
            radius=500.0
        )

    # 7. Setup Dynamic Lighting (Directional Light and SkyLight)
    print("Setting up Sky Lighting...")
    # Sun Light
    spawn_light(
        light_class=unreal.DirectionalLight,
        location=unreal.Vector(0, 0, 5000),
        intensity=4.0,
        color=unreal.Color(255, 240, 220, 255), # Pale yellow sun
        name="DirectionalLight"
    )
    
    # 8. Setup Player Start
    print("Placing Player Start...")
    editor_actors = unreal.EditorActorSubsystem()
    
    # Check if a PlayerStart already exists in the SeriousSam namespace
    all_actors = editor_actors.get_all_level_actors()
    player_start_exists = False
    for actor in all_actors:
        if "SeriousSam_PlayerStart" in actor.get_actor_label():
            player_start_exists = True
            # Re-position it
            actor.set_actor_location(unreal.Vector(0, 2500, 100), False, False)
            actor.set_actor_rotation(unreal.Rotator(0, -90, 0), False)
            break
            
    if not player_start_exists:
        # Spawn a new PlayerStart
        p_start = editor_actors.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(0, 2500, 100), unreal.Rotator(0, -90, 0))
        if p_start:
            p_start.set_actor_label("SeriousSam_PlayerStart")
            
    print("\n[SUCCESS] Serious Sam Egyptian Arena procedurally generated at (0, 0, 0)!")
    print("=========================================================")

if __name__ == "__main__":
    generate_arena()
