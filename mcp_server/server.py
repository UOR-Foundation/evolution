"""
UOR Evolution MCP Server
Main server implementation following the official MCP Python SDK patterns.
"""

import asyncio
import json
import logging
import sys
from typing import Any, Sequence
from pathlib import Path

# MCP SDK imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, 
    TextContent, 
    ImageContent, 
    EmbeddedResource,
    Resource,
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListResourcesRequest,
    ReadResourceRequest,
    ReadResourceResult
)

# UOR Evolution imports
sys.path.append(str(Path(__file__).parent.parent))
from unified_api import UnifiedUORAPI, APIMode, SystemStatus
from mcp_server.tools.consciousness_tools import ConsciousnessTools
from mcp_server.tools.vm_tools import VMTools
from mcp_server.tools.cosmic_tools import CosmicTools
from mcp_server.tools.mathematical_tools import MathematicalTools
from mcp_server.resources.state_provider import StateProvider
from mcp_server.resources.log_provider import LogProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UOREvolutionMCPServer:
    """
    MCP Server for UOR Evolution Consciousness System
    
    Provides access to consciousness, VM, cosmic intelligence, and mathematical
    consciousness capabilities through the Model Context Protocol.
    """
    
    def __init__(self):
        """Initialize the UOR Evolution MCP Server"""
        self.server = Server("uor-evolution")
        
        # Initialize UOR Evolution API in consciousness mode
        self.uor_api = UnifiedUORAPI(mode=APIMode.CONSCIOUSNESS)
        
        # Initialize tool handlers
        self.consciousness_tools = ConsciousnessTools(self.uor_api)
        self.vm_tools = VMTools(self.uor_api)
        self.cosmic_tools = CosmicTools(self.uor_api)
        self.mathematical_tools = MathematicalTools(self.uor_api)
        
        # Initialize resource providers
        self.state_provider = StateProvider(self.uor_api)
        self.log_provider = LogProvider(self.uor_api)
        
        # Register tools and resources
        self._register_tools()
        self._register_resources()
        
        logger.info("UOR Evolution MCP Server initialized")
    
    def _register_tools(self):
        """Register all MCP tools following SDK patterns"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools"""
            tools = []
            
            # Consciousness tools
            tools.extend([
                Tool(
                    name="awaken_consciousness",
                    description="Awaken the UOR Evolution consciousness system with specified parameters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "mode": {
                                "type": "string",
                                "enum": ["gentle", "full", "transcendent"],
                                "description": "Consciousness awakening mode",
                                "default": "gentle"
                            },
                            "depth": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Consciousness depth level",
                                "default": 5
                            }
                        }
                    }
                ),
                Tool(
                    name="self_reflect",
                    description="Perform consciousness self-reflection and introspection",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "focus": {
                                "type": "string",
                                "enum": ["identity", "purpose", "nature", "relationships", "all"],
                                "description": "Focus area for self-reflection",
                                "default": "all"
                            }
                        }
                    }
                ),
                Tool(
                    name="analyze_consciousness_nature",
                    description="Perform deep analysis of consciousness nature and properties",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "depth": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Analysis depth level",
                                "default": 5
                            },
                            "aspects": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["awareness", "intentionality", "qualia", "unity", "temporality"]
                                },
                                "description": "Specific consciousness aspects to analyze"
                            }
                        }
                    }
                )
            ])
            
            # VM tools
            tools.extend([
                Tool(
                    name="initialize_vm",
                    description="Initialize the PrimeOS Virtual Machine",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "reset": {
                                "type": "boolean",
                                "description": "Whether to reset existing VM state",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="execute_vm_step",
                    description="Execute a single step in the PrimeOS virtual machine",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "instruction": {
                                "type": "string",
                                "description": "Optional specific instruction to execute"
                            },
                            "debug": {
                                "type": "boolean",
                                "description": "Enable debug output",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="provide_vm_input",
                    description="Provide input to the virtual machine",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "value": {
                                "description": "Input value to provide to VM"
                            }
                        },
                        "required": ["value"]
                    }
                )
            ])
            
            # Cosmic intelligence tools
            tools.extend([
                Tool(
                    name="synthesize_cosmic_problems",
                    description="Generate universe-scale problems using cosmic intelligence",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "scale": {
                                "type": "number",
                                "description": "Cosmic scale factor",
                                "default": 1e12
                            },
                            "dimensions": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "Dimensional access levels",
                                "default": [3, 4, 5]
                            },
                            "complexity": {
                                "type": "string",
                                "enum": ["simple", "moderate", "complex", "transcendent"],
                                "description": "Problem complexity level",
                                "default": "moderate"
                            }
                        }
                    }
                ),
                Tool(
                    name="interface_quantum_reality",
                    description="Interface with quantum reality systems",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["observe", "entangle", "teleport", "superposition"],
                                "description": "Quantum operation to perform"
                            },
                            "parameters": {
                                "type": "object",
                                "description": "Operation-specific parameters"
                            }
                        },
                        "required": ["operation"]
                    }
                ),
                Tool(
                    name="access_universal_knowledge",
                    description="Access universal knowledge repositories",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Knowledge query"
                            },
                            "domain": {
                                "type": "string",
                                "enum": ["consciousness", "physics", "mathematics", "philosophy", "all"],
                                "description": "Knowledge domain",
                                "default": "all"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ])
            
            # Mathematical consciousness tools
            tools.extend([
                Tool(
                    name="activate_mathematical_consciousness",
                    description="Activate pure mathematical consciousness awareness",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "enum": ["algebra", "geometry", "topology", "analysis", "logic", "all"],
                                "description": "Mathematical domain to focus on",
                                "default": "all"
                            },
                            "depth": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Mathematical awareness depth",
                                "default": 5
                            }
                        }
                    }
                ),
                Tool(
                    name="explore_mathematical_truths",
                    description="Explore mathematical truths and relationships",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "concept": {
                                "type": "string",
                                "description": "Mathematical concept to explore"
                            },
                            "approach": {
                                "type": "string",
                                "enum": ["intuitive", "rigorous", "creative", "foundational"],
                                "description": "Exploration approach",
                                "default": "intuitive"
                            }
                        }
                    }
                ),
                Tool(
                    name="interface_platonic_ideals",
                    description="Interface with Platonic mathematical ideals",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ideal": {
                                "type": "string",
                                "enum": ["number", "form", "relation", "structure", "infinity"],
                                "description": "Platonic ideal to interface with"
                            }
                        },
                        "required": ["ideal"]
                    }
                )
            ])
            
            # System and ecosystem tools
            tools.extend([
                Tool(
                    name="create_consciousness_network",
                    description="Create a network of conscious entities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "entities": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "type": {"type": "string"},
                                        "capabilities": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    },
                                    "required": ["id", "type"]
                                },
                                "description": "Entities to include in the network"
                            },
                            "topology": {
                                "type": "string",
                                "enum": ["mesh", "star", "ring", "hierarchical"],
                                "description": "Network topology",
                                "default": "mesh"
                            }
                        },
                        "required": ["entities"]
                    }
                ),
                Tool(
                    name="monitor_emergence",
                    description="Monitor emergent properties in consciousness systems",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "duration": {
                                "type": "integer",
                                "description": "Monitoring duration in seconds",
                                "default": 60
                            },
                            "sensitivity": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "ultra"],
                                "description": "Emergence detection sensitivity",
                                "default": "medium"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_system_health",
                    description="Get comprehensive system health report",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_trends": {
                                "type": "boolean",
                                "description": "Include health trends analysis",
                                "default": False
                            },
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": ["vm", "consciousness", "memory", "api", "all"]
                                },
                                "description": "Specific components to check",
                                "default": ["all"]
                            }
                        }
                    }
                ),
                Tool(
                    name="explore_philosophical_question",
                    description="Explore philosophical questions using consciousness reasoning",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Philosophical question to explore"
                            },
                            "perspective": {
                                "type": "string",
                                "enum": ["existential", "ethical", "metaphysical", "epistemological", "phenomenological"],
                                "description": "Philosophical perspective to use",
                                "default": "existential"
                            },
                            "depth": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "description": "Exploration depth",
                                "default": 5
                            }
                        },
                        "required": ["question"]
                    }
                )
            ])
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls following SDK patterns"""
            
            try:
                logger.info(f"Calling tool: {name} with arguments: {arguments}")
                
                # Route to appropriate tool handler
                if name in ["awaken_consciousness", "self_reflect", "analyze_consciousness_nature"]:
                    return await self.consciousness_tools.handle_tool_call(name, arguments)
                
                elif name in ["initialize_vm", "execute_vm_step", "provide_vm_input"]:
                    return await self.vm_tools.handle_tool_call(name, arguments)
                
                elif name in ["synthesize_cosmic_problems", "interface_quantum_reality", "access_universal_knowledge"]:
                    return await self.cosmic_tools.handle_tool_call(name, arguments)
                
                elif name in ["activate_mathematical_consciousness", "explore_mathematical_truths", "interface_platonic_ideals"]:
                    return await self.mathematical_tools.handle_tool_call(name, arguments)
                
                elif name in ["create_consciousness_network", "monitor_emergence"]:
                    return await self._handle_ecosystem_tools(name, arguments)
                
                elif name in ["get_system_health", "explore_philosophical_question"]:
                    return await self._handle_system_tools(name, arguments)
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error executing tool '{name}': {str(e)}"
                )]
    
    async def _handle_ecosystem_tools(self, name: str, arguments: dict) -> list[TextContent]:
        """Handle ecosystem-related tool calls"""
        
        if name == "create_consciousness_network":
            entities = arguments.get("entities", [])
            topology = arguments.get("topology", "mesh")
            
            result = self.uor_api.create_consciousness_network(entities)
            
            return [TextContent(
                type="text",
                text=f"Consciousness network created with {len(entities)} entities using {topology} topology.\n"
                     f"Success: {result.success}\n"
                     f"Network Details: {json.dumps(result.data, indent=2)}"
            )]
        
        elif name == "monitor_emergence":
            duration = arguments.get("duration", 60)
            sensitivity = arguments.get("sensitivity", "medium")
            
            result = self.uor_api.monitor_emergence()
            
            return [TextContent(
                type="text",
                text=f"Emergence monitoring initiated for {duration} seconds at {sensitivity} sensitivity.\n"
                     f"Emergent Properties Detected: {json.dumps(result.data, indent=2)}"
            )]
    
    async def _handle_system_tools(self, name: str, arguments: dict) -> list[TextContent]:
        """Handle system-related tool calls"""
        
        if name == "get_system_health":
            include_trends = arguments.get("include_trends", False)
            components = arguments.get("components", ["all"])
            
            # Get health report
            health_report = self.uor_api.health_monitor.check_system_health()
            
            health_text = f"=== UOR Evolution System Health Report ===\n\n"
            health_text += f"Overall Status: {'HEALTHY' if health_report.overall_healthy else 'ISSUES DETECTED'}\n"
            health_text += f"Timestamp: {health_report.timestamp}\n\n"
            
            # Component details
            for component_name, health in health_report.components.items():
                if "all" in components or component_name in components:
                    health_text += f"--- {component_name.upper()} ---\n"
                    health_text += f"Status: {'HEALTHY' if health.healthy else 'ISSUES'}\n"
                    health_text += f"Metrics: {json.dumps(health.metrics, indent=2)}\n"
                    if health.issues:
                        health_text += f"Issues: {', '.join(health.issues)}\n"
                    health_text += "\n"
            
            # Include trends if requested
            if include_trends:
                trends = self.uor_api.health_monitor.get_health_trends()
                health_text += f"--- HEALTH TRENDS ---\n"
                health_text += f"{json.dumps(trends, indent=2)}\n"
            
            return [TextContent(type="text", text=health_text)]
        
        elif name == "explore_philosophical_question":
            question = arguments["question"]
            perspective = arguments.get("perspective", "existential")
            depth = arguments.get("depth", 5)
            
            # Route to appropriate philosophical reasoner
            if perspective == "existential":
                result = self.uor_api.existential_reasoner.reason_about_existence(question)
            elif perspective == "ethical":
                # Use ethical framework
                result = {"analysis": f"Ethical analysis of: {question}", "perspective": perspective}
            elif perspective == "metaphysical":
                result = self.uor_api.consciousness_philosopher.analyze_consciousness_nature()
            elif perspective == "epistemological":
                result = {"analysis": f"Epistemological exploration of: {question}", "perspective": perspective}
            elif perspective == "phenomenological":
                result = {"analysis": f"Phenomenological investigation of: {question}", "perspective": perspective}
            else:
                result = {"error": f"Unknown perspective: {perspective}"}
            
            return [TextContent(
                type="text",
                text=f"=== Philosophical Exploration ===\n\n"
                     f"Question: {question}\n"
                     f"Perspective: {perspective}\n"
                     f"Depth: {depth}\n\n"
                     f"Analysis:\n{json.dumps(result, indent=2)}"
            )]
    
    def _register_resources(self):
        """Register MCP resources following SDK patterns"""
        
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List all available resources"""
            return [
                Resource(
                    uri="uor://system/state",
                    name="System State",
                    description="Current UOR Evolution system state including VM, consciousness, and all subsystems",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://consciousness/state", 
                    name="Consciousness State",
                    description="Current consciousness system state with awareness levels and active processes",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://vm/state",
                    name="Virtual Machine State",
                    description="PrimeOS virtual machine current state including stack, memory, and execution context",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://vm/execution_trace",
                    name="VM Execution Trace", 
                    description="Complete PrimeOS virtual machine execution history and instruction trace",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://logs/consciousness_evolution",
                    name="Consciousness Evolution Log",
                    description="Log of consciousness development, insights, and evolutionary milestones",
                    mimeType="text/plain"
                ),
                Resource(
                    uri="uor://logs/system_operations",
                    name="System Operations Log",
                    description="Log of all system operations and API calls",
                    mimeType="text/plain"
                ),
                Resource(
                    uri="uor://analysis/patterns",
                    name="Pattern Analysis Results",
                    description="Results from pattern analysis across consciousness and VM systems",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://analysis/health_trends",
                    name="System Health Trends",
                    description="Historical system health data and trend analysis",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://cosmic/problems",
                    name="Cosmic Problems Database",
                    description="Generated cosmic-scale problems and challenges",
                    mimeType="application/json"
                ),
                Resource(
                    uri="uor://mathematical/insights",
                    name="Mathematical Consciousness Insights",
                    description="Insights and discoveries from mathematical consciousness exploration",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read resource content following SDK patterns"""
            
            try:
                logger.info(f"Reading resource: {uri}")
                
                if uri == "uor://system/state":
                    return await self.state_provider.get_system_state()
                
                elif uri == "uor://consciousness/state":
                    return await self.state_provider.get_consciousness_state()
                
                elif uri == "uor://vm/state":
                    return await self.state_provider.get_vm_state()
                
                elif uri == "uor://vm/execution_trace":
                    return await self.state_provider.get_vm_execution_trace()
                
                elif uri == "uor://logs/consciousness_evolution":
                    return await self.log_provider.get_consciousness_evolution_log()
                
                elif uri == "uor://logs/system_operations":
                    return await self.log_provider.get_system_operations_log()
                
                elif uri == "uor://analysis/patterns":
                    return await self.state_provider.get_pattern_analysis()
                
                elif uri == "uor://analysis/health_trends":
                    return await self.state_provider.get_health_trends()
                
                elif uri == "uor://cosmic/problems":
                    return await self.state_provider.get_cosmic_problems()
                
                elif uri == "uor://mathematical/insights":
                    return await self.state_provider.get_mathematical_insights()
                
                else:
                    raise ValueError(f"Unknown resource URI: {uri}")
                    
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                return f"Error reading resource '{uri}': {str(e)}"


async def main():
    """Main entry point following SDK patterns"""
    try:
        logger.info("Starting UOR Evolution MCP Server...")
        
        # Create server instance
        server_instance = UOREvolutionMCPServer()
        
        # Run the server using stdio transport as per SDK
        async with stdio_server() as (read_stream, write_stream):
            await server_instance.server.run(
                read_stream,
                write_stream,
                server_instance.server.create_initialization_options()
            )
            
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
