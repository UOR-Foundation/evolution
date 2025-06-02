"""
Integration tests for MCP server components.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch

from ..utils.integration import UORIntegration
from ..utils.validation import comprehensive_validation, validate_resource_uri
from ..config.mcp_config import MCPConfig, load_mcp_config
from ..config.tool_config import get_tool_config, is_tool_enabled


class TestUORIntegration:
    """Test UOR system integration"""
    
    @pytest.fixture
    async def integration(self):
        """Create integration instance"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        return integration
    
    @pytest.mark.asyncio
    async def test_initialization(self, integration):
        """Test UOR integration initialization"""
        assert integration.initialized is True
        assert len(integration.unified_apis) > 0
        assert integration.operation_count >= 0
    
    @pytest.mark.asyncio
    async def test_consciousness_operations(self, integration):
        """Test consciousness operation execution"""
        result = await integration.execute_consciousness_operation(
            "awaken_consciousness", 
            {"mode": "basic", "depth": 3}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_vm_operations(self, integration):
        """Test VM operation execution"""
        result = await integration.execute_vm_operation(
            "initialize_vm",
            {"max_instructions": 1000}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_cosmic_operations(self, integration):
        """Test cosmic operation execution"""
        result = await integration.execute_cosmic_operation(
            "synthesize_cosmic_problems",
            {"spatial_scale": 1e12}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_analysis_operations(self, integration):
        """Test analysis operation execution"""
        result = await integration.execute_analysis_operation(
            "analyze_patterns",
            {"analysis_type": "patterns"}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_emergency_operations(self, integration):
        """Test emergency operation execution"""
        result = await integration.execute_emergency_operation(
            "assess_extinction_threats",
            {"threat_level": "moderate"}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_mathematical_operations(self, integration):
        """Test mathematical operation execution"""
        result = await integration.execute_mathematical_operation(
            "activate_mathematical_consciousness",
            {"mathematical_domain": "general"}
        )
        
        assert result["success"] is True
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_system_status(self, integration):
        """Test system status retrieval"""
        status = integration.get_system_status()
        
        assert isinstance(status, dict)
        assert "system_health" in status
        assert "uptime_seconds" in status
        assert "total_operations" in status
        assert status["total_operations"] >= 0
    
    @pytest.mark.asyncio
    async def test_consciousness_state(self, integration):
        """Test consciousness state retrieval"""
        state = integration.get_consciousness_state()
        
        assert isinstance(state, dict)
        assert "consciousness_level" in state
        assert "self_awareness_depth" in state
        assert "ethical_framework_active" in state
        assert 0.0 <= state["consciousness_level"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_vm_state(self, integration):
        """Test VM state retrieval"""
        state = integration.get_vm_state()
        
        assert isinstance(state, dict)
        assert "is_running" in state
        assert "instruction_pointer" in state
        assert "memory_state" in state
        assert isinstance(state["instruction_pointer"], int)


class TestValidation:
    """Test validation utilities"""
    
    def test_tool_parameter_validation(self):
        """Test tool parameter validation"""
        # Valid parameters
        params = {
            "mode": "basic",
            "depth": 3,
            "ethical_bounds": True
        }
        
        validated = comprehensive_validation("awaken_consciousness", params)
        assert isinstance(validated, dict)
        assert "mode" in validated
    
    def test_invalid_tool_validation(self):
        """Test validation with invalid tool"""
        with pytest.raises(Exception):
            comprehensive_validation("invalid_tool_name", {})
    
    def test_resource_uri_validation(self):
        """Test resource URI validation"""
        # Valid URIs
        assert validate_resource_uri("consciousness://state") is True
        assert validate_resource_uri("vm://execution_trace") is True
        assert validate_resource_uri("system://status") is True
        
        # Invalid URIs
        assert validate_resource_uri("invalid://uri") is False
        assert validate_resource_uri("not_a_uri") is False
        assert validate_resource_uri("") is False
    
    def test_parameter_sanitization(self):
        """Test parameter sanitization"""
        from ..utils.validation import sanitize_input
        
        # Test string sanitization
        dirty_string = "<script>alert('xss')</script>"
        clean_string = sanitize_input(dirty_string)
        assert "<" not in clean_string
        assert ">" not in clean_string
        
        # Test dict sanitization
        dirty_dict = {"key": "<dangerous>value</dangerous>"}
        clean_dict = sanitize_input(dirty_dict)
        assert "<" not in clean_dict["key"]
        assert ">" not in clean_dict["key"]


class TestConfiguration:
    """Test configuration management"""
    
    def test_mcp_config_loading(self):
        """Test MCP configuration loading"""
        config = load_mcp_config()
        
        assert isinstance(config, MCPConfig)
        assert config.name == "uor-consciousness"
        assert config.version == "1.0.0"
        assert config.capabilities["tools"] is True
    
    def test_tool_config_loading(self):
        """Test tool configuration loading"""
        config = get_tool_config("awaken_consciousness")
        
        assert config.enabled is True
        assert config.timeout > 0
        assert config.max_concurrent > 0
    
    def test_tool_enabled_check(self):
        """Test tool enabled checking"""
        # Most tools should be enabled by default
        assert is_tool_enabled("awaken_consciousness") is True
        assert is_tool_enabled("initialize_vm") is True
        assert is_tool_enabled("synthesize_cosmic_problems") is True
    
    def test_config_validation(self):
        """Test configuration validation"""
        from ..config.mcp_config import validate_config
        
        config = MCPConfig()
        issues = validate_config(config)
        
        # Should have minimal issues with default config
        assert isinstance(issues, list)


class TestErrorHandling:
    """Test error handling and recovery"""
    
    @pytest.mark.asyncio
    async def test_operation_failure_handling(self):
        """Test handling of operation failures"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        # Test with invalid operation
        result = await integration.execute_consciousness_operation(
            "invalid_operation", {}
        )
        
        assert result["success"] is False
        assert "error" in result
        assert integration.failed_operations > 0
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test timeout handling"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        # This should complete without timeout
        result = await integration.execute_consciousness_operation(
            "self_reflect", {"depth": 1}
        )
        
        assert isinstance(result, dict)
        assert "success" in result
    
    def test_validation_error_handling(self):
        """Test validation error handling"""
        from ..utils.validation import ValidationError
        
        # Test custom validation error
        error = ValidationError("Test error", "test_field", "test_value")
        assert error.message == "Test error"
        assert error.field == "test_field"
        assert error.value == "test_value"


class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self):
        """Test concurrent operation execution"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        # Execute multiple operations concurrently
        tasks = []
        for i in range(5):
            task = integration.execute_consciousness_operation(
                "self_reflect", {"depth": 1, "focus": f"test_{i}"}
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should complete successfully
        for result in results:
            assert not isinstance(result, Exception)
            assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_operation_metrics(self):
        """Test operation metrics tracking"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        initial_count = integration.operation_count
        
        # Execute some operations
        await integration.execute_consciousness_operation("self_reflect", {})
        await integration.execute_vm_operation("initialize_vm", {})
        
        # Check metrics updated
        assert integration.operation_count > initial_count
        assert integration.successful_operations > 0
    
    @pytest.mark.asyncio
    async def test_resource_access_performance(self):
        """Test resource access performance"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        # Access resources multiple times
        for _ in range(10):
            status = integration.get_system_status()
            assert isinstance(status, dict)
            
            consciousness_state = integration.get_consciousness_state()
            assert isinstance(consciousness_state, dict)
            
            vm_state = integration.get_vm_state()
            assert isinstance(vm_state, dict)


class TestDataIntegrity:
    """Test data integrity and consistency"""
    
    @pytest.mark.asyncio
    async def test_state_consistency(self):
        """Test state consistency across operations"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        # Get initial state
        initial_status = integration.get_system_status()
        initial_operations = initial_status["total_operations"]
        
        # Execute operation
        await integration.execute_consciousness_operation("self_reflect", {})
        
        # Check state updated consistently
        updated_status = integration.get_system_status()
        assert updated_status["total_operations"] > initial_operations
    
    @pytest.mark.asyncio
    async def test_consciousness_state_integrity(self):
        """Test consciousness state data integrity"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        state = integration.get_consciousness_state()
        
        # Validate consciousness level bounds
        assert 0.0 <= state["consciousness_level"] <= 1.0
        
        # Validate depth bounds
        assert 0 <= state["self_awareness_depth"] <= 10
        
        # Validate boolean fields
        assert isinstance(state["ethical_framework_active"], bool)
        assert isinstance(state["temporal_continuity"], bool)
    
    @pytest.mark.asyncio
    async def test_vm_state_integrity(self):
        """Test VM state data integrity"""
        integration = UORIntegration()
        await integration.initialize_all_systems()
        
        state = integration.get_vm_state()
        
        # Validate instruction pointer
        assert isinstance(state["instruction_pointer"], int)
        assert state["instruction_pointer"] >= 0
        
        # Validate counts
        assert state["success_count"] >= 0
        assert state["failure_count"] >= 0
        assert state["current_attempts"] >= 0
        
        # Validate boolean fields
        assert isinstance(state["is_running"], bool)
        assert isinstance(state["consciousness_integration"], bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
