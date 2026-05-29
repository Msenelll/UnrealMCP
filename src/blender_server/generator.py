# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_TDD_ARC_05] Blender Mesh Generator
Injects configuration data into the bpy template and executes Blender CLI worker with a strict timeout
"""

import asyncio
import os
import sys
import tempfile
import logging
from typing import Dict, Any, List

logger = logging.getLogger("BlenderMeshGenerator")

class BlenderMeshGenerator:
    """
    Handles headless execution of Blender worker processes to procedurally generate 3D meshes.
    Enforces inputs validation and safe termination on timeouts (<30s).
    """

    def __init__(self, blender_path: str = "blender"):
        self.blender_path = blender_path

    def _locate_blender(self) -> str:
        """
        Locates the Blender executable on Windows, checking typical install directories.
        """
        if self.blender_path != "blender" and os.path.exists(self.blender_path):
            return self.blender_path
            
        # Common Windows installation directories
        common_paths = [
            "C:\\Program Files\\Blender Foundation\\Blender 4.2\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 4.1\\blender.exe",
            "C:\\Program Files\\Blender Foundation\\Blender 4.0\\blender.exe",
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                logger.info(f"Located Blender installation at: {path}")
                return path
                
        # Default fallback to environment PATH
        return self.blender_path

    def validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates mesh parameters and forces strict defaults.
        """
        shape = params.get("shape", "cube").lower()
        if shape not in ("cube", "sphere", "cylinder"):
            shape = "cube"
            
        size = float(params.get("size", 1.0))
        if size <= 0.0:
            size = 1.0
            
        albedo = params.get("albedo", [0.7, 0.7, 0.7, 1.0])
        if not isinstance(albedo, list) or len(albedo) != 4:
            albedo = [0.7, 0.7, 0.7, 1.0]
            
        metallic = float(params.get("metallic", 0.0))
        metallic = max(0.0, min(1.0, metallic))
        
        roughness = float(params.get("roughness", 0.5))
        roughness = max(0.0, min(1.0, roughness))
        
        output_path = params.get("output_path", "")
        if not output_path:
            # Generate default filepath in Temp
            output_path = os.path.join(tempfile.gettempdir(), f"SM_Proc_{shape}.fbx").replace("\\", "/")
            
        return {
            "shape": shape,
            "size": size,
            "albedo": albedo,
            "metallic": metallic,
            "roughness": roughness,
            "output_path": output_path
        }

    async def generate_mesh(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates mesh and material procedurally in background by launching a headless Blender CLI worker.
        Enforces a 30-second execution timeout.
        [REQ_SRD_BLN_01] / [REQ_TDD_ARC_05] / [AC_03]
        """
        config = self.validate_params(params)
        blender_exe = self._locate_blender()
        
        # Load the base template
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "templates",
            "procedural_mesh.py"
        )
        
        if not os.path.exists(template_path):
            return {
                "success": False,
                "error": "TEMPLATE_MISSING",
                "message": f"Blender template file not found at: {template_path}"
            }
            
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()
                
            # Prepend injected configuration data directly into the script
            injected_script = f"CONFIG_DATA = {config}\n\n{template_content}"
            
            # Write out to a temporary script file
            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w", encoding="utf-8") as temp_f:
                temp_f.write(injected_script)
                temp_script_path = temp_f.name
                
        except Exception as e:
            return {
                "success": False,
                "error": "SCRIPT_GENERATION_FAILED",
                "message": f"Failed to generate temp bpy script: {e}"
            }
            
        # Spawn the headless Blender subprocess with background flags
        cmd = [blender_exe, "--background", "--python", temp_script_path]
        logger.info(f"Launching Blender CLI worker: {' '.join(cmd)}")
        
        process = None
        try:
            # Launch the subprocess asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000 if os.name == 'nt' else 0  # CREATE_NO_WINDOW
            )
            
            # Concurrently read output and wait with a strict 30-second timeout limit
            async def read_stdout():
                success_detected = False
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    decoded = line.decode('utf-8', errors='replace').strip()
                    if "SUCCESS_PROCEDURAL_EXPORT" in decoded:
                        success_detected = True
                    logger.debug(f"[BLENDER_WORKER] {decoded}")
                return success_detected

            # Wait with a strict 30s timeout
            try:
                success_task = asyncio.create_task(read_stdout())
                # asyncio.wait_for will throw TimeoutError if it times out
                success_detected = await asyncio.wait_for(success_task, timeout=30.0)
                await process.wait()
            except asyncio.TimeoutError:
                logger.error("Blender CLI worker timed out after 30 seconds. Forcefully terminating process...")
                try:
                    process.kill()
                    await process.wait()
                except Exception as ex:
                    logger.error(f"Failed to kill Blender process: {ex}")
                return {
                    "success": False,
                    "error": "TIMEOUT",
                    "message": "Procedural generation timed out. Blender execution exceeded the 30-second limit."
                }
                
            # Clean up the temporary python script
            if os.path.exists(temp_script_path):
                os.remove(temp_script_path)
                
            if process.returncode == 0 and success_detected:
                logger.info(f"Blender successfully exported FBX to: {config['output_path']}")
                return {
                    "success": True,
                    "output_path": config["output_path"],
                    "config": config,
                    "message": f"Procedural {config['shape']} mesh successfully generated and exported."
                }
            else:
                stderr_data = await process.stderr.read()
                err_message = stderr_data.decode('utf-8', errors='replace').strip()
                logger.error(f"Blender worker failed with exit code {process.returncode}: {err_message}")
                return {
                    "success": False,
                    "error": "EXECUTION_FAILED",
                    "message": f"Blender worker execution failed with code {process.returncode}. Error: {err_message}"
                }
                
        except Exception as e:
            logger.error(f"Failed to launch or execute Blender process: {e}")
            if process:
                try:
                    process.kill()
                    await process.wait()
                except Exception:
                    pass
            return {
                "success": False,
                "error": "LAUNCH_FAILED",
                "message": f"Blender execution launcher failed: {e}"
            }
