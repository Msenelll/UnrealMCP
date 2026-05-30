# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
UnrealMCP v2.0 Hands-On Verification Tool
Interactive live testing of PBI_006, PBI_007, PBI_008, and PBI_009.
"""

import asyncio
import sys
from src.unreal_server.client import UnrealClient
from src.unreal_server.remote_execution_client import UnrealRemoteExecutor

async def main():
    print("==================================================================")
    print("      LUDUS MAGNUS - UNREALMCP V2.0 LIVE VERIFICATION TOOL        ")
    print("==================================================================")
    print("Connecting to local Unreal Engine Editor (localhost:30010)...")
    
    client = UnrealClient()
    executor = UnrealRemoteExecutor()
    
    # Check if editor is online
    telemetry = await client.get_viewport_telemetry()
    if not telemetry.get("success") or telemetry.get("error") == "EDITOR_OFFLINE":
        print("\n[ERROR] Unreal Editor is OFFLINE or Web Remote Control Server is inactive on port 30010.")
        print("Please ensure the editor is open and 'WebControl.StartServer' has been run.")
        await client.close()
        return

    print("\n[SUCCESS] Connected to active Unreal Editor!")
    print(f"Active Camera Coordinates: {telemetry['camera']['location']}")
    
    # --------------------------------------------------------
    # STEP 1: PBI_007 Scene Introspection & Hierarchy
    # --------------------------------------------------------
    print("\n--- STEP 1: Scene Hierarchy Introspection (PBI_007) ---")
    hierarchy = await client.get_scene_hierarchy()
    if hierarchy.get("success"):
        actors = hierarchy.get("actors", [])
        print(f"Detected {len(actors)} actors in active Level.")
        if actors:
            # Print the first 5 actors
            print("First few actors in hierarchy:")
            for a in actors[:5]:
                print(f"  * {a['name']} ({a['actor_path']})")
                
            # Introspect components of the first actor
            target_actor = actors[0]["actor_path"]
            print(f"\nIntrospecting components for target: {actors[0]['name']}...")
            comp_res = await client.get_actor_components(target_actor)
            if comp_res.get("success"):
                print(f"Successfully introspected components:")
                for c in comp_res.get("components", []):
                    print(f"  - Component: {c['name']} (Type: {c['type']})")
    else:
        print(f"Hierarchy fetch failed: {hierarchy}")

    # --------------------------------------------------------
    # STEP 2: PBI_008 Custom Blueprint & Asset Spawning
    # --------------------------------------------------------
    print("\n--- STEP 2: Custom Asset Spawning (PBI_008) ---")
    # We will spawn a PointLight as a safe test actor
    print("Spawning a test PointLight actor in the level...")
    spawn_res = await client.spawn_actor(
        actor_class="/Script/Engine.PointLight",
        location={"x": 0.0, "y": 0.0, "z": 200.0}
    )
    if spawn_res.get("success"):
        spawned_actor_path = spawn_res["actor_path"]
        print(f"[SUCCESS] Spawned PointLight: {spawned_actor_path}")
    else:
        print(f"[ERROR] Failed to spawn actor: {spawn_res}")
        await client.close()
        return

    # Wait for visual confirmation
    print("\nWait 3 seconds for visual confirmation in your viewport...")
    await asyncio.sleep(3.0)

    # --------------------------------------------------------
    # STEP 3: PBI_009 Editor Undo / Rollback
    # --------------------------------------------------------
    print("\n--- STEP 3: Editor Undo History Rollback (PBI_009) ---")
    print("Calling 'unreal_editor_undo' to remove the spawned actor...")
    undo_res = await client.undo()
    if undo_res.get("success"):
        print("[SUCCESS] Editor Undo command sent! Look at your Viewport: The PointLight should be GONE.")
    else:
        print(f"[ERROR] Undo failed: {undo_res}")

    # Wait for visual confirmation
    print("\nWait 3 seconds for visual confirmation...")
    await asyncio.sleep(3.0)

    # --------------------------------------------------------
    # STEP 4: PBI_009 Editor Redo
    # --------------------------------------------------------
    print("\n--- STEP 4: Editor Redo History Rollback (PBI_009) ---")
    print("Calling 'unreal_editor_redo' to restore the spawned actor...")
    redo_res = await client.redo()
    if redo_res.get("success"):
        print("[SUCCESS] Editor Redo command sent! Look at your Viewport: The PointLight should be RESTORED.")
    else:
        print(f"[ERROR] Redo failed: {redo_res}")

    # Wait for visual confirmation
    print("\nWait 3 seconds for visual confirmation...")
    await asyncio.sleep(3.0)

    # --------------------------------------------------------
    # STEP 5: PBI_006 Socket-based Python Remote Execution
    # --------------------------------------------------------
    print("\n--- STEP 5: Socket-Based Python Execution (PBI_006) ---")
    print("Sending dynamic script over socket TCP bridge...")
    script = (
        "import unreal\n"
        "unreal.log_warning('LUDUS MAGNUS: unreal_execute_python socket bridge is online!')\n"
        "selected = unreal.EditorActorSubsystem().get_selected_level_actors()\n"
        "print(f'Active Python Selection: {len(selected)} actors')"
    )
    
    exec_res = await executor.execute_command(script, exec_mode="ExecuteFile")
    if exec_res.get("success"):
        print("[SUCCESS] Python execution completed!")
        print("Script execution logs:")
        print(exec_res.get("result", ""))
        print("\nCheck the Output Log inside your Unreal Editor: you will see the orange warning from Ludus Magnus!")
    else:
        print(f"[ERROR] Socket execution failed: {exec_res}")

    await client.close()
    await executor.stop_session()
    print("\n==================================================================")
    print("Verification completed successfully!")
    print("==================================================================")

if __name__ == "__main__":
    # Ensure correct asyncio loop on Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
