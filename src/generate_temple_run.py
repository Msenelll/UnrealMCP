# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Procedural Temple Run Level Generator
Clears Serious Sam actors and constructs a winding, high-altitude Temple Run pathway with obstacles, coins, and a chasing monster.
"""

import math
import unreal

def delete_existing_actors():
    """
    Cleans up any previously generated Serious Sam and Temple Run actors for a clean slate.
    """
    editor_actors = unreal.EditorActorSubsystem()
    all_actors = editor_actors.get_all_level_actors()
    
    sam_deleted = 0
    tr_deleted = 0
    for actor in all_actors:
        actor_name = actor.get_actor_label()
        if "SeriousSam_" in actor_name:
            editor_actors.destroy_actor(actor)
            sam_deleted += 1
        elif "TempleRun_" in actor_name:
            editor_actors.destroy_actor(actor)
            tr_deleted += 1
            
    if sam_deleted > 0:
        print(f"Removed {sam_deleted} Serious Sam actors.")
    if tr_deleted > 0:
        print(f"Removed {tr_deleted} existing Temple Run actors.")

def spawn_static_mesh(mesh_path, location, scale, name, rotation=unreal.Rotator(0,0,0), material_path=None):
    """
    Helper to spawn a StaticMeshActor.
    """
    editor_actors = unreal.EditorActorSubsystem()
    actor = editor_actors.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    if not actor:
        return None
        
    actor.set_actor_label(f"TempleRun_{name}")
    actor.set_actor_scale3d(scale)
    
    sm_component = actor.static_mesh_component
    loaded_mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if loaded_mesh:
        sm_component.set_static_mesh(loaded_mesh)
        
    if material_path:
        loaded_mat = unreal.EditorAssetLibrary.load_asset(material_path)
        if loaded_mat:
            sm_component.set_material(0, loaded_mat)
            
    return actor

def spawn_light(light_class, location, intensity, color, name, radius=1000.0):
    """
    Helper to spawn PointLights for torches/traps.
    """
    editor_actors = unreal.EditorActorSubsystem()
    actor = editor_actors.spawn_actor_from_class(light_class, location, unreal.Rotator(0, 0, 0))
    if not actor:
        return None
    actor.set_actor_label(f"TempleRun_{name}")
    
    if light_class == unreal.PointLight:
        light_comp = actor.point_light_component
        light_comp.set_intensity(intensity)
        light_comp.set_light_color(color)
        light_comp.set_attenuation_radius(radius)
        
    return actor

def generate_temple_run():
    print("=========================================================")
    print("  LUDUS MAGNUS: CONSTRUCTING PROCEDURAL TEMPLE RUN TRACK ")
    print("=========================================================")
    
    # 0. Clean slate
    delete_existing_actors()
    
    # Asset paths
    cube_mesh = "/Engine/BasicShapes/Cube.Cube"
    cylinder_mesh = "/Engine/BasicShapes/Cylinder.Cylinder"
    cone_mesh = "/Engine/BasicShapes/Cone.Cone"
    sphere_mesh = "/Engine/BasicShapes/Sphere.Sphere"
    grid_mat = "/Engine/EngineMaterials/M_Grid_Green.M_Grid_Green"
    
    # 1. Spawn Starting Altar / Platform (10m x 10m x 1m)
    print("Building Starting Platform...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(0, 0, 0),
        scale=unreal.Vector(10, 10, 1),
        name="Start_Platform",
        material_path=grid_mat
    )
    
    # Side guard rails for the starting platform
    spawn_static_mesh(cube_mesh, unreal.Vector(0, 500, 100), unreal.Vector(10, 0.4, 2), "Start_Rail_L")
    spawn_static_mesh(cube_mesh, unreal.Vector(0, -500, 100), unreal.Vector(10, 0.4, 2), "Start_Rail_R")
    
    # 2. RUNWAY SECTION 1: North (Along +X Axis, length 30m, width 3m)
    print("Spawning Runway Segment 1 (North)...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(2000, 0, 0),
        scale=unreal.Vector(30, 3, 1),
        name="Runway_1",
        material_path=grid_mat
    )
    
    # Gold coins floating on Runway 1
    for x_offset in range(1000, 3200, 400):
        # Coin sphere (Scale: 0.4m)
        spawn_static_mesh(sphere_mesh, unreal.Vector(x_offset, 0, 120), unreal.Vector(0.4, 0.4, 0.4), f"Coin_1_{x_offset}")
        spawn_light(unreal.PointLight, unreal.Vector(x_offset, 0, 160), 3000.0, unreal.Color(255, 215, 0, 255), f"CoinGlow_1_{x_offset}", radius=200.0)
        
    # Obstacle 1: Tree Log hurdle across track
    spawn_static_mesh(cylinder_mesh, unreal.Vector(1800, 0, 80), unreal.Vector(0.6, 3.2, 0.6), "Hurdle_Log", rotation=unreal.Rotator(0, 0, 90))
    spawn_light(unreal.PointLight, unreal.Vector(1800, 0, 180), 8000.0, unreal.Color(255, 0, 0, 255), "Hurdle_Glow", radius=400.0)

    # 3. INTERSECTION 1: Right-Angle Turn Right (At X = 3500, Y = 0)
    print("Building Junction Platform 1 (Turn Right)...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(3500, 0, 0),
        scale=unreal.Vector(6, 6, 1),
        name="Junction_1",
        material_path=grid_mat
    )
    # Block direct North path at the junction so player must turn
    spawn_static_mesh(cube_mesh, unreal.Vector(3800, 0, 150), unreal.Vector(0.5, 6, 3), "Junction_1_Wall")

    # 4. RUNWAY SECTION 2: East (Along +Y Axis, length 30m, width 3m)
    print("Spawning Runway Segment 2 (East)...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(3500, 1800, 0),
        scale=unreal.Vector(3, 30, 1),
        name="Runway_2",
        material_path=grid_mat
    )
    
    # Gold coins floating on Runway 2
    for y_offset in range(800, 3000, 400):
        spawn_static_mesh(sphere_mesh, unreal.Vector(3500, y_offset, 120), unreal.Vector(0.4, 0.4, 0.4), f"Coin_2_{y_offset}")
        spawn_light(unreal.PointLight, unreal.Vector(3500, y_offset, 160), 3000.0, unreal.Color(255, 215, 0, 255), f"CoinGlow_2_{y_offset}", radius=200.0)

    # Obstacle 2: Broken Arch (Player must slide under)
    # Pillars
    spawn_static_mesh(cylinder_mesh, unreal.Vector(3380, 2200, 150), unreal.Vector(0.5, 0.5, 3), "Arch_Pillar_L")
    spawn_static_mesh(cylinder_mesh, unreal.Vector(3620, 2200, 150), unreal.Vector(0.5, 0.5, 3), "Arch_Pillar_R")
    # Arch Header (placed low so player has to duck/slide)
    spawn_static_mesh(cube_mesh, unreal.Vector(3500, 2200, 280), unreal.Vector(3.0, 0.6, 0.4), "Arch_Header")

    # 5. INTERSECTION 2: Right-Angle Turn Left (At X = 3500, Y = 3300)
    print("Building Junction Platform 2 (Turn Left)...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(3500, 3300, 0),
        scale=unreal.Vector(6, 6, 1),
        name="Junction_2",
        material_path=grid_mat
    )
    # Block direct East path at junction
    spawn_static_mesh(cube_mesh, unreal.Vector(3500, 3600, 150), unreal.Vector(6, 0.5, 3), "Junction_2_Wall")

    # 6. RUNWAY SECTION 3: North (Along +X Axis, length 40m, width 3m)
    print("Spawning Runway Segment 3 (North)...")
    spawn_static_mesh(
        mesh_path=cube_mesh,
        location=unreal.Vector(5500, 3300, 0),
        scale=unreal.Vector(40, 3, 1),
        name="Runway_3",
        material_path=grid_mat
    )
    
    # Gold coins floating on Runway 3
    for x_offset in range(4000, 7200, 400):
        spawn_static_mesh(sphere_mesh, unreal.Vector(x_offset, 3300, 120), unreal.Vector(0.4, 0.4, 0.4), f"Coin_3_{x_offset}")
        spawn_light(unreal.PointLight, unreal.Vector(x_offset, 3300, 160), 3000.0, unreal.Color(255, 215, 0, 255), f"CoinGlow_3_{x_offset}", radius=200.0)

    # 7. THE CHASING DEMON MONSTER
    print("Spawning Chasing Demon Monkey placeholder...")
    # A terrifying spiked structure with dynamic purple glow hovering right behind starting line
    spawn_static_mesh(cone_mesh, unreal.Vector(-450, 0, 200), unreal.Vector(3, 3, 3), "Demon_Body", rotation=unreal.Rotator(180, 0, 0))
    spawn_static_mesh(sphere_mesh, unreal.Vector(-450, 150, 200), unreal.Vector(1, 1, 1), "Demon_LeftClaw")
    spawn_static_mesh(sphere_mesh, unreal.Vector(-450, -150, 200), unreal.Vector(1, 1, 1), "Demon_RightClaw")
    # Scary purple demonic glow
    spawn_light(unreal.PointLight, unreal.Vector(-300, 0, 250), 40000.0, unreal.Color(138, 43, 226, 255), "Demon_EyeGlow", radius=1200.0)

    # 8. ATMOSPHERIC WALL TORCHES
    print("Placing Side Torches...")
    # Warm torches along runway walls
    torch_positions = [
        unreal.Vector(1000, 160, 120),
        unreal.Vector(2500, -160, 120),
        unreal.Vector(3340, 1200, 120),
        unreal.Vector(3660, 2500, 120),
        unreal.Vector(4800, 3460, 120),
        unreal.Vector(6500, 3140, 120)
    ]
    for idx, pos in enumerate(torch_positions):
        # Small torch cylinder
        spawn_static_mesh(cylinder_mesh, pos, unreal.Vector(0.15, 0.15, 0.8), f"Torch_{idx+1}")
        # Warm fire light
        spawn_light(unreal.PointLight, pos + unreal.Vector(0, 0, 60), 12000.0, unreal.Color(255, 100, 0, 255), f"TorchLight_{idx+1}", radius=800.0)

    # 9. Setup Player Start
    print("Configuring Player Start...")
    editor_actors = unreal.EditorActorSubsystem()
    all_actors = editor_actors.get_all_level_actors()
    player_start_exists = False
    
    for actor in all_actors:
        # Check label for SeriousSam_PlayerStart to destroy it
        label = actor.get_actor_label()
        if "SeriousSam_PlayerStart" in label:
            editor_actors.destroy_actor(actor)
        elif "TempleRun_PlayerStart" in label:
            player_start_exists = True
            # Re-position at the start of Temple Run runway
            actor.set_actor_location(unreal.Vector(-200, 0, 100), False, False)
            actor.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
            
    if not player_start_exists:
        p_start = editor_actors.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-200, 0, 100), unreal.Rotator(0, 0, 0))
        if p_start:
            p_start.set_actor_label("TempleRun_PlayerStart")

    print("\n[SUCCESS] Temple Run suspended level successfully generated at (0, 0, 0)!")
    print("=========================================================")

if __name__ == "__main__":
    generate_temple_run()
