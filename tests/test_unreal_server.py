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
from src.unreal_server.remote_execution_client import UnrealRemoteExecutor

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
        elif "GetLevelViewportCameraInfo" in func:
            return {
                "success": True,
                "data": {
                    "CameraLocation": {"X": 500.0, "Y": -200.0, "Z": 150.0},
                    "CameraRotation": {"Pitch": -10.0, "Yaw": 45.0, "Roll": 0.0}
                }
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
async def test_unreal_client_import_asset():
    """
    Verifies that import_asset successfully maps requests to AssetTools
    and handles simulated fallbacks when editor is offline.
    """
    client = UnrealClient()
    
    # Test offline simulated fallback first (should catch connection exception and return simulation success)
    res_offline = await client.import_asset("C:/Temp/SM_Sphere.fbx")
    assert res_offline["success"] is True
    assert res_offline["asset_path"] == "/Game/ProceduralAssets/Meshes/SM_Sphere.SM_Sphere"
    assert "simulated fallback" in res_offline["message"]
    
    # Test mocked successful online call
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.content_type = "application/json"
    mock_response.json = AsyncMock(return_value={"returnValue": True})
    
    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.close = AsyncMock()
    mock_session.request.return_value.__aenter__.return_value = mock_response
    
    client.session = mock_session
    
    res_online = await client.import_asset("C:/Temp/SM_Cube.fbx")
    assert res_online["success"] is True
    assert "Successfully imported" in res_online["message"]
    
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

# ==========================================
# 4. UnrealRemoteExecutor Unit Tests
# ==========================================

@pytest.mark.asyncio
async def test_unreal_remote_executor_offline():
    """
    Verifies that the executor handles offline scenarios gracefully.
    """
    executor = UnrealRemoteExecutor()
    
    # Mock RemoteExecution to simulate no discovered nodes (empty list)
    with patch("src.unreal_server.remote_execution_client.RemoteExecution") as MockRemoteExec:
        mock_instance = MockRemoteExec.return_value
        mock_instance.remote_nodes = []
        mock_instance.has_command_connection.return_value = False
        
        res = await executor.execute_command("print('test')")
        
        assert res["success"] is False
        assert res["error"] == "EDITOR_OFFLINE"
        
    await executor.stop_session()

@pytest.mark.asyncio
async def test_unreal_remote_executor_mocked_success():
    """
    Verifies successful execution and reconnect handling in remote executor.
    """
    executor = UnrealRemoteExecutor()
    
    # Mock RemoteExecution node discovery and command connection run_command
    with patch("src.unreal_server.remote_execution_client.RemoteExecution") as MockRemoteExec:
        mock_instance = MockRemoteExec.return_value
        mock_instance.remote_nodes = [{"node_id": "test_node_id"}]
        mock_instance.has_command_connection.return_value = False
        mock_instance.run_command.return_value = {"success": True, "result": "mocked_stdout_result"}
        
        res = await executor.execute_command("print('success_test')")
        
        assert res["success"] is True
        assert res["result"] == "mocked_stdout_result"
        
        mock_instance.start.assert_called_once()
        mock_instance.open_command_connection.assert_called_once_with("test_node_id")
        mock_instance.run_command.assert_called_once_with("print('success_test')", unattended=True, exec_mode="ExecuteFile")
        
    await executor.stop_session()

@pytest.mark.asyncio
async def test_unreal_client_get_scene_hierarchy():
    """
    Verifies that get_scene_hierarchy correctly queries and parses the level actors.
    """
    client = UnrealClient()
    
    async def mock_send_request(method, path, payload=None):
        return {
            "success": True,
            "data": {
                "returnValue": [
                    "/Game/Maps/PersistentLevel.StaticMeshActor_1",
                    "/Game/Maps/PersistentLevel.PointLight_1"
                ]
            }
        }
        
    client._send_request = mock_send_request
    
    res = await client.get_scene_hierarchy()
    
    assert res["success"] is True
    assert len(res["actors"]) == 2
    assert res["actors"][0]["name"] == "StaticMeshActor_1"
    assert res["actors"][1]["name"] == "PointLight_1"
    
    await client.close()

@pytest.mark.asyncio
async def test_unreal_client_get_actor_components():
    """
    Verifies that get_actor_components successfully queries and filters actor components from describe metadata.
    """
    client = UnrealClient()
    
    async def mock_send_request(method, path, payload=None):
        return {
            "success": True,
            "data": {
                "name": "MyPointLight",
                "className": "PointLight",
                "properties": [
                    {"name": "LightComponent", "type": "PointLightComponent"},
                    {"name": "RootComponent", "type": "SceneComponent"},
                    {"name": "Intensity", "type": "float"}
                ]
            }
        }
        
    client._send_request = mock_send_request
    
    res = await client.get_actor_components("/Game/Maps/PersistentLevel.PointLight_1")
    
    assert res["success"] is True
    assert res["metadata"]["name"] == "MyPointLight"
    assert res["metadata"]["class"] == "PointLight"
    assert len(res["components"]) == 2
    assert res["components"][0]["name"] == "LightComponent"
    assert res["components"][1]["name"] == "RootComponent"
    
    await client.close()

# ==========================================
# 5. Blueprint Spawning Unit Tests
# ==========================================

@pytest.mark.asyncio
async def test_spawn_actor_invalid_class_path():
    """
    Verifies strict validation of invalid actor class paths.
    """
    client = UnrealClient()
    
    res = await client.spawn_actor("BP_MyActor", {"x": 0.0, "y": 0.0, "z": 0.0})
    assert res["success"] is False
    assert res["error"] == "INVALID_CLASS_PATH"
    assert "Paths must start with" in res["message"]
    
    await client.close()

@pytest.mark.asyncio
async def test_spawn_actor_blueprint_auto_format():
    """
    Verifies auto-formatting expansion of custom Blueprint paths to _C suffix.
    """
    client = UnrealClient()
    
    # Mock successful response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.content_type = "application/json"
    mock_response.json = AsyncMock(return_value={"returnValue": "/Game/Maps.BP_MyActor_C_1"})
    
    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.close = AsyncMock()
    mock_session.request.return_value.__aenter__.return_value = mock_response
    client.session = mock_session
    
    # Pass short path (lacks .BP_MyActor_C)
    res = await client.spawn_actor("/Game/Blueprints/BP_MyActor", {"x": 100.0, "y": 100.0, "z": 0.0})
    
    assert res["success"] is True
    assert "BP_MyActor.BP_MyActor_C" in res["message"]
    
    # Verify exact called string
    called_args = mock_session.request.call_args[1]
    assert called_args["json"]["parameters"]["ActorClass"] == "/Game/Blueprints/BP_MyActor.BP_MyActor_C"
    
    await client.close()

@pytest.mark.asyncio
async def test_spawn_actor_asset_not_found_500():
    """
    Verifies that HTTP_500 from the Remote Control Web Server translates to ASSET_NOT_FOUND.
    """
    client = UnrealClient()
    
    async def mock_send_request(method, path, payload=None):
        return {
            "success": False,
            "error": "HTTP_500",
            "message": "Internal Server Error"
        }
    client._send_request = mock_send_request
    
    res = await client.spawn_actor("/Game/Blueprints/BP_Invalid", {"x": 0.0, "y": 0.0, "z": 0.0})
    
    assert res["success"] is False
    assert res["error"] == "ASSET_NOT_FOUND"
    assert "verify that the Blueprint asset path exists" in res["message"]
    
    await client.close()



