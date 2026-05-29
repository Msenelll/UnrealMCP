# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_TDD_ARC_01] Blender MCP Server Entry Point
Initializes stdio server transport, registers tools, and routes procedural calls asynchronously
"""

import asyncio
import sys
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from src.blender_server.generator import BlenderMeshGenerator

# Configure enterprise logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr  # Direct logging to stderr so it does not interfere with stdio channels
)
logger = logging.getLogger("BlenderMCPServer")

# Initialize Server instance
server = Server("blender-mcp-server")

# Instantiate generator class
mesh_generator = BlenderMeshGenerator()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    Registers the core tool for otonom procedural 3D mesh and PBR material synthesis.
    """
    return [
        types.Tool(
            name="blender_generate_procedural_mesh",
            description="Generates a 3D geometric mesh and parameterized PBR material procedurally using headless Blender [REQ_SRD_BLN_01] [REQ_SRD_BLN_02].",
            inputSchema={
                "type": "object",
                "properties": {
                    "shape": {
                        "type": "string",
                        "description": "Geometric primitive shape: cube, sphere, or cylinder",
                        "enum": ["cube", "sphere", "cylinder"]
                    },
                    "size": {
                        "type": "number",
                        "description": "Outer dimensions or scale of the primitive (default: 1.0)"
                    },
                    "albedo": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "RGBA base albedo color array, values between 0.0 and 1.0 (default: [0.7, 0.7, 0.7, 1.0])"
                    },
                    "metallic": {
                        "type": "number",
                        "description": "Metallic value of the PBR material, between 0.0 and 1.0 (default: 0.0)"
                    },
                    "roughness": {
                        "type": "number",
                        "description": "Roughness value of the PBR material, between 0.0 and 1.0 (default: 0.5)"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Target file path to export the FBX. Optional; defaults to system temp path."
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """
    Routes tool calls asynchronously to the BlenderMeshGenerator engine, wrapping logs and returning responses.
    """
    args = arguments or {}
    logger.info(f"Executing tool {name} with arguments: {args}")
    
    try:
        if name == "blender_generate_procedural_mesh":
            res = await mesh_generator.generate_mesh(args)
            return [types.TextContent(type="text", text=str(res))]
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
            
    except Exception as e:
        logger.error(f"Error handling tool call '{name}': {e}")
        return [types.TextContent(type="text", text=f"Error: An unexpected exception occurred: {e}")]

async def main():
    """
    Main entry point initializing stdio server transport.
    """
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Blender MCP Server successfully running on stdio transport...")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        logger.critical(f"Server crash encountered: {e}")

if __name__ == "__main__":
    asyncio.run(main())
