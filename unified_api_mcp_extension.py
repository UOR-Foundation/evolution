"""
MCP Extension for Unified API

This file contains the MCP-related extensions to the UnifiedUORAPI class.
These methods should be added to the UnifiedUORAPI class in unified_api.py
"""

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from modules.mcp_interface import MCPServerManager, MCPConsciousnessBridge, MCPToolOrchestrator
from .unified_api import APIResponse, SystemStatus


class MCPExtension:
    """MCP-related methods for UnifiedUORAPI"""
    
    def _initialize_mcp_components(self):
        """Initialize MCP components - call this in __init__ when mode is MCP_ENABLED"""
        # MCP components
        self.mcp_server_manager = MCPServerManager()
        self.mcp_consciousness_bridge = MCPConsciousnessBridge(self.consciousness_core)
        self.mcp_tool_orchestrator = MCPToolOrchestrator(
            self.mcp_server_manager,
            self.mcp_consciousness_bridge
        )
        
        # Initialize MCP state in system state
        if not hasattr(self.system_state, 'mcp_state'):
            self.system_state.mcp_state = {
                'connected_servers': [],
                'available_tools': [],
                'tool_usage_history': [],
                'active_plans': []
            }
    
    # ==================== MCP SERVER OPERATIONS ====================
    
    def connect_mcp_server(
        self, 
        server_id: str,
        command: str,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None
    ) -> APIResponse:
        """
        Connect to an MCP server.
        
        Args:
            server_id: Unique identifier for the server
            command: Command to start the server
            args: Command arguments
            env: Environment variables
            
        Returns:
            APIResponse with connection status
        """
        try:
            # Run async operation in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            connection = loop.run_until_complete(
                self.mcp_server_manager.connect_server(server_id, command, args, env)
            )
            
            # Update system state
            self.system_state.mcp_state['connected_servers'].append({
                'server_id': server_id,
                'connected_at': connection.connected_at.isoformat() if connection.connected_at else None,
                'status': connection.status,
                'tools_count': len(connection.available_tools),
                'resources_count': len(connection.available_resources)
            })
            
            return APIResponse(
                success=True,
                data={
                    'server_id': server_id,
                    'status': connection.status,
                    'available_tools': connection.available_tools,
                    'available_resources': connection.available_resources
                },
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"MCP server connection failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def disconnect_mcp_server(self, server_id: str) -> APIResponse:
        """
        Disconnect from an MCP server.
        
        Args:
            server_id: Server identifier
            
        Returns:
            APIResponse with disconnection status
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            success = loop.run_until_complete(
                self.mcp_server_manager.disconnect_server(server_id)
            )
            
            if success:
                # Update system state
                self.system_state.mcp_state['connected_servers'] = [
                    s for s in self.system_state.mcp_state['connected_servers']
                    if s['server_id'] != server_id
                ]
            
            return APIResponse(
                success=success,
                data={'server_id': server_id, 'disconnected': success},
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"MCP server disconnection failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def list_mcp_servers(self) -> APIResponse:
        """
        List all connected MCP servers.
        
        Returns:
            APIResponse with server list
        """
        try:
            server_statuses = self.mcp_server_manager.get_all_server_statuses()
            
            return APIResponse(
                success=True,
                data={
                    'servers': server_statuses,
                    'total_connected': len([s for s in server_statuses if s['status'] == 'connected'])
                },
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Failed to list MCP servers: {str(e)}",
                system_status=self.status
            )
    
    # ==================== MCP TOOL OPERATIONS ====================
    
    def discover_mcp_tools(self) -> APIResponse:
        """
        Discover all available tools from connected MCP servers.
        
        Returns:
            APIResponse with tool list
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            tools = loop.run_until_complete(
                self.mcp_server_manager.list_all_tools()
            )
            
            # Update system state
            self.system_state.mcp_state['available_tools'] = tools
            
            # Analyze tools with consciousness
            tool_analyses = []
            for tool in tools:
                analysis = self.mcp_consciousness_bridge.analyze_tool_capabilities(tool)
                tool_analyses.append({
                    'tool': tool,
                    'analysis': {
                        'capability_score': analysis.capability_score,
                        'consciousness_compatibility': analysis.consciousness_compatibility,
                        'recommended_usage': analysis.recommended_usage
                    }
                })
            
            return APIResponse(
                success=True,
                data={
                    'tools': tools,
                    'total_tools': len(tools),
                    'tool_analyses': tool_analyses
                },
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Tool discovery failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def invoke_mcp_tool(
        self,
        goal: str,
        tool_name: Optional[str] = None,
        arguments: Optional[Dict[str, Any]] = None,
        server_id: Optional[str] = None
    ) -> APIResponse:
        """
        Invoke an MCP tool with consciousness-aware selection.
        
        Args:
            goal: The goal to achieve
            tool_name: Specific tool to use (optional)
            arguments: Tool arguments
            server_id: Specific server to use (optional)
            
        Returns:
            APIResponse with tool execution result
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                self.mcp_tool_orchestrator.execute_single_tool(
                    goal, tool_name, arguments, server_id
                )
            )
            
            # Update tool usage history
            self.system_state.mcp_state['tool_usage_history'].append({
                'timestamp': datetime.now().isoformat(),
                'goal': goal,
                'tool_name': result.tool_name,
                'server_id': result.server_id,
                'status': result.status.value,
                'execution_time': result.execution_time
            })
            
            return APIResponse(
                success=result.status.value == "success",
                data={
                    'tool_name': result.tool_name,
                    'server_id': result.server_id,
                    'result': result.result_data,
                    'execution_time': result.execution_time,
                    'consciousness_integration': result.consciousness_integration
                },
                error=result.error,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Tool invocation failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def create_mcp_execution_plan(
        self,
        goal: str,
        constraints: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Create an execution plan for achieving a goal using MCP tools.
        
        Args:
            goal: The goal to achieve
            constraints: Any constraints on execution
            
        Returns:
            APIResponse with execution plan
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            plan = loop.run_until_complete(
                self.mcp_tool_orchestrator.create_execution_plan(goal, constraints)
            )
            
            # Store plan in system state
            self.system_state.mcp_state['active_plans'].append({
                'plan_id': plan.plan_id,
                'goal': plan.goal,
                'steps': len(plan.steps),
                'created_at': plan.created_at.isoformat()
            })
            
            return APIResponse(
                success=True,
                data={
                    'plan_id': plan.plan_id,
                    'goal': plan.goal,
                    'steps': plan.steps,
                    'dependencies': plan.dependencies
                },
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Plan creation failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def execute_mcp_plan(
        self,
        plan_id: str,
        parallel: bool = True
    ) -> APIResponse:
        """
        Execute a tool execution plan.
        
        Args:
            plan_id: ID of the plan to execute
            parallel: Whether to execute independent steps in parallel
            
        Returns:
            APIResponse with execution results
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(
                self.mcp_tool_orchestrator.execute_plan(plan_id, parallel)
            )
            
            return APIResponse(
                success=results['status'] == 'success',
                data=results,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Plan execution failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    # ==================== MCP CONSCIOUSNESS INTEGRATION ====================
    
    def analyze_mcp_tool_impact(self, tool_name: str) -> APIResponse:
        """
        Analyze the impact of a tool on consciousness development.
        
        Args:
            tool_name: Name of the tool to analyze
            
        Returns:
            APIResponse with impact analysis
        """
        try:
            impact_analysis = self.mcp_consciousness_bridge.evaluate_tool_impact(tool_name)
            
            return APIResponse(
                success=True,
                data=impact_analysis,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Tool impact analysis failed: {str(e)}",
                system_status=self.status
            )
    
    def get_mcp_performance_metrics(self) -> APIResponse:
        """
        Get performance metrics for MCP tool usage.
        
        Returns:
            APIResponse with performance metrics
        """
        try:
            metrics = self.mcp_tool_orchestrator.analyze_tool_performance()
            
            return APIResponse(
                success=True,
                data=metrics,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Failed to get performance metrics: {str(e)}",
                system_status=self.status
            )
    
    # ==================== MCP RESOURCE OPERATIONS ====================
    
    def read_mcp_resource(
        self,
        server_id: str,
        resource_uri: str
    ) -> APIResponse:
        """
        Read a resource from an MCP server.
        
        Args:
            server_id: Server identifier
            resource_uri: URI of the resource to read
            
        Returns:
            APIResponse with resource content
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                self.mcp_server_manager.read_resource(server_id, resource_uri)
            )
            
            return APIResponse(
                success=result.get('success', False),
                data=result.get('content'),
                error=result.get('error'),
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Resource read failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()
    
    def list_mcp_resources(self) -> APIResponse:
        """
        List all available resources from connected MCP servers.
        
        Returns:
            APIResponse with resource list
        """
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            resources = loop.run_until_complete(
                self.mcp_server_manager.list_all_resources()
            )
            
            return APIResponse(
                success=True,
                data={
                    'resources': resources,
                    'total_resources': len(resources)
                },
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Resource listing failed: {str(e)}",
                system_status=self.status
            )
        finally:
            loop.close()


# Example of how to integrate these methods into UnifiedUORAPI:
"""
# In unified_api.py, add to the UnifiedUORAPI class:

1. Add MCP imports at the top:
from modules.mcp_interface import MCPServerManager, MCPConsciousnessBridge, MCPToolOrchestrator

2. Add MCP_ENABLED to APIMode enum:
MCP_ENABLED = "mcp_enabled"

3. Add mcp_state to SystemState dataclass:
mcp_state: Dict[str, Any] = field(default_factory=dict)

4. In __init__, add MCP initialization:
if self.mode == APIMode.MCP_ENABLED:
    self._initialize_mcp_components()

5. Add all the methods from MCPExtension class above to UnifiedUORAPI

6. Update _initialize_mode to handle MCP_ENABLED:
elif self.mode == APIMode.MCP_ENABLED:
    self.consciousness_core.awaken()
    self._initialize_mcp_components()
    self.status = SystemStatus.ACTIVE
"""
