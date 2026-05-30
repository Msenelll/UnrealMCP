# USER_TODO - UnrealMCP v2.0 Setup and Editor Actions

This document outlines the specific editor configurations and manual setups required on your end to utilize and test the advanced features of **UnrealMCP v2.0**. Since these settings belong to your local Unreal Engine Editor environment, they cannot be configured programmatically by the MCP server.

---

## 1. Required Editor Plugins Configuration

To enable HTTP/REST and Socket-based Python execution:

1. Open your **UE5 Project**.
2. Go to **Edit -> Plugins**.
3. Search for and **Enable** the following plugins:
   * **Remote Control API** (Provides HTTP/REST endpoints for Spawning, Transform, and Undo/Redo)
   * **Python Editor Script Plugin** (Provides Python Remote Execution socket bridge)
4. Restart the Unreal Editor if prompted.

---

## 2. Remote Python Execution Settings (For Socket Execution)

To allow the `unreal_execute_python` tool to execute scripts directly within the Editor:

1. Go to **Edit -> Project Settings**.
2. Scroll down to **Plugins** and select **Python**.
3. Under **Remote Execution**, enable **Enable Remote Execution?**.
4. Set the **Multicast Bind Address** to `0.0.0.0` or `127.0.0.1` if you are working locally.
5. In the Unreal Console (at the bottom of the Editor), verify that the python listener has started.

---

## 3. Web Remote Control Server Activation

Ensure the Remote Control HTTP Server is active and listening on port `30010`:

1. In the Unreal Editor Command Console (Cmd line), enter:
   ```cmd
   WebControl.StartServer
   ```
2. You should see a log confirmation: `Remote Control Web Server started on port 30010`.

---

## 4. Testing Custom Blueprint Spawning

To test PBI_008 dynamic Spawning:
1. Create a simple Blueprint Actor class (e.g., `BP_TestObstacle`) inside your content folder under `/Game/Blueprints/`.
2. Save and compile it.
3. You can now spawn this custom asset from the client using:
   * Class Path: `/Game/Blueprints/BP_TestObstacle`
   * The MCP server will automatically resolve this to `/Game/Blueprints/BP_TestObstacle.BP_TestObstacle_C` and place it at the requested viewport coordinate.

---

## 5. Testing Editor Undo/Redo

To test PBI_009 Undo/Redo:
1. Call the `unreal_spawn_actor` or `unreal_set_actor_transform` tool to spawn or move an actor in the level.
2. Call the `unreal_editor_undo` tool. You will instantly see the actor disappear or return to its original coordinate in the viewport.
3. Call the `unreal_editor_redo` tool. The actor will reappear or move back to the transformed coordinate.
