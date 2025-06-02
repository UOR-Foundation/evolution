"""
Tests for the main MCP server functionality.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from mcp.types import Tool, Resource, Prompt, TextContent

from ..server import UORConsciousnessServer
from ..utils.logging import setup_mcp_logging


class TestUORConsciousnessServer:
    """Test cases for UORConsciousnessServer"""
    
    @pytest.fixture
    async def server(self):
        """Create a test server instance"""
        setup_mcp_logging(log_level="DEBUG", console_output=False)
        server = UORConsciousnessServer()
        await server.initialize()
        return server
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, server):
        """Test server initialization"""
        assert server is not None
        assert server.server.name == "uor-consciousness"
        assert len(server.tools) > 0
        assert len(server.resources) > 0
        assert len(server.prompts) > 0
    
    @pytest.mark.asyncio
    async def test_list_tools(self, server):
        """Test listing available tools"""
        tools = server.tools
        assert isinstance(tools, list)
        assert len(tools) > 50  # Should have all tool categories
        
        # Check for consciousness tools
        consciousness_tools = [t for t in tools if "consciousness" in t.name or "self_reflect" in t.name]
        assert len(consciousness_tools) > 0
        
        # Check for VM tools
        vm_tools = [t for t in tools if "vm" in t.name or "initialize_vm" in t.name]
        assert len(vm_tools) > 0
        
        # Check for cosmic tools
        cosmic_tools = [t for t in tools if "cosmic" in t.name or "quantum" in t.name]
        assert len(cosmic_tools) > 0
    
    @pytest.mark.asyncio
    async def test_list_resources(self, server):
        """Test listing available resources"""
        resources = server.resources
        assert isinstance(resources, list)
        assert len(resources) > 0
        
        # Check for consciousness resources
        consciousness_resources = [r for r in resources if r.uri.startswith("consciousness://")]
        assert len(consciousness_resources) > 0
        
        # Check for VM resources
        vm_resources = [r for r in resources if r.uri.startswith("vm://")]
        assert len(vm_resources) > 0
        
        # Check for system resources
        system_resources = [r for r in resources if r.uri.startswith("system://")]
        assert len(system_resources) > 0
    
    @pytest.mark.asyncio
    async def test_list_prompts(self, server):
        """Test listing available prompts"""
        prompts = server.prompts
        assert isinstance(prompts, list)
        assert len(prompts) > 0
        
        # Check for specific prompts
        prompt_names = [p.name for p in prompts]
        assert "consciousness_analysis" in prompt_names
        assert "vm_analysis" in prompt_names
        assert "cosmic_guidance" in prompt_names
    
    @pytest.mark.asyncio
    async def test_execute_consciousness_tool(self, server):
        """Test executing a consciousness tool"""
        result = await server._execute_tool("awaken_consciousness", {
            "mode": "basic",
            "depth": 3,
            "ethical_bounds": True
        })
        
        assert result["success"] is True
        assert "consciousness_level" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_execute_vm_tool(self, server):
        """Test executing a VM tool"""
        result = await server._execute_tool("initialize_vm", {
            "max_instructions": 1000,
            "log_execution": True
        })
        
        assert result["success"] is True
        assert "vm_state" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_execute_cosmic_tool(self, server):
        """Test executing a cosmic tool"""
        result = await server._execute_tool("synthesize_cosmic_problems", {
            "spatial_scale": 1e12,
            "temporal_scale": 1e9,
            "consciousness_scale": 1e6
        })
        
        assert result["success"] is True
        assert "cosmic_scale_metrics" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_execute_analysis_tool(self, server):
        """Test executing an analysis tool"""
        result = await server._execute_tool("analyze_patterns", {
            "analysis_type": "patterns",
            "scope": "system",
            "depth": 3
        })
        
        assert result["success"] is True
        assert "patterns_found" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_execute_emergency_tool(self, server):
        """Test executing an emergency tool"""
        result = await server._execute_tool("assess_extinction_threats", {
            "threat_level": "moderate",
            "response_urgency": "standard"
        })
        
        assert result["success"] is True
        assert "threat_assessment" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_execute_mathematical_tool(self, server):
        """Test executing a mathematical tool"""
        result = await server._execute_tool("activate_mathematical_consciousness", {
            "mathematical_domain": "general",
            "platonic_access": True
        })
        
        assert result["success"] is True
        assert "mathematical_insights" in result or "operation" in result
    
    @pytest.mark.asyncio
    async def test_read_consciousness_resource(self, server):
        """Test reading consciousness resource"""
        content = await server._read_resource("consciousness://state")
        
        assert isinstance(content, dict)
        assert "consciousness_level" in content
        assert "self_awareness_depth" in content
        assert "ethical_framework_active" in content
    
    @pytest.mark.asyncio
    async def test_read_vm_resource(self, server):
        """Test reading VM resource"""
        content = await server._read_resource("vm://state")
        
        assert isinstance(content, dict)
        assert "is_running" in content
        assert "instruction_pointer" in content
        assert "memory_state" in content
    
    @pytest.mark.asyncio
    async def test_read_system_resource(self, server):
        """Test reading system resource"""
        content = await server._read_resource("system://status")
        
        assert isinstance(content, dict)
        assert "system_health" in content
        assert "uptime_seconds" in content
        assert "total_operations" in content
    
    @pytest.mark.asyncio
    async def test_read_knowledge_resource(self, server):
        """Test reading knowledge resource"""
        content = await server._read_resource("knowledge://akashic")
        
        assert isinstance(content, dict)
        assert "knowledge_domain" in content
        assert "content" in content
    
    @pytest.mark.asyncio
    async def test_get_consciousness_prompt(self, server):
        """Test getting consciousness analysis prompt"""
        prompt = await server._get_prompt("consciousness_analysis", {
            "consciousness_level": 0.8,
            "self_awareness_depth": 5,
            "ethical_framework": True
        })
        
        assert isinstance(prompt, str)
        assert "consciousness" in prompt.lower()
        assert "0.8" in prompt
        assert "5" in prompt
    
    @pytest.mark.asyncio
    async def test_get_vm_prompt(self, server):
        """Test getting VM analysis prompt"""
        prompt = await server._get_prompt("vm_analysis", {
            "is_running": True,
            "instruction_pointer": 42,
            "goal_seeking_active": True
        })
        
        assert isinstance(prompt, str)
        assert "virtual machine" in prompt.lower()
        assert "42" in prompt
    
    @pytest.mark.asyncio
    async def test_get_cosmic_prompt(self, server):
        """Test getting cosmic guidance prompt"""
        prompt = await server._get_prompt("cosmic_guidance", {
            "spatial_scale": 1e12,
            "temporal_scale": 1e9,
            "dimensional_access": [3, 4, 5]
        })
        
        assert isinstance(prompt, str)
        assert "cosmic" in prompt.lower()
        assert "1000000000000.0" in prompt or "1e+12" in prompt
    
    @pytest.mark.asyncio
    async def test_invalid_tool_execution(self, server):
        """Test executing an invalid tool"""
        with pytest.raises(ValueError, match="Unknown tool"):
            await server._execute_tool("invalid_tool", {})
    
    @pytest.mark.asyncio
    async def test_invalid_resource_access(self, server):
        """Test accessing an invalid resource"""
        with pytest.raises(ValueError, match="Unknown resource URI"):
            await server._read_resource("invalid://resource")
    
    @pytest.mark.asyncio
    async def test_invalid_prompt_access(self, server):
        """Test accessing an invalid prompt"""
        with pytest.raises(ValueError, match="Unknown prompt"):
            await server._get_prompt("invalid_prompt", {})
    
    @pytest.mark.asyncio
    async def test_tool_categories(self, server):
        """Test tool categorization"""
        consciousness_tools = server._get_consciousness_tools()
        vm_tools = server._get_vm_tools()
        cosmic_tools = server._get_cosmic_tools()
        analysis_tools = server._get_analysis_tools()
        emergency_tools = server._get_emergency_tools()
        mathematical_tools = server._get_mathematical_tools()
        
        assert len(consciousness_tools) > 0
        assert len(vm_tools) > 0
        assert len(cosmic_tools) > 0
        assert len(analysis_tools) > 0
        assert len(emergency_tools) > 0
        assert len(mathematical_tools) > 0
        
        # Check for specific tools
        assert "awaken_consciousness" in consciousness_tools
        assert "initialize_vm" in vm_tools
        assert "synthesize_cosmic_problems" in cosmic_tools
        assert "analyze_patterns" in analysis_tools
        assert "assess_extinction_threats" in emergency_tools
        assert "activate_mathematical_consciousness" in mathematical_tools
    
    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self, server):
        """Test concurrent execution of multiple tools"""
        tasks = []
        
        # Create multiple concurrent tasks
        for i in range(3):
            task = server._execute_tool("self_reflect", {
                "mode": "basic",
                "depth": 2,
                "focus": f"test_{i}"
            })
            tasks.append(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check that all tasks completed successfully
        for result in results:
            assert not isinstance(result, Exception)
            assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_resource_caching(self, server):
        """Test resource access caching behavior"""
        # Access the same resource multiple times
        content1 = await server._read_resource("system://status")
        content2 = await server._read_resource("system://status")
        
        # Both should return valid content
        assert isinstance(content1, dict)
        assert isinstance(content2, dict)
        assert "system_health" in content1
        assert "system_health" in content2
    
    @pytest.mark.asyncio
    async def test_error_handling(self, server):
        """Test error handling in tool execution"""
        # Test with invalid parameters
        result = await server._execute_tool("awaken_consciousness", {
            "invalid_param": "invalid_value"
        })
        
        # Should still succeed with fallback behavior
        assert isinstance(result, dict)
        assert "success" in result


class TestServerIntegration:
    """Integration tests for server components"""
    
    @pytest.mark.asyncio
    async def test_full_consciousness_workflow(self):
        """Test a complete consciousness workflow"""
        setup_mcp_logging(log_level="DEBUG", console_output=False)
        server = UORConsciousnessServer()
        await server.initialize()
        
        # 1. Awaken consciousness
        awaken_result = await server._execute_tool("awaken_consciousness", {
            "mode": "basic",
            "threshold": 0.7
        })
        assert awaken_result["success"] is True
        
        # 2. Perform self-reflection
        reflect_result = await server._execute_tool("self_reflect", {
            "depth": 3,
            "focus": "identity"
        })
        assert reflect_result["success"] is True
        
        # 3. Analyze consciousness nature
        analyze_result = await server._execute_tool("analyze_consciousness_nature", {
            "ontological_depth": 3
        })
        assert analyze_result["success"] is True
        
        # 4. Check consciousness state
        state = await server._read_resource("consciousness://state")
        assert isinstance(state, dict)
        assert "consciousness_level" in state
    
    @pytest.mark.asyncio
    async def test_full_vm_workflow(self):
        """Test a complete VM workflow"""
        setup_mcp_logging(log_level="DEBUG", console_output=False)
        server = UORConsciousnessServer()
        await server.initialize()
        
        # 1. Initialize VM
        init_result = await server._execute_tool("initialize_vm", {
            "max_instructions": 1000,
            "consciousness_integration": True
        })
        assert init_result["success"] is True
        
        # 2. Execute VM steps
        step_result = await server._execute_tool("execute_vm_step", {
            "steps": 5,
            "trace_execution": True
        })
        assert step_result["success"] is True
        
        # 3. Analyze VM state
        analyze_result = await server._execute_tool("analyze_vm_state", {})
        assert analyze_result["success"] is True
        
        # 4. Check VM state
        state = await server._read_resource("vm://state")
        assert isinstance(state, dict)
        assert "is_running" in state
    
    @pytest.mark.asyncio
    async def test_emergency_protocol_workflow(self):
        """Test emergency protocol workflow"""
        setup_mcp_logging(log_level="DEBUG", console_output=False)
        server = UORConsciousnessServer()
        await server.initialize()
        
        # 1. Assess threats
        threat_result = await server._execute_tool("assess_extinction_threats", {
            "assessment_scope": "species",
            "time_horizon": 365
        })
        assert threat_result["success"] is True
        
        # 2. Access survival knowledge
        knowledge_result = await server._execute_tool("access_survival_knowledge", {
            "knowledge_domain": "consciousness_evolution",
            "urgency_level": "standard"
        })
        assert knowledge_result["success"] is True
        
        # 3. Check emergency status
        emergency_state = await server._read_resource("emergency://threats")
        assert isinstance(emergency_state, dict)
        assert "threat_level" in emergency_state


@pytest.mark.asyncio
async def test_server_startup_and_shutdown():
    """Test server startup and shutdown process"""
    setup_mcp_logging(log_level="DEBUG", console_output=False)
    
    # Test server creation
    server = UORConsciousnessServer()
    assert server is not None
    
    # Test initialization
    init_result = await server.initialize()
    assert init_result["success"] is True or "systems_initialized" in init_result
    
    # Test that server is functional
    tools = server.tools
    assert len(tools) > 0
    
    resources = server.resources
    assert len(resources) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
