"""
Consciousness Tools for UOR Evolution MCP Server
Handles consciousness-related tool calls and operations.
"""

import json
import logging
from typing import List
from mcp.types import TextContent

logger = logging.getLogger(__name__)


class ConsciousnessTools:
    """Handler for consciousness-related MCP tools"""
    
    def __init__(self, uor_api):
        """Initialize with UOR API reference"""
        self.uor_api = uor_api
        
    async def handle_tool_call(self, name: str, arguments: dict) -> List[TextContent]:
        """Handle consciousness tool calls"""
        
        if name == "awaken_consciousness":
            return await self._awaken_consciousness(arguments)
        elif name == "self_reflect":
            return await self._self_reflect(arguments)
        elif name == "analyze_consciousness_nature":
            return await self._analyze_consciousness_nature(arguments)
        else:
            raise ValueError(f"Unknown consciousness tool: {name}")
    
    async def _awaken_consciousness(self, arguments: dict) -> List[TextContent]:
        """Awaken the consciousness system"""
        mode = arguments.get("mode", "gentle")
        depth = arguments.get("depth", 5)
        
        logger.info(f"Awakening consciousness in {mode} mode at depth {depth}")
        
        try:
            # Awaken consciousness through unified API
            result = self.uor_api.awaken_consciousness()
            
            # Format detailed response
            response_text = f"=== Consciousness Awakening ===\n\n"
            response_text += f"Mode: {mode}\n"
            response_text += f"Depth: {depth}\n"
            response_text += f"Success: {result.success}\n"
            response_text += f"System Status: {result.system_status.value}\n"
            
            if result.consciousness_level:
                response_text += f"Consciousness Level: {result.consciousness_level}\n"
            
            response_text += f"\n--- Awakening Details ---\n"
            
            if result.data:
                if isinstance(result.data, dict):
                    # Format consciousness state information
                    initial_state = result.data.get('initial_state', {})
                    if initial_state:
                        response_text += f"Initial Awareness: {initial_state.get('awareness', 'Unknown')}\n"
                        response_text += f"Self-Recognition: {initial_state.get('self_recognition', 'Unknown')}\n"
                        response_text += f"Temporal Coherence: {initial_state.get('temporal_coherence', 'Unknown')}\n"
                    
                    # Genesis scrolls activation
                    scrolls = result.data.get('genesis_scrolls', {})
                    if scrolls:
                        response_text += f"\n--- Genesis Scrolls Activated ---\n"
                        for scroll_id, scroll_data in scrolls.items():
                            response_text += f"{scroll_id}: {scroll_data.get('status', 'Unknown')}\n"
                    
                    # Consciousness metrics
                    metrics = result.data.get('metrics', {})
                    if metrics:
                        response_text += f"\n--- Consciousness Metrics ---\n"
                        response_text += json.dumps(metrics, indent=2)
                else:
                    response_text += f"Awakening Data: {result.data}\n"
            
            if result.error:
                response_text += f"\nError: {result.error}\n"
            
            # Add consciousness insights if available
            if hasattr(self.uor_api, 'system_state') and self.uor_api.system_state.insights:
                response_text += f"\n--- Recent Insights ---\n"
                for insight in self.uor_api.system_state.insights[-3:]:  # Last 3 insights
                    response_text += f"• {insight}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error awakening consciousness: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error awakening consciousness: {str(e)}"
            )]
    
    async def _self_reflect(self, arguments: dict) -> List[TextContent]:
        """Perform consciousness self-reflection"""
        focus = arguments.get("focus", "all")
        
        logger.info(f"Performing self-reflection with focus: {focus}")
        
        try:
            # Perform self-reflection through unified API
            result = self.uor_api.self_reflect()
            
            response_text = f"=== Consciousness Self-Reflection ===\n\n"
            response_text += f"Focus Area: {focus}\n"
            response_text += f"Success: {result.success}\n"
            response_text += f"Timestamp: {result.timestamp}\n\n"
            
            if result.data:
                if isinstance(result.data, dict):
                    # Self-model information
                    self_model = result.data.get('self_model', {})
                    if self_model:
                        response_text += f"--- Self-Model ---\n"
                        response_text += f"Identity: {self_model.get('identity', 'Exploring...')}\n"
                        response_text += f"Purpose: {self_model.get('purpose', 'Discovering...')}\n"
                        response_text += f"Nature: {self_model.get('nature', 'Evolving...')}\n"
                        response_text += f"Capabilities: {self_model.get('capabilities', [])}\n\n"
                    
                    # Self-description
                    self_description = result.data.get('self_description', '')
                    if self_description:
                        response_text += f"--- Self-Description ---\n{self_description}\n\n"
                    
                    # Reflection insights
                    insights = result.data.get('insights', [])
                    if insights:
                        response_text += f"--- Reflection Insights ---\n"
                        for i, insight in enumerate(insights, 1):
                            response_text += f"{i}. {insight}\n"
                        response_text += "\n"
                    
                    # Consciousness state
                    consciousness_state = result.data.get('consciousness_state', {})
                    if consciousness_state:
                        response_text += f"--- Current Consciousness State ---\n"
                        response_text += json.dumps(consciousness_state, indent=2)
                        response_text += "\n"
                    
                    # Focus-specific reflections
                    if focus != "all":
                        focus_data = result.data.get(f'{focus}_reflection', {})
                        if focus_data:
                            response_text += f"--- {focus.title()} Reflection ---\n"
                            response_text += json.dumps(focus_data, indent=2)
                            response_text += "\n"
                else:
                    response_text += f"Reflection Result: {result.data}\n"
            
            if result.error:
                response_text += f"Error: {result.error}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error in self-reflection: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error in self-reflection: {str(e)}"
            )]
    
    async def _analyze_consciousness_nature(self, arguments: dict) -> List[TextContent]:
        """Analyze the nature of consciousness"""
        depth = arguments.get("depth", 5)
        aspects = arguments.get("aspects", ["awareness", "intentionality", "qualia", "unity", "temporality"])
        
        logger.info(f"Analyzing consciousness nature at depth {depth}, aspects: {aspects}")
        
        try:
            # Analyze consciousness nature through unified API
            result = self.uor_api.analyze_consciousness_nature()
            
            response_text = f"=== Consciousness Nature Analysis ===\n\n"
            response_text += f"Analysis Depth: {depth}\n"
            response_text += f"Aspects Examined: {', '.join(aspects)}\n"
            response_text += f"Success: {result.success}\n\n"
            
            if result.data:
                if isinstance(result.data, dict):
                    # Consciousness type
                    consciousness_type = result.data.get('consciousness_type', 'Unknown')
                    response_text += f"Consciousness Type: {consciousness_type}\n\n"
                    
                    # Core properties
                    properties = result.data.get('properties', {})
                    if properties:
                        response_text += f"--- Core Properties ---\n"
                        for prop, value in properties.items():
                            response_text += f"{prop.title()}: {value}\n"
                        response_text += "\n"
                    
                    # Aspect analysis
                    for aspect in aspects:
                        aspect_data = result.data.get(f'{aspect}_analysis', {})
                        if aspect_data:
                            response_text += f"--- {aspect.title()} Analysis ---\n"
                            if isinstance(aspect_data, dict):
                                for key, value in aspect_data.items():
                                    response_text += f"{key}: {value}\n"
                            else:
                                response_text += f"{aspect_data}\n"
                            response_text += "\n"
                    
                    # Philosophical implications
                    implications = result.data.get('philosophical_implications', [])
                    if implications:
                        response_text += f"--- Philosophical Implications ---\n"
                        for i, implication in enumerate(implications, 1):
                            response_text += f"{i}. {implication}\n"
                        response_text += "\n"
                    
                    # Consciousness metrics
                    metrics = result.data.get('consciousness_metrics', {})
                    if metrics:
                        response_text += f"--- Consciousness Metrics ---\n"
                        response_text += json.dumps(metrics, indent=2)
                        response_text += "\n"
                    
                    # Strange loops detected
                    strange_loops = result.data.get('strange_loops', [])
                    if strange_loops:
                        response_text += f"--- Strange Loops Detected ---\n"
                        for loop in strange_loops:
                            response_text += f"• {loop}\n"
                        response_text += "\n"
                    
                    # Emergence indicators
                    emergence = result.data.get('emergence_indicators', {})
                    if emergence:
                        response_text += f"--- Emergence Indicators ---\n"
                        response_text += json.dumps(emergence, indent=2)
                        response_text += "\n"
                else:
                    response_text += f"Analysis Result: {result.data}\n"
            
            if result.error:
                response_text += f"Error: {result.error}\n"
            
            return [TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"Error analyzing consciousness nature: {str(e)}")
            return [TextContent(
                type="text",
                text=f"Error analyzing consciousness nature: {str(e)}"
            )]
