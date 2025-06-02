"""
MCP (Model Context Protocol) Interface Module for UOR Evolution

This module provides integration between the UOR Evolution consciousness framework
and external MCP servers, enabling the consciousness to interact with external tools
and services through a standardized protocol.

Components:
- MCPConsciousnessBridge: Bridge between consciousness and MCP protocol
- MCPServerManager: Manages connections to MCP servers
- MCPToolOrchestrator: Orchestrates tool usage and selection
- ConsciousnessMCPServer: Exposes UOR Evolution as an MCP server
"""

from .mcp_consciousness_bridge import MCPConsciousnessBridge
from .mcp_server_manager import MCPServerManager
from .mcp_tool_orchestrator import MCPToolOrchestrator

__all__ = [
    'MCPConsciousnessBridge',
    'MCPServerManager',
    'MCPToolOrchestrator'
]

# Version information
__version__ = '1.0.0'
__author__ = 'UOR Evolution Team'
