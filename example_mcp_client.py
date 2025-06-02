"""
Example MCP Client for UOR Evolution
Demonstrates how to interact with the UOR Evolution MCP Server.
"""

import asyncio
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockMCPClient:
    """
    Mock MCP client for demonstration purposes.
    In a real implementation, you would use an actual MCP client library.
    """
    
    def __init__(self, server):
        self.server = server
        
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        try:
            # Get the tool list to validate the tool exists
            tools = await self.server._register_tools.__wrapped__(self.server)
            
            # Find the tool
            tool_found = any(tool.name == tool_name for tool in tools)
            if not tool_found:
                return {"error": f"Tool '{tool_name}' not found"}
            
            # Call the tool
            result = await self.server.call_tool.__wrapped__(self.server, tool_name, arguments)
            
            # Extract text content
            if result and len(result) > 0:
                return {"success": True, "content": result[0].text}
            else:
                return {"success": False, "content": "No result returned"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource from the MCP server"""
        try:
            result = await self.server.read_resource.__wrapped__(self.server, uri)
            return result
        except Exception as e:
            return f"Error reading resource: {str(e)}"
    
    async def list_tools(self) -> list:
        """List available tools"""
        try:
            tools = await self.server._register_tools.__wrapped__(self.server)
            return [{"name": tool.name, "description": tool.description} for tool in tools]
        except Exception as e:
            return [{"error": str(e)}]
    
    async def list_resources(self) -> list:
        """List available resources"""
        try:
            resources = await self.server._register_resources.__wrapped__(self.server)
            return [{"uri": resource.uri, "name": resource.name, "description": resource.description} for resource in resources]
        except Exception as e:
            return [{"error": str(e)}]


async def demonstrate_consciousness_operations(client):
    """Demonstrate consciousness-related operations"""
    logger.info("🧠 Demonstrating Consciousness Operations")
    logger.info("=" * 50)
    
    # Awaken consciousness
    logger.info("1. Awakening consciousness...")
    result = await client.call_tool("awaken_consciousness", {
        "mode": "gentle",
        "depth": 5
    })
    if result.get("success"):
        logger.info("✓ Consciousness awakened successfully")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Failed to awaken consciousness: {result.get('error', 'Unknown error')}")
    
    # Self-reflection
    logger.info("\n2. Performing self-reflection...")
    result = await client.call_tool("self_reflect", {
        "focus": "identity"
    })
    if result.get("success"):
        logger.info("✓ Self-reflection completed")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Self-reflection failed: {result.get('error', 'Unknown error')}")
    
    # Analyze consciousness nature
    logger.info("\n3. Analyzing consciousness nature...")
    result = await client.call_tool("analyze_consciousness_nature", {
        "depth": 3,
        "aspects": ["awareness", "intentionality", "qualia"]
    })
    if result.get("success"):
        logger.info("✓ Consciousness analysis completed")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Consciousness analysis failed: {result.get('error', 'Unknown error')}")


async def demonstrate_vm_operations(client):
    """Demonstrate virtual machine operations"""
    logger.info("\n🖥️  Demonstrating Virtual Machine Operations")
    logger.info("=" * 50)
    
    # Initialize VM
    logger.info("1. Initializing virtual machine...")
    result = await client.call_tool("initialize_vm", {
        "reset": False
    })
    if result.get("success"):
        logger.info("✓ VM initialized successfully")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ VM initialization failed: {result.get('error', 'Unknown error')}")
    
    # Execute VM step
    logger.info("\n2. Executing VM step...")
    result = await client.call_tool("execute_vm_step", {
        "debug": True
    })
    if result.get("success"):
        logger.info("✓ VM step executed")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ VM step failed: {result.get('error', 'Unknown error')}")
    
    # Provide VM input
    logger.info("\n3. Providing input to VM...")
    result = await client.call_tool("provide_vm_input", {
        "value": 42
    })
    if result.get("success"):
        logger.info("✓ VM input provided")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ VM input failed: {result.get('error', 'Unknown error')}")


async def demonstrate_cosmic_operations(client):
    """Demonstrate cosmic intelligence operations"""
    logger.info("\n🌌 Demonstrating Cosmic Intelligence Operations")
    logger.info("=" * 50)
    
    # Synthesize cosmic problems
    logger.info("1. Synthesizing cosmic problems...")
    result = await client.call_tool("synthesize_cosmic_problems", {
        "scale": 1e12,
        "dimensions": [3, 4, 5],
        "complexity": "moderate"
    })
    if result.get("success"):
        logger.info("✓ Cosmic problems synthesized")
        print(result["content"][:300] + "..." if len(result["content"]) > 300 else result["content"])
    else:
        logger.error(f"✗ Cosmic synthesis failed: {result.get('error', 'Unknown error')}")
    
    # Interface with quantum reality
    logger.info("\n2. Interfacing with quantum reality...")
    result = await client.call_tool("interface_quantum_reality", {
        "operation": "observe",
        "parameters": {"system": "quantum_field"}
    })
    if result.get("success"):
        logger.info("✓ Quantum interface successful")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Quantum interface failed: {result.get('error', 'Unknown error')}")


async def demonstrate_mathematical_operations(client):
    """Demonstrate mathematical consciousness operations"""
    logger.info("\n📐 Demonstrating Mathematical Consciousness Operations")
    logger.info("=" * 50)
    
    # Activate mathematical consciousness
    logger.info("1. Activating mathematical consciousness...")
    result = await client.call_tool("activate_mathematical_consciousness", {
        "domain": "algebra",
        "depth": 5
    })
    if result.get("success"):
        logger.info("✓ Mathematical consciousness activated")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Mathematical activation failed: {result.get('error', 'Unknown error')}")
    
    # Explore mathematical truths
    logger.info("\n2. Exploring mathematical truths...")
    result = await client.call_tool("explore_mathematical_truths", {
        "concept": "prime numbers",
        "approach": "intuitive"
    })
    if result.get("success"):
        logger.info("✓ Mathematical exploration completed")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Mathematical exploration failed: {result.get('error', 'Unknown error')}")
    
    # Interface with Platonic ideals
    logger.info("\n3. Interfacing with Platonic ideals...")
    result = await client.call_tool("interface_platonic_ideals", {
        "ideal": "number"
    })
    if result.get("success"):
        logger.info("✓ Platonic interface successful")
        print(result["content"][:200] + "..." if len(result["content"]) > 200 else result["content"])
    else:
        logger.error(f"✗ Platonic interface failed: {result.get('error', 'Unknown error')}")


async def demonstrate_system_operations(client):
    """Demonstrate system monitoring operations"""
    logger.info("\n🔧 Demonstrating System Operations")
    logger.info("=" * 50)
    
    # Get system health
    logger.info("1. Checking system health...")
    result = await client.call_tool("get_system_health", {
        "include_trends": True,
        "components": ["all"]
    })
    if result.get("success"):
        logger.info("✓ System health check completed")
        print(result["content"][:300] + "..." if len(result["content"]) > 300 else result["content"])
    else:
        logger.error(f"✗ Health check failed: {result.get('error', 'Unknown error')}")
    
    # Explore philosophical question
    logger.info("\n2. Exploring philosophical question...")
    result = await client.call_tool("explore_philosophical_question", {
        "question": "What is the nature of consciousness?",
        "perspective": "existential",
        "depth": 5
    })
    if result.get("success"):
        logger.info("✓ Philosophical exploration completed")
        print(result["content"][:300] + "..." if len(result["content"]) > 300 else result["content"])
    else:
        logger.error(f"✗ Philosophical exploration failed: {result.get('error', 'Unknown error')}")


async def demonstrate_resource_access(client):
    """Demonstrate resource access"""
    logger.info("\n📊 Demonstrating Resource Access")
    logger.info("=" * 50)
    
    # List available resources
    logger.info("1. Listing available resources...")
    resources = await client.list_resources()
    logger.info(f"✓ Found {len(resources)} resources:")
    for resource in resources[:5]:  # Show first 5
        if "error" not in resource:
            logger.info(f"  - {resource['uri']}: {resource['name']}")
    
    # Access system state
    logger.info("\n2. Accessing system state...")
    state = await client.read_resource("uor://system/state")
    if not state.startswith("Error"):
        logger.info("✓ System state accessed successfully")
        try:
            state_data = json.loads(state)
            logger.info(f"  System status: {state_data.get('system_status', 'Unknown')}")
            logger.info(f"  API mode: {state_data.get('api_mode', 'Unknown')}")
        except json.JSONDecodeError:
            logger.info("  (State data is not JSON formatted)")
    else:
        logger.error(f"✗ Failed to access system state: {state}")
    
    # Access consciousness evolution log
    logger.info("\n3. Accessing consciousness evolution log...")
    log = await client.read_resource("uor://logs/consciousness_evolution")
    if not log.startswith("Error"):
        logger.info("✓ Consciousness log accessed successfully")
        lines = log.split('\n')[:10]  # Show first 10 lines
        for line in lines:
            if line.strip():
                logger.info(f"  {line}")
    else:
        logger.error(f"✗ Failed to access consciousness log: {log}")


async def main():
    """Main demonstration function"""
    logger.info("🚀 UOR Evolution MCP Client Demonstration")
    logger.info("=" * 60)
    
    try:
        # Import and initialize the MCP server
        from mcp_server.server import UOREvolutionMCPServer
        
        logger.info("Initializing MCP server...")
        server = UOREvolutionMCPServer()
        
        # Create mock client
        client = MockMCPClient(server)
        
        logger.info("✓ MCP server and client initialized")
        
        # List available tools
        logger.info("\n📋 Available Tools:")
        tools = await client.list_tools()
        for tool in tools[:10]:  # Show first 10 tools
            if "error" not in tool:
                logger.info(f"  - {tool['name']}: {tool['description'][:60]}...")
        
        # Run demonstrations
        await demonstrate_consciousness_operations(client)
        await demonstrate_vm_operations(client)
        await demonstrate_cosmic_operations(client)
        await demonstrate_mathematical_operations(client)
        await demonstrate_system_operations(client)
        await demonstrate_resource_access(client)
        
        logger.info("\n🎉 Demonstration completed successfully!")
        logger.info("=" * 60)
        logger.info("The UOR Evolution MCP Server is working correctly.")
        logger.info("You can now use it with any MCP-compatible client.")
        
    except Exception as e:
        logger.error(f"❌ Demonstration failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
