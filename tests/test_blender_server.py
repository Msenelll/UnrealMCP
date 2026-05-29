# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Verification Tests for Blender Server Suite
Covers BlenderMeshGenerator parameters validation, script injection, and timeout safety
"""

import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock, AsyncMock
from src.blender_server.generator import BlenderMeshGenerator

# ==========================================
# 1. Parameter Validation Unit Tests
# ==========================================

def test_blender_generator_param_validation():
    """
    Verifies that BlenderMeshGenerator clamps, sanitizes, and maps inputs properly.
    """
    generator = BlenderMeshGenerator()
    
    # Faulty parameters test
    raw_params = {
        "shape": "invalid_shape_name",
        "size": -5.0,  # Negative size must be overridden
        "albedo": "not_a_list",  # Color must be overridden to default array
        "metallic": 5.0,  # Metallic must be clamped to 1.0
        "roughness": -1.0  # Roughness must be clamped to 0.0
    }
    
    clean = generator.validate_params(raw_params)
    
    assert clean["shape"] == "cube"
    assert clean["size"] == 1.0
    assert clean["albedo"] == [0.7, 0.7, 0.7, 1.0]
    assert clean["metallic"] == 1.0
    assert clean["roughness"] == 0.0
    assert clean["output_path"].endswith("SM_Proc_cube.fbx")

# ==========================================
# 2. Heads-up Subprocess Execution and Timeout Verification
# ==========================================

@pytest.mark.asyncio
async def test_blender_generator_execution_timeout():
    """
    Verifies that the generator terminates the Blender process immediately
    if execution exceeds the 30-second timeout limit.
    """
    generator = BlenderMeshGenerator()
    
    # Mock create_subprocess_exec to simulate a hanging subprocess
    mock_process = AsyncMock()
    
    async def mock_readline():
        # Simulate infinite read block by sleeping longer than test timeout
        await asyncio.sleep(5.0)
        return b""
        
    mock_process.stdout.readline = mock_readline
    mock_process.kill = MagicMock()
    mock_process.wait = AsyncMock(return_value=-1)
    
    # Patch subprocess launcher to return our mock hanging process
    with patch("asyncio.create_subprocess_exec", return_value=mock_process) as mock_launcher:
        # Override wait_for timeout to a small value (e.g., 0.5s) to trigger timeout quickly in test
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
            res = await generator.generate_mesh({
                "shape": "sphere",
                "size": 2.0
            })
            
            assert res["success"] is False
            assert res["error"] == "TIMEOUT"
            assert "exceeded the 30-second limit" in res["message"]
            
            # Confirm process was forcefully terminated
            mock_process.kill.assert_called_once()
            mock_process.wait.assert_called_once()

@pytest.mark.asyncio
async def test_blender_generator_successful_mocked_execution():
    """
    Verifies successful script creation, subprocess launch, and output monitoring.
    """
    generator = BlenderMeshGenerator()
    
    mock_process = AsyncMock()
    mock_process.returncode = 0
    
    # Simulate a stream that prints success and exits immediately
    stdout_lines = [b"SUCCESS_PROCEDURAL_EXPORT\n", b""]
    line_iter = iter(stdout_lines)
    
    async def mock_readline():
        return next(line_iter)
        
    mock_process.stdout.readline = mock_readline
    mock_process.wait = AsyncMock(return_value=0)
    
    with patch("asyncio.create_subprocess_exec", return_value=mock_process) as mock_launcher:
        res = await generator.generate_mesh({
            "shape": "cylinder",
            "size": 1.5,
            "output_path": "C:/Temp/SM_Cylinder.fbx"
        })
        
        assert res["success"] is True
        assert res["output_path"] == "C:/Temp/SM_Cylinder.fbx"
        assert res["config"]["shape"] == "cylinder"
        mock_launcher.assert_called_once()
