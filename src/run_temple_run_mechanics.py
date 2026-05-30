# -*- coding: utf-8 -*-
"""
UnrealMCP - Temple Run Mechanics Remote Trigger
Sends temple_run_mechanics.py to the active Unreal Editor session via socket TCP bridge.
"""

import asyncio
import sys
import os
from src.unreal_server.remote_execution_client import UnrealRemoteExecutor

async def main():
    script_path = os.path.join(os.path.dirname(__file__), "temple_run_mechanics.py")
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at {script_path}")
        return
        
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
        
    print("Connecting to Unreal Engine TCP Socket Listener...")
    executor = UnrealRemoteExecutor()
    
    print("Injecting Temple Run Gameplay Engine into Unreal Editor Post-Tick loop...")
    res = await executor.execute_command(script_code, exec_mode="ExecuteFile")
    
    if res.get("success"):
        print("\n[SUCCESS] Temple Run Gameplay Engine successfully injected and running in the editor!")
        print("Execution Logs from Editor:")
        print(res.get("result", ""))
        print("\n========================================================")
        print("TEMPLE RUN GAME MECHANICS ARE NOW LIVE!")
        print("1. Go to your Unreal Editor.")
        print("2. Press PLAY (PIE) in the Editor toolbar.")
        print("3. Your character will automatically run forward!")
        print("4. Controls:")
        print("   * A / Left Arrow: Turn 90 degrees Left (at intersections)")
        print("   * D / Right Arrow: Turn 90 degrees Right (at intersections)")
        print("   * Space / Up Arrow: Jump (over Tomruk Log hurdles)")
        print("5. UI HUD will show your Coins and Distance in real-time!")
        print("6. If you fall off the bridge or hit obstacles, the game")
        print("   will show GAME OVER and restart you after 2 seconds!")
        print("========================================================")
    else:
        print(f"\n[ERROR] Remote execution failed: {res}")
        
    await executor.stop_session()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
