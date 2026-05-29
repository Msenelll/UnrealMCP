# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
Verification Tests for Unreal Server Suite
Covers CoordinateConverter, UnrealClient, and SubprocessManager
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from src.common.transforms import CoordinateConverter
from src.unreal_server.client import UnrealClient
from src.unreal_server.execution import SubprocessManager

# ==========================================
# 1. CoordinateConverter Unit Tests
# ==========================================

def test_coordinate_converter_translation():
    """
    Verifies meter-to-centimeter scale transformation logic.
    """
    b_loc = {"x": 1.5, "y": -2.0, "z": 0.5}
    u_loc = CoordinateConverter.blender_to_unreal_location(b_loc)
    
    # Scale conversion check (meter -> centimeter)
    assert u_loc["x"] == 150.0
    assert u_loc["y"] == -200.0
    assert u_loc["z"] == 50.0

def test_coordinate_converter_rotation():
    """
    Verifies eksen angles conversion mapping.
    """
    b_rot = {"x": 10.0, "y": 20.0, "z": 30.0}
    u_rot = CoordinateConverter.blender_to_unreal_rotation(b_rot)
    
    assert u_rot["pitch"] == 20.0  # Blender Y -> Unreal Pitch
    assert u_rot["yaw"] == 30.0    # Blender Z -> Unreal Yaw
    assert u_rot["roll"] == 10.0   # Blender X -> Unreal Roll

# ==========================================
# 2. UnrealClient Entegrasyon Tests
# ==========================================

@pytest.mark.asyncio
async def test_unreal_client_editor_offline():
    """
    Verifies that the client returns a safe EDITOR_OFFLINE response
    when the editor is closed (port 30010 offline).
    """
    # Instantiate client targeting a dead port
    client = UnrealClient(base_url="http://localhost:59999")
    res = await client.get_viewport_telemetry()
    
    assert res["success"] is False
    assert res["error"] == "EDITOR_OFFLINE"
    assert "Unreal Editor is not running" in res["message"]
    
    await client.close()

@pytest.mark.asyncio
async def test_unreal_client_mocked_spawn():
    """
    Verifies correct JSON payload parsing and formatting during actor spawning.
    """
    client = UnrealClient()
    
    # Mock connection session and response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.content_type = "application/json"
    mock_response.json = AsyncMock(return_value={"returnValue": "/Game/Maps/PersistentLevel.PointLight_1"})
    
    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.close = AsyncMock()
    # Mock the 'async with session.request(...) as response' context manager
    mock_session.request.return_value.__aenter__.return_value = mock_response
    
    client.session = mock_session
    
    res = await client.spawn_actor(
        actor_class="/Script/Engine.PointLight",
        location={"x": 10.0, "y": 20.0, "z": 30.0}
    )
    
    assert res["success"] is True
    assert res["actor_path"] == "/Game/Maps/PersistentLevel.PointLight_1"
    
    # Verify request payload format matches EditorActorSubsystem standards
    mock_session.request.assert_called_once()
    called_args = mock_session.request.call_args[1]
    assert called_args["json"]["functionName"] == "SpawnActorFromClass"
    assert called_args["json"]["parameters"]["Location"]["X"] == 10.0
    
    await client.close()

@pytest.mark.asyncio
async def test_unreal_client_get_viewport_telemetry():
    """
    Verifies that get_viewport_telemetry successfully fetches camera data
    and selected actors when the Remote Control Web Server responds correctly.
    """
    client = UnrealClient()
    
    # Direct mock of _send_request to simulate active UE5 subsystems
    async def mock_send_request(method, path, payload=None):
        payload = payload or {}
        func = payload.get("functionName", "")
        if "GetSelectedLevelActors" in func:
            return {
                "success": True,
                "data": {"returnValue": ["/Game/Maps/PersistentLevel.StaticMeshActor_1"]}
            }
        elif "GetActiveViewportCameraLocation" in func:
            return {
                "success": True,
                "data": {"returnValue": {"X": 500.0, "Y": -200.0, "Z": 150.0}}
            }
        elif "GetActiveViewportCameraRotation" in func:
            return {
                "success": True,
                "data": {"returnValue": {"Pitch": -10.0, "Yaw": 45.0, "Roll": 0.0}}
            }
        return {"success": False}
        
    client._send_request = mock_send_request
    
    res = await client.get_viewport_telemetry()
    
    assert res["success"] is True
    assert res["camera"]["location"]["x"] == 500.0
    assert res["camera"]["rotation"]["pitch"] == -10.0
    assert len(res["selected_actors"]) == 1
    assert res["selected_actors"][0]["name"] == "StaticMeshActor_1"
    
    await client.close()

@pytest.mark.asyncio
async def test_unreal_client_is_pie_active_true():
    """
    Verifies that is_pie_active returns True when UEDPIE_ prefix is in actor path.
    """
    client = UnrealClient()
    
    async def mock_send_request(method, path, payload=None):
        return {
            "success": True,
            "data": {"returnValue": ["/Game/Maps/UEDPIE_0_MainLevel.MainLevel:PersistentLevel.StaticMeshActor_1"]}
        }
    client._send_request = mock_send_request
    
    pie_active = await client.is_pie_active()
    assert pie_active is True
    await client.close()

@pytest.mark.asyncio
async def test_unreal_client_is_pie_active_false():
    """
    Verifies that is_pie_active returns False when UEDPIE_ prefix is absent.
    """
    client = UnrealClient()
    
    async def mock_send_request(method, path, payload=None):
        return {
            "success": True,
            "data": {"returnValue": ["/Game/Maps/PersistentLevel.StaticMeshActor_1"]}
        }
    client._send_request = mock_send_request
    
    pie_active = await client.is_pie_active()
    assert pie_active is False
    await client.close()

# ==========================================
# 3. SubprocessManager Unit Tests
# ==========================================

@pytest.mark.asyncio
async def test_subprocess_manager_simulated_live_coding():
    """
    Verifies that SubprocessManager safely handles simulated recompilations
    and aggregates execution logs without thread blocking.
    """
    manager = SubprocessManager()
    logs = []
    
    def log_callback(line: str):
        logs.append(line)
        
    exit_code = await manager.trigger_live_coding(log_callback)
    
    assert exit_code == 0
    assert len(logs) > 0
    assert any("LiveCoding" in log for log in logs)

@pytest.mark.asyncio
async def test_subprocess_manager_simulated_run_uat():
    """
    Verifies simulated RunUAT packaging log stream operations.
    """
    manager = SubprocessManager()
    logs = []
    
    def log_callback(line: str):
        logs.append(line)
        
    exit_code = await manager.trigger_run_uat(
        project_path="C:/repo/MyProject/MyProject.uproject",
        log_callback=log_callback
    )
    
    assert exit_code == 0
    assert len(logs) > 0
    assert any("RunUAT" in log for log in logs)
