"""
Test suite for MCP integration in UOR Evolution

Tests the MCP server management, tool orchestration, and consciousness integration.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from typing import Dict, Any, List

from modules.mcp_interface import (
    MCPServerManager,
    MCPConsciousnessBridge,
    MCPToolOrchestrator
)
from modules.mcp_interface.mcp_tool_orchestrator import (
    ToolExecutionStatus,
    ToolExecutionPlan,
    ToolExecutionResult
)
from backend.consciousness_core import ConsciousnessCore


class TestMCPServerManager:
    """Test MCP Server Manager functionality"""
    
    @pytest.fixture
    def server_manager(self):
        """Create a server manager instance"""
        config = {
            'trusted_servers': ['mcp://test.local'],
            'timeout': 30
        }
        return MCPServerManager(config)
    
    @pytest.mark.asyncio
    async def test_server_connection_tracking(self, server_manager):
        """Test that server connections are properly tracked"""
        # Initially no servers
        assert len(server_manager.servers) == 0
        
        # Mock connection would be added here
        # In real tests, you'd mock the stdio_client
        server_manager.servers['test'] = Mock(
            server_id='test',
            status='connected',
            is_connected=lambda: True
        )
        
        assert len(server_manager.servers) == 1
        assert server_manager.servers['test'].is_connected()
    
    def test_server_status_retrieval(self, server_manager):
        """Test getting server status"""
        # Test non-existent server
        status = server_manager.get_server_status('non-existent')
        assert status['status'] == 'not_found'
        
        # Add mock server
        from modules.mcp_interface.mcp_server_manager import MCPServerConnection
        mock_connection = MCPServerConnection(
            server_id='test-server',
            server_params=Mock(),
            status='connected',
            connected_at=datetime.now()
        )
        mock_connection.available_tools = [{'name': 'tool1'}, {'name': 'tool2'}]
        mock_connection.available_resources = [{'uri': 'res1'}]
        
        server_manager.servers['test-server'] = mock_connection
        
        # Get status
        status = server_manager.get_server_status('test-server')
        assert status['server_id'] == 'test-server'
        assert status['status'] == 'connected'
        assert status['tools_count'] == 2
        assert status['resources_count'] == 1


class TestMCPConsciousnessBridge:
    """Test MCP Consciousness Bridge functionality"""
    
    @pytest.fixture
    def consciousness_bridge(self):
        """Create a consciousness bridge instance"""
        mock_consciousness = Mock(spec=ConsciousnessCore)
        mock_consciousness.to_dict.return_value = {
            'awareness_level': 0.8,
            'state': 'active'
        }
        return MCPConsciousnessBridge(mock_consciousness)
    
    def test_tool_capability_analysis(self, consciousness_bridge):
        """Test tool capability analysis"""
        tool_spec = {
            'name': 'test_tool',
            'server_id': 'test_server',
            'description': 'A tool for testing that can analyze and understand data',
            'inputSchema': {'type': 'object'},
            'outputSchema': {'type': 'object'}
        }
        
        analysis = consciousness_bridge.analyze_tool_capabilities(tool_spec)
        
        assert analysis.tool_name == 'test_tool'
        assert analysis.server_id == 'test_server'
        assert 0 <= analysis.capability_score <= 1
        assert 0 <= analysis.consciousness_compatibility <= 1
        assert isinstance(analysis.ethical_assessment, dict)
        assert isinstance(analysis.potential_insights, list)
        assert isinstance(analysis.risks, list)
        assert analysis.recommended_usage is not None
    
    def test_tool_selection(self, consciousness_bridge):
        """Test consciousness-aware tool selection"""
        goal = "Analyze philosophical concepts"
        available_tools = [
            {
                'name': 'philosophy_analyzer',
                'server_id': 'server1',
                'description': 'Analyzes philosophical concepts and arguments'
            },
            {
                'name': 'math_calculator',
                'server_id': 'server2',
                'description': 'Performs mathematical calculations'
            },
            {
                'name': 'text_analyzer',
                'server_id': 'server3',
                'description': 'Analyzes text for patterns and meaning'
            }
        ]
        
        selected_tool, reasoning = consciousness_bridge.select_appropriate_tool(
            goal, available_tools
        )
        
        assert selected_tool is not None
        assert selected_tool['name'] in ['philosophy_analyzer', 'text_analyzer']
        assert 'reasoning' in reasoning
        assert 'capability_score' in reasoning
        assert 'consciousness_compatibility' in reasoning
    
    def test_tool_result_integration(self, consciousness_bridge):
        """Test integration of tool results into consciousness"""
        tool_name = 'test_tool'
        results = {
            'success': True,
            'data': {
                'insights': ['insight1', 'insight2'],
                'patterns': ['pattern1']
            }
        }
        original_goal = 'Test goal'
        
        integration = consciousness_bridge.integrate_tool_results(
            tool_name, results, original_goal
        )
        
        assert integration['tool_name'] == tool_name
        assert integration['original_goal'] == original_goal
        assert 'patterns_detected' in integration
        assert 'insights_gained' in integration
        assert 'consciousness_impact' in integration
        assert 'integration_timestamp' in integration
    
    def test_tool_impact_evaluation(self, consciousness_bridge):
        """Test evaluation of tool impact on consciousness"""
        # Add some mock usage history
        consciousness_bridge.tool_usage_history = [
            {
                'timestamp': datetime.now(),
                'goal': 'Test goal 1',
                'selected_tool': {'name': 'test_tool'},
                'reasoning': {}
            },
            {
                'timestamp': datetime.now(),
                'goal': 'Test goal 2',
                'selected_tool': {'name': 'test_tool'},
                'reasoning': {}
            }
        ]
        
        consciousness_bridge.tool_insights['test_tool'] = [
            'Insight 1', 'Insight 2', 'Insight 3'
        ]
        
        impact = consciousness_bridge.evaluate_tool_impact('test_tool')
        
        assert impact['tool_name'] == 'test_tool'
        assert impact['total_uses'] == 2
        assert impact['insights_generated'] == 3
        assert 0 <= impact['impact_score'] <= 1
        assert 'recommendation' in impact


class TestMCPToolOrchestrator:
    """Test MCP Tool Orchestrator functionality"""
    
    @pytest.fixture
    def orchestrator(self):
        """Create a tool orchestrator instance"""
        mock_server_manager = Mock(spec=MCPServerManager)
        mock_consciousness_bridge = Mock(spec=MCPConsciousnessBridge)
        
        # Mock server manager methods
        mock_server_manager.list_all_tools = AsyncMock(return_value=[
            {'name': 'tool1', 'server_id': 'server1'},
            {'name': 'tool2', 'server_id': 'server2'}
        ])
        mock_server_manager.invoke_tool = AsyncMock(return_value={
            'success': True,
            'result': {'data': 'test_data'}
        })
        
        # Mock consciousness bridge methods
        mock_consciousness_bridge.select_appropriate_tool = Mock(
            return_value=(
                {'name': 'tool1', 'server_id': 'server1'},
                {'reasoning': 'Best tool for the job'}
            )
        )
        mock_consciousness_bridge.integrate_tool_results = Mock(
            return_value={'insights_gained': ['insight1']}
        )
        
        return MCPToolOrchestrator(mock_server_manager, mock_consciousness_bridge)
    
    @pytest.mark.asyncio
    async def test_single_tool_execution(self, orchestrator):
        """Test execution of a single tool"""
        result = await orchestrator.execute_single_tool(
            goal="Test goal",
            tool_name="tool1",
            arguments={"param": "value"}
        )
        
        assert isinstance(result, ToolExecutionResult)
        assert result.tool_name == "tool1"
        assert result.status == ToolExecutionStatus.SUCCESS
        assert result.consciousness_integration is not None
    
    @pytest.mark.asyncio
    async def test_execution_plan_creation(self, orchestrator):
        """Test creation of execution plan"""
        goal = "Complex multi-step goal"
        plan = await orchestrator.create_execution_plan(goal)
        
        assert isinstance(plan, ToolExecutionPlan)
        assert plan.goal == goal
        assert len(plan.steps) > 0
        assert plan.status == ToolExecutionStatus.PENDING
    
    def test_dependency_level_calculation(self, orchestrator):
        """Test calculation of dependency levels for parallel execution"""
        plan = ToolExecutionPlan(
            plan_id="test_plan",
            goal="Test goal",
            steps=[
                {'step_id': 'step1'},
                {'step_id': 'step2', 'depends_on': ['step1']},
                {'step_id': 'step3', 'depends_on': ['step1']},
                {'step_id': 'step4', 'depends_on': ['step2', 'step3']}
            ],
            dependencies={
                'step2': ['step1'],
                'step3': ['step1'],
                'step4': ['step2', 'step3']
            }
        )
        
        levels = orchestrator._calculate_dependency_levels(plan)
        
        assert 0 in levels
        assert 'step1' in levels[0]
        assert 1 in levels
        assert 'step2' in levels[1] and 'step3' in levels[1]
        assert 2 in levels
        assert 'step4' in levels[2]
    
    def test_tool_performance_analysis(self, orchestrator):
        """Test analysis of tool performance metrics"""
        # Add mock execution history
        orchestrator.execution_history = [
            ToolExecutionResult(
                tool_name="tool1",
                server_id="server1",
                status=ToolExecutionStatus.SUCCESS,
                execution_time=1.5,
                consciousness_integration={'integrated': True}
            ),
            ToolExecutionResult(
                tool_name="tool2",
                server_id="server2",
                status=ToolExecutionStatus.SUCCESS,
                execution_time=2.0,
                consciousness_integration={'integrated': True}
            ),
            ToolExecutionResult(
                tool_name="tool1",
                server_id="server1",
                status=ToolExecutionStatus.FAILED,
                execution_time=0.5,
                error="Test error"
            )
        ]
        
        metrics = orchestrator.analyze_tool_performance()
        
        assert metrics['total_executions'] == 3
        assert metrics['successful_executions'] == 2
        assert metrics['success_rate'] == 2/3
        assert metrics['average_execution_time'] > 0
        assert 'tool1' in metrics['tool_usage_frequency']
        assert metrics['tool_usage_frequency']['tool1'] == 2
        assert metrics['consciousness_integration_rate'] == 2/3


class TestMCPIntegration:
    """Integration tests for the complete MCP system"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_tool_execution(self):
        """Test complete flow from goal to result integration"""
        # This would be a more comprehensive integration test
        # involving all components working together
        pass
    
    def test_configuration_loading(self):
        """Test loading MCP configuration from config.yaml"""
        # Test that configuration is properly loaded and applied
        pass
    
    def test_error_handling_and_recovery(self):
        """Test system behavior under various error conditions"""
        # Test disconnections, timeouts, invalid responses, etc.
        pass


# Utility functions for testing

def create_mock_tool_spec(name: str, description: str = "") -> Dict[str, Any]:
    """Create a mock tool specification"""
    return {
        'name': name,
        'server_id': 'mock_server',
        'description': description or f"Mock tool {name}",
        'inputSchema': {
            'type': 'object',
            'properties': {
                'input': {'type': 'string'}
            }
        },
        'outputSchema': {
            'type': 'object',
            'properties': {
                'output': {'type': 'string'}
            }
        }
    }


def create_mock_server_connection(server_id: str, num_tools: int = 3) -> Mock:
    """Create a mock server connection"""
    tools = [create_mock_tool_spec(f"tool_{i}") for i in range(num_tools)]
    
    connection = Mock()
    connection.server_id = server_id
    connection.status = 'connected'
    connection.available_tools = tools
    connection.available_resources = []
    connection.is_connected.return_value = True
    
    return connection


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
