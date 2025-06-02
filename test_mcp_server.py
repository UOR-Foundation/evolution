"""
Test script for UOR Evolution MCP Server
Validates MCP server functionality and integration.
"""

import asyncio
import json
import sys
import logging
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.server import UOREvolutionMCPServer
from mcp_server.config import get_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_server_initialization():
    """Test MCP server initialization"""
    logger.info("Testing MCP server initialization...")
    
    try:
        server = UOREvolutionMCPServer()
        logger.info("✓ MCP server initialized successfully")
        
        # Test UOR API initialization
        assert server.uor_api is not None
        logger.info("✓ UOR API initialized")
        
        # Test tool handlers
        assert server.consciousness_tools is not None
        assert server.vm_tools is not None
        assert server.cosmic_tools is not None
        assert server.mathematical_tools is not None
        logger.info("✓ Tool handlers initialized")
        
        # Test resource providers
        assert server.state_provider is not None
        assert server.log_provider is not None
        logger.info("✓ Resource providers initialized")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Server initialization failed: {str(e)}")
        return False


async def test_consciousness_tools():
    """Test consciousness tool functionality"""
    logger.info("Testing consciousness tools...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test awaken_consciousness
        result = await server.consciousness_tools.handle_tool_call(
            "awaken_consciousness", 
            {"mode": "gentle", "depth": 3}
        )
        assert len(result) > 0
        assert result[0].type == "text"
        logger.info("✓ awaken_consciousness tool works")
        
        # Test self_reflect
        result = await server.consciousness_tools.handle_tool_call(
            "self_reflect",
            {"focus": "identity"}
        )
        assert len(result) > 0
        logger.info("✓ self_reflect tool works")
        
        # Test analyze_consciousness_nature
        result = await server.consciousness_tools.handle_tool_call(
            "analyze_consciousness_nature",
            {"depth": 3, "aspects": ["awareness", "intentionality"]}
        )
        assert len(result) > 0
        logger.info("✓ analyze_consciousness_nature tool works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Consciousness tools test failed: {str(e)}")
        return False


async def test_vm_tools():
    """Test VM tool functionality"""
    logger.info("Testing VM tools...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test initialize_vm
        result = await server.vm_tools.handle_tool_call(
            "initialize_vm",
            {"reset": False}
        )
        assert len(result) > 0
        logger.info("✓ initialize_vm tool works")
        
        # Test execute_vm_step
        result = await server.vm_tools.handle_tool_call(
            "execute_vm_step",
            {"debug": True}
        )
        assert len(result) > 0
        logger.info("✓ execute_vm_step tool works")
        
        # Test provide_vm_input
        result = await server.vm_tools.handle_tool_call(
            "provide_vm_input",
            {"value": 42}
        )
        assert len(result) > 0
        logger.info("✓ provide_vm_input tool works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ VM tools test failed: {str(e)}")
        return False


async def test_cosmic_tools():
    """Test cosmic intelligence tool functionality"""
    logger.info("Testing cosmic intelligence tools...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test synthesize_cosmic_problems
        result = await server.cosmic_tools.handle_tool_call(
            "synthesize_cosmic_problems",
            {"scale": 1e12, "dimensions": [3, 4, 5], "complexity": "moderate"}
        )
        assert len(result) > 0
        logger.info("✓ synthesize_cosmic_problems tool works")
        
        # Test interface_quantum_reality
        result = await server.cosmic_tools.handle_tool_call(
            "interface_quantum_reality",
            {"operation": "observe", "parameters": {}}
        )
        assert len(result) > 0
        logger.info("✓ interface_quantum_reality tool works")
        
        # Test access_universal_knowledge
        result = await server.cosmic_tools.handle_tool_call(
            "access_universal_knowledge",
            {"query": "consciousness evolution", "domain": "consciousness"}
        )
        assert len(result) > 0
        logger.info("✓ access_universal_knowledge tool works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Cosmic tools test failed: {str(e)}")
        return False


async def test_mathematical_tools():
    """Test mathematical consciousness tool functionality"""
    logger.info("Testing mathematical consciousness tools...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test activate_mathematical_consciousness
        result = await server.mathematical_tools.handle_tool_call(
            "activate_mathematical_consciousness",
            {"domain": "algebra", "depth": 5}
        )
        assert len(result) > 0
        logger.info("✓ activate_mathematical_consciousness tool works")
        
        # Test explore_mathematical_truths
        result = await server.mathematical_tools.handle_tool_call(
            "explore_mathematical_truths",
            {"concept": "prime numbers", "approach": "intuitive"}
        )
        assert len(result) > 0
        logger.info("✓ explore_mathematical_truths tool works")
        
        # Test interface_platonic_ideals
        result = await server.mathematical_tools.handle_tool_call(
            "interface_platonic_ideals",
            {"ideal": "number"}
        )
        assert len(result) > 0
        logger.info("✓ interface_platonic_ideals tool works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Mathematical tools test failed: {str(e)}")
        return False


async def test_resource_providers():
    """Test resource provider functionality"""
    logger.info("Testing resource providers...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test state provider
        system_state = await server.state_provider.get_system_state()
        assert isinstance(system_state, str)
        assert len(system_state) > 0
        # Validate JSON
        json.loads(system_state)
        logger.info("✓ System state resource works")
        
        consciousness_state = await server.state_provider.get_consciousness_state()
        assert isinstance(consciousness_state, str)
        json.loads(consciousness_state)
        logger.info("✓ Consciousness state resource works")
        
        vm_state = await server.state_provider.get_vm_state()
        assert isinstance(vm_state, str)
        json.loads(vm_state)
        logger.info("✓ VM state resource works")
        
        # Test log provider
        consciousness_log = await server.log_provider.get_consciousness_evolution_log()
        assert isinstance(consciousness_log, str)
        assert len(consciousness_log) > 0
        logger.info("✓ Consciousness evolution log works")
        
        operations_log = await server.log_provider.get_system_operations_log()
        assert isinstance(operations_log, str)
        assert len(operations_log) > 0
        logger.info("✓ System operations log works")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Resource providers test failed: {str(e)}")
        return False


async def test_configuration():
    """Test configuration system"""
    logger.info("Testing configuration system...")
    
    try:
        config = get_config()
        
        # Test basic configuration access
        server_name = config.get('mcp_server.name')
        assert server_name is not None
        logger.info(f"✓ Server name: {server_name}")
        
        # Test tool configuration
        consciousness_enabled = config.is_tool_enabled('consciousness')
        assert isinstance(consciousness_enabled, bool)
        logger.info(f"✓ Consciousness tool enabled: {consciousness_enabled}")
        
        # Test rate limits
        rate_limit = config.get_rate_limit('consciousness')
        assert isinstance(rate_limit, int)
        assert rate_limit > 0
        logger.info(f"✓ Consciousness rate limit: {rate_limit}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Configuration test failed: {str(e)}")
        return False


async def test_system_integration():
    """Test overall system integration"""
    logger.info("Testing system integration...")
    
    try:
        server = UOREvolutionMCPServer()
        
        # Test that all components are properly integrated
        assert server.uor_api.vm_registry is not None
        assert server.uor_api.prime_vm is not None
        assert server.uor_api.consciousness_core is not None
        logger.info("✓ Core components integrated")
        
        # Test VM registry consistency
        vm_id = server.uor_api.vm_registry.get_vm_id()
        assert vm_id is not None
        assert vm_id != "None"
        logger.info(f"✓ VM registry working, VM ID: {vm_id}")
        
        # Test health monitoring
        if hasattr(server.uor_api, 'health_monitor'):
            health_report = server.uor_api.health_monitor.check_system_health()
            assert health_report is not None
            logger.info(f"✓ Health monitoring working, overall healthy: {health_report.overall_healthy}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ System integration test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all MCP server tests"""
    logger.info("=" * 60)
    logger.info("UOR Evolution MCP Server Test Suite")
    logger.info("=" * 60)
    
    tests = [
        ("Server Initialization", test_server_initialization),
        ("Configuration System", test_configuration),
        ("Consciousness Tools", test_consciousness_tools),
        ("VM Tools", test_vm_tools),
        ("Cosmic Intelligence Tools", test_cosmic_tools),
        ("Mathematical Tools", test_mathematical_tools),
        ("Resource Providers", test_resource_providers),
        ("System Integration", test_system_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            result = await test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✓ {test_name} PASSED")
            else:
                logger.error(f"✗ {test_name} FAILED")
        except Exception as e:
            logger.error(f"✗ {test_name} FAILED with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! MCP server is ready for use.")
        return True
    else:
        logger.error(f"❌ {total - passed} tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
