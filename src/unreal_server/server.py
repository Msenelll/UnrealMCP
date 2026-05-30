# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_TDD_ARC_01] Unreal Engine 5 MCP Server Entry Point
Initializes stdio server transport, registers tools, and routes calls asynchronously
"""

import asyncio
import sys
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from src.unreal_server.client import UnrealClient
from src.unreal_server.execution import SubprocessManager
from src.unreal_server.remote_execution_client import UnrealRemoteExecutor

# Configure strict enterprise logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr  # Direct logging to stderr so it does not interfere with stdout stdio channel
)
logger = logging.getLogger("UnrealMCPServer")

# Initialize Server instance
server = Server("unreal-mcp-server")

# Instantiate async modules
unreal_client = UnrealClient()
proc_manager = SubprocessManager()
remote_executor = UnrealRemoteExecutor()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Registers the 5 core tools for otonom actor manipulation, viewport telemetry,
    and Dual-Layer Compilation triggers.
    """
    return [
        types.Tool(
            name="unreal_get_viewport_telemetry",
            description="Fetches active Unreal Engine viewport telemetry details (camera location, rotation, fov, and selected actors list) [REQ_SRD_UE5_01].",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="unreal_spawn_actor",
            description="Spawns an actor in Unreal Engine [REQ_SRD_UE5_02]. Supported classes: /Script/Engine.StaticMeshActor, /Script/Engine.PointLight, /Script/Engine.DirectionalLight, /Script/Engine.CameraActor.",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor_class": {
                        "type": "string",
                        "description": "Unreal Engine Actor Class path (e.g. /Script/Engine.PointLight)"
                    },
                    "location": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number", "description": "World X position in centimeters"},
                            "y": {"type": "number", "description": "World Y position in centimeters"},
                            "z": {"type": "number", "description": "World Z position in centimeters"}
                        },
                        "required": ["x", "y", "z"],
                        "description": "Location map containing absolute target coordinates"
                    },
                    "rotation": {
                        "type": "object",
                        "properties": {
                            "pitch": {"type": "number", "description": "Rotation pitch angle"},
                            "yaw": {"type": "number", "description": "Rotation yaw angle"},
                            "roll": {"type": "number", "description": "Rotation roll angle"}
                        },
                        "description": "Optional rotation map"
                    }
                },
                "required": ["actor_class", "location"]
            }
        ),
        types.Tool(
            name="unreal_set_actor_transform",
            description="Sets or modifies the transform (location, rotation) of an actor [REQ_SRD_UE5_03].",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor_path": {
                        "type": "string",
                        "description": "Full object path of the target actor (e.g. PersistentLevel.StaticMeshActor_1)"
                    },
                    "location": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                            "z": {"type": "number"}
                        },
                        "description": "Target coordinate location map"
                    },
                    "rotation": {
                        "type": "object",
                        "properties": {
                            "pitch": {"type": "number"},
                            "yaw": {"type": "number"},
                            "roll": {"type": "number"}
                        },
                        "description": "Target rotation map"
                    }
                },
                "required": ["actor_path"]
            }
        ),
        types.Tool(
            name="unreal_live_coding_trigger",
            description="Triggers Live Coding recompile in Unreal Engine [REQ_SRD_UE5_04]. Pre-condition: Editor must be in idle and PIE must be inactive.",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="unreal_package_project",
            description="Runs RunUAT to build, cook, and package the Unreal project asynchronously [REQ_SRD_UE5_05].",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Absolute Windows path to the .uproject file"
                    }
                },
                "required": ["project_path"]
            }
        ),
        types.Tool(
            name="unreal_import_asset",
            description="Imports an FBX mesh file into the Unreal Engine Content Browser [REQ_SRD_INT_01] [REQ_PID_AST_04].",
            inputSchema={
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Absolute Windows path to the FBX file"
                    },
                    "destination_path": {
                        "type": "string",
                        "description": "Target Content Browser folder (default: /Game/ProceduralAssets/Meshes)"
                    }
                },
                "required": ["filepath"]
            }
        ),
        types.Tool(
            name="unreal_execute_python",
            description="Executes an arbitrary Python script or statement inside the Unreal Editor using the Python Remote Execution socket interface [REQ_SRD_UE5_06].",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The Python script or command string to execute."
                    },
                    "exec_mode": {
                        "type": "string",
                        "enum": ["ExecuteFile", "ExecuteStatement", "EvaluateStatement"],
                        "default": "ExecuteFile",
                        "description": "Execution mode. Use 'ExecuteFile' for multi-line scripts or files, 'ExecuteStatement' to run a single statement, or 'EvaluateStatement' to evaluate an expression and return its value."
                    }
                },
                "required": ["command"]
            }
        ),
        types.Tool(
            name="unreal_get_scene_hierarchy",
            description="Fetches all active actors in the active level to display the scene hierarchy [REQ_SRD_UE5_07].",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="unreal_get_actor_components",
            description="Queries all components and metadata of a target actor [REQ_SRD_UE5_07].",
            inputSchema={
                "type": "object",
                "properties": {
                    "actor_path": {
                        "type": "string",
                        "description": "Full object path of the target actor (e.g. PersistentLevel.StaticMeshActor_1)"
                    }
                },
                "required": ["actor_path"]
            }
        ),
        types.Tool(
            name="unreal_editor_undo",
            description="Triggers the last editor transaction to be undone (Undo / Ctrl+Z) in the Unreal Editor [REQ_SRD_UE5_09].",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="unreal_editor_redo",
            description="Triggers the last undone editor transaction to be redone (Redo / Ctrl+Y) in the Unreal Editor [REQ_SRD_UE5_09].",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """
    Asynchronously handles and routes tool calls to client wrappers or subprocess managers.
    Ensures proper JSON serialization and robust, non-crashing exception handling.
    """
    args = arguments or {}
    logger.info(f"Executing tool {name} with arguments: {args}")
    
    try:
        if name == "unreal_get_viewport_telemetry":
            res = await unreal_client.get_viewport_telemetry()
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_spawn_actor":
            actor_class = args.get("actor_class")
            location = args.get("location")
            rotation = args.get("rotation")
            res = await unreal_client.spawn_actor(actor_class, location, rotation)
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_set_actor_transform":
            actor_path = args.get("actor_path")
            location = args.get("location")
            rotation = args.get("rotation")
            res = await unreal_client.set_actor_transform(actor_path, location, rotation)
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_live_coding_trigger":
            # Safety gate check: query editor status first
            telemetry = await unreal_client.get_viewport_telemetry()
            if not telemetry.get("success") and telemetry.get("error") != "EDITOR_OFFLINE":
                return [types.TextContent(type="text", text=f"Pre-condition Check Failed: {telemetry}")]
                
            # If editor is online, check if game/PIE simulation is running
            if telemetry.get("success"):
                pie_active = await unreal_client.is_pie_active()
                if pie_active:
                    return [types.TextContent(
                        type="text",
                        text="Error: Live Coding cannot be triggered because the editor is currently in PIE (Play In Editor) mode. Please stop the game simulation and try again."
                    )]
                
            logs = []
            def log_collector(line: str):
                logs.append(line)
                
            exit_code = await proc_manager.trigger_live_coding(log_collector)
            return [types.TextContent(
                type="text",
                text=f"Live Coding Completed. Exit Code: {exit_code}\nExecution Output:\n" + "\n".join(logs)
            )]
            
        elif name == "unreal_package_project":
            project_path = args.get("project_path")
            if not project_path:
                return [types.TextContent(type="text", text="Error: Missing project_path argument.")]
                
            logs = []
            def log_collector(line: str):
                logs.append(line)
                
            exit_code = await proc_manager.trigger_run_uat(project_path, log_collector)
            return [types.TextContent(
                type="text",
                text=f"Packaging Completed. Exit Code: {exit_code}\nExecution Output:\n" + "\n".join(logs)
            )]
            
        elif name == "unreal_import_asset":
            filepath = args.get("filepath")
            destination_path = args.get("destination_path", "/Game/ProceduralAssets/Meshes")
            if not filepath:
                return [types.TextContent(type="text", text="Error: Missing filepath argument.")]
                
            res = await unreal_client.import_asset(filepath, destination_path)
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_execute_python":
            command = args.get("command")
            exec_mode = args.get("exec_mode", "ExecuteFile")
            if not command:
                return [types.TextContent(type="text", text="Error: Missing command argument.")]
                
            res = await remote_executor.execute_command(command, exec_mode)
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_get_scene_hierarchy":
            res = await unreal_client.get_scene_hierarchy()
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_get_actor_components":
            actor_path = args.get("actor_path")
            if not actor_path:
                return [types.TextContent(type="text", text="Error: Missing actor_path argument.")]
                
            res = await unreal_client.get_actor_components(actor_path)
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_editor_undo":
            res = await unreal_client.undo()
            return [types.TextContent(type="text", text=str(res))]
            
        elif name == "unreal_editor_redo":
            res = await unreal_client.redo()
            return [types.TextContent(type="text", text=str(res))]
            
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
            
    except Exception as e:
        logger.error(f"Error handling tool call '{name}': {e}")
        return [types.TextContent(type="text", text=f"Error: An unexpected exception occurred: {e}")]

async def main():
    """
    Main entry point initializing asynchronous stdio server transport.
    """
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Unreal Engine MCP Server successfully running on stdio transport...")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        logger.critical(f"Server crash encountered: {e}")
    finally:
        await unreal_client.close()
        await remote_executor.stop_session()

if __name__ == "__main__":
    asyncio.run(main())
