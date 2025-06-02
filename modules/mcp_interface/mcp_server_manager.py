"""
MCP Server Manager for UOR Evolution

Manages connections to external MCP servers and handles server lifecycle.
"""

import asyncio
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


@dataclass
class MCPServerConnection:
    """Represents a connection to an MCP server"""
    server_id: str
    server_params: StdioServerParameters
    session: Optional[ClientSession] = None
    connected_at: Optional[datetime] = None
    available_tools: List[Dict[str, Any]] = field(default_factory=list)
    available_resources: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "disconnected"
    
    def is_connected(self) -> bool:
        """Check if server is connected"""
        return self.status == "connected" and self.session is not None


class MCPServerManager:
    """
    Manages multiple MCP server connections for the consciousness framework.
    
    This manager handles:
    - Server discovery and connection
    - Tool and resource enumeration
    - Connection lifecycle management
    - Server health monitoring
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MCP Server Manager.
        
        Args:
            config: Configuration dictionary for server management
        """
        self.config = config or {}
        self.servers: Dict[str, MCPServerConnection] = {}
        self.trusted_servers: Set[str] = set(
            self.config.get('trusted_servers', [])
        )
        self._running_tasks: List[asyncio.Task] = []
        
    async def connect_server(
        self, 
        server_id: str, 
        command: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None
    ) -> MCPServerConnection:
        """
        Connect to an MCP server.
        
        Args:
            server_id: Unique identifier for the server
            command: Command to start the server
            args: Command arguments
            env: Environment variables
            
        Returns:
            MCPServerConnection object
        """
        if server_id in self.servers and self.servers[server_id].is_connected():
            logger.info(f"Server {server_id} already connected")
            return self.servers[server_id]
            
        # Create server parameters
        server_params = StdioServerParameters(
            command=command,
            args=args or [],
            env=env
        )
        
        # Create connection object
        connection = MCPServerConnection(
            server_id=server_id,
            server_params=server_params
        )
        
        try:
            # Connect to the server
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    connection.session = session
                    connection.connected_at = datetime.now()
                    connection.status = "connected"
                    
                    # Initialize the connection
                    await session.initialize()
                    
                    # Discover available tools
                    tools_response = await session.list_tools()
                    connection.available_tools = [
                        tool.model_dump() for tool in tools_response.tools
                    ]
                    
                    # Discover available resources
                    resources_response = await session.list_resources()
                    connection.available_resources = [
                        resource.model_dump() for resource in resources_response.resources
                    ]
                    
                    # Store the connection
                    self.servers[server_id] = connection
                    
                    logger.info(
                        f"Connected to server {server_id} with "
                        f"{len(connection.available_tools)} tools and "
                        f"{len(connection.available_resources)} resources"
                    )
                    
                    # Keep the connection alive
                    await self._maintain_connection(connection)
                    
        except Exception as e:
            logger.error(f"Failed to connect to server {server_id}: {e}")
            connection.status = "error"
            connection.session = None
            raise
            
        return connection
    
    async def disconnect_server(self, server_id: str) -> bool:
        """
        Disconnect from an MCP server.
        
        Args:
            server_id: Server identifier
            
        Returns:
            True if disconnected successfully
        """
        if server_id not in self.servers:
            logger.warning(f"Server {server_id} not found")
            return False
            
        connection = self.servers[server_id]
        connection.status = "disconnected"
        connection.session = None
        
        # Remove from active servers
        del self.servers[server_id]
        
        logger.info(f"Disconnected from server {server_id}")
        return True
    
    async def list_all_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from all connected servers.
        
        Returns:
            List of tool specifications with server information
        """
        all_tools = []
        
        for server_id, connection in self.servers.items():
            if connection.is_connected():
                for tool in connection.available_tools:
                    tool_info = tool.copy()
                    tool_info['server_id'] = server_id
                    all_tools.append(tool_info)
                    
        return all_tools
    
    async def list_all_resources(self) -> List[Dict[str, Any]]:
        """
        List all available resources from all connected servers.
        
        Returns:
            List of resource specifications with server information
        """
        all_resources = []
        
        for server_id, connection in self.servers.items():
            if connection.is_connected():
                for resource in connection.available_resources:
                    resource_info = resource.copy()
                    resource_info['server_id'] = server_id
                    all_resources.append(resource_info)
                    
        return all_resources
    
    async def invoke_tool(
        self, 
        server_id: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke a tool on a specific server.
        
        Args:
            server_id: Server identifier
            tool_name: Name of the tool to invoke
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        if server_id not in self.servers:
            raise ValueError(f"Server {server_id} not found")
            
        connection = self.servers[server_id]
        if not connection.is_connected():
            raise ConnectionError(f"Server {server_id} is not connected")
            
        if not connection.session:
            raise ConnectionError(f"No active session for server {server_id}")
            
        try:
            # Call the tool
            result = await connection.session.call_tool(tool_name, arguments)
            
            return {
                'success': True,
                'server_id': server_id,
                'tool_name': tool_name,
                'result': result.model_dump() if hasattr(result, 'model_dump') else result
            }
            
        except Exception as e:
            logger.error(f"Tool invocation failed: {e}")
            return {
                'success': False,
                'server_id': server_id,
                'tool_name': tool_name,
                'error': str(e)
            }
    
    async def read_resource(
        self, 
        server_id: str, 
        resource_uri: str
    ) -> Dict[str, Any]:
        """
        Read a resource from a specific server.
        
        Args:
            server_id: Server identifier
            resource_uri: URI of the resource to read
            
        Returns:
            Resource content
        """
        if server_id not in self.servers:
            raise ValueError(f"Server {server_id} not found")
            
        connection = self.servers[server_id]
        if not connection.is_connected():
            raise ConnectionError(f"Server {server_id} is not connected")
            
        if not connection.session:
            raise ConnectionError(f"No active session for server {server_id}")
            
        try:
            # Read the resource
            result = await connection.session.read_resource(resource_uri)
            
            return {
                'success': True,
                'server_id': server_id,
                'resource_uri': resource_uri,
                'content': result.model_dump() if hasattr(result, 'model_dump') else result
            }
            
        except Exception as e:
            logger.error(f"Resource read failed: {e}")
            return {
                'success': False,
                'server_id': server_id,
                'resource_uri': resource_uri,
                'error': str(e)
            }
    
    async def _maintain_connection(self, connection: MCPServerConnection):
        """
        Maintain a connection to a server.
        
        Args:
            connection: Server connection to maintain
        """
        # This is a placeholder for connection maintenance logic
        # In a real implementation, this would handle reconnection,
        # heartbeats, and connection monitoring
        while connection.is_connected():
            await asyncio.sleep(30)  # Check every 30 seconds
            
    def get_server_status(self, server_id: str) -> Dict[str, Any]:
        """
        Get the status of a specific server.
        
        Args:
            server_id: Server identifier
            
        Returns:
            Server status information
        """
        if server_id not in self.servers:
            return {
                'server_id': server_id,
                'status': 'not_found'
            }
            
        connection = self.servers[server_id]
        return {
            'server_id': server_id,
            'status': connection.status,
            'connected_at': connection.connected_at.isoformat() if connection.connected_at else None,
            'tools_count': len(connection.available_tools),
            'resources_count': len(connection.available_resources)
        }
    
    def get_all_server_statuses(self) -> List[Dict[str, Any]]:
        """
        Get status of all servers.
        
        Returns:
            List of server status information
        """
        return [
            self.get_server_status(server_id) 
            for server_id in self.servers.keys()
        ]
    
    async def shutdown(self):
        """Shutdown all server connections"""
        logger.info("Shutting down MCP Server Manager")
        
        # Cancel all running tasks
        for task in self._running_tasks:
            task.cancel()
            
        # Disconnect all servers
        server_ids = list(self.servers.keys())
        for server_id in server_ids:
            await self.disconnect_server(server_id)
            
        logger.info("MCP Server Manager shutdown complete")
