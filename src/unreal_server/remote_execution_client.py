# -*- coding: utf-8 -*-
"""
Ludus Magnus - Dual MCP Server Suite
[REQ_TDD_ARC_08] Unreal Engine Python Remote Execution Client
Asynchronous wrapper around Epic's socket-based remote execution protocol
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from src.unreal_server.remote_execution import (
    RemoteExecution,
    RemoteExecutionConfig,
    MODE_EXEC_FILE,
    MODE_EXEC_STATEMENT,
    MODE_EVAL_STATEMENT
)

logger = logging.getLogger("UnrealRemoteExecutor")

class UnrealRemoteExecutor:
    """
    Manages non-blocking discovery and execution of Python commands inside Unreal Editor
    via TCP/UDP socket remote execution.
    Connections are cached to ensure extremely low latency (<10ms per execution).
    """

    def __init__(self):
        self.remote_exec: Optional[RemoteExecution] = None
        self.connected_node_id: Optional[str] = None
        self.lock = asyncio.Lock()

    async def _discover_and_connect(self) -> bool:
        """
        Starts discovery and attempts to connect to the first available Unreal Editor node.
        Runs safely inside an lock to prevent concurrent connection attempts.
        """
        if self.remote_exec and self.remote_exec.has_command_connection():
            return True

        logger.info("Initializing new Python Remote Execution session...")
        
        # Stop any stale sessions
        await self.stop_session()

        # Initialize Epic's RemoteExecution class
        # Node discovery UDP multicast: 239.0.0.1:6766
        # Command TCP listener: 127.0.0.1:6776
        config = RemoteExecutionConfig()
        self.remote_exec = RemoteExecution(config=config)
        
        # Start UDP listener thread
        await asyncio.to_thread(self.remote_exec.start)

        # Wait up to 3.0 seconds for UDP pong discovery
        discovered = False
        for i in range(30):
            nodes = self.remote_exec.remote_nodes
            if nodes:
                logger.info(f"Discovered Unreal Editor nodes: {nodes}")
                self.connected_node_id = nodes[0]["node_id"]
                discovered = True
                break
            await asyncio.sleep(0.1)

        if not discovered:
            logger.error("No active Unreal Editor nodes discovered via UDP multicast. Please verify 'Allow Python Remote Execution' is enabled in Unreal Project Settings.")
            await asyncio.to_thread(self.remote_exec.stop)
            self.remote_exec = None
            return False

        # Establish TCP Command Connection
        try:
            logger.info(f"Establishing TCP command connection to node {self.connected_node_id}...")
            await asyncio.to_thread(self.remote_exec.open_command_connection, self.connected_node_id)
            logger.info("TCP command connection successfully established!")
            return True
        except Exception as e:
            logger.error(f"Failed to open TCP command connection: {e}")
            await asyncio.to_thread(self.remote_exec.stop)
            self.remote_exec = None
            self.connected_node_id = None
            return False

    async def execute_command(
        self, 
        command: str, 
        exec_mode: str = MODE_EXEC_FILE, 
        unattended: bool = True
    ) -> Dict[str, Any]:
        """
        Executes a Python command string asynchronously inside the Unreal Editor.
        Automatically reconnects if the connection has dropped.
        """
        async with self.lock:
            # Ensure we are connected
            connected = await self._discover_and_connect()
            if not connected or not self.remote_exec:
                return {
                    "success": False,
                    "error": "EDITOR_OFFLINE",
                    "result": "Unreal Editor is offline or Python Remote Execution is disabled in Project Settings."
                }

            try:
                # Execute command via thread pool to keep asyncio event loop non-blocking
                logger.info(f"Sending Python script to Unreal Editor (mode={exec_mode})...")
                res = await asyncio.to_thread(
                    self.remote_exec.run_command,
                    command,
                    unattended=unattended,
                    exec_mode=exec_mode
                )
                return res
            except Exception as e:
                logger.error(f"TCP communication error during execution: {e}")
                # Reset connection on failure so it reconnects next time
                await self.stop_session()
                return {
                    "success": False,
                    "error": "COMMUNICATION_ERROR",
                    "result": f"Failed to communicate with Unreal Editor over socket: {e}"
                }

    async def stop_session(self) -> None:
        """
        Safely stops the remote execution threads and closes socket connections.
        """
        if self.remote_exec:
            logger.info("Stopping Python Remote Execution session...")
            try:
                await asyncio.to_thread(self.remote_exec.stop)
            except Exception as e:
                logger.warning(f"Error during remote execution cleanup: {e}")
            self.remote_exec = None
            self.connected_node_id = None
