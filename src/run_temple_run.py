# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Temple Run Generator Remote Trigger
Reads generate_temple_run.py and executes it inside the active Unreal Editor session via socket TCP bridge.
"""

import asyncio
import sys
import os
from src.unreal_server.remote_execution_client import UnrealRemoteExecutor

async def main():
    script_path = os.path.join(os.path.dirname(__file__), "generate_temple_run.py")
    if not os.path.exists(script_path):
        print(f"Error: Script file not found at {script_path}")
        return
        
    with open(script_path, "r", encoding="utf-8") as f:
        script_code = f.read()
        
    print("Connecting to Unreal Engine TCP Socket Listener...")
    executor = UnrealRemoteExecutor()
    
    print("Sending procedural Temple Run generator code to Unreal Editor...")
    res = await executor.execute_command(script_code, exec_mode="ExecuteFile")
    
    if res.get("success"):
        print("\n[SUCCESS] Procedural generator script successfully executed inside Unreal Editor!")
        print("Execution Logs from Editor:")
        print(res.get("result", ""))
        print("\n========================================================")
        print("Procedural Temple Run build complete! Open your Unreal Editor viewport.")
        print("Find 'TempleRun_Start_Platform' or press F to focus on the starting line.")
        print("Press PLAY in the Editor to test your suspended track run!")
        print("========================================================")
    else:
        print(f"\n[ERROR] Remote execution failed: {res}")
        
    await executor.stop_session()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
