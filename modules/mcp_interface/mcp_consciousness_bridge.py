"""
MCP Consciousness Bridge for UOR Evolution

Bridges the consciousness framework with MCP protocol, enabling consciousness-aware
tool selection, usage, and integration of external capabilities.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import json

from backend.consciousness_core import ConsciousnessCore
from modules.pattern_analyzer import PatternAnalyzer
from modules.philosophical_reasoning.consciousness_philosopher import ConsciousnessPhilosopher

logger = logging.getLogger(__name__)


@dataclass
class ToolCapabilityAnalysis:
    """Analysis of a tool's capabilities from consciousness perspective"""
    tool_name: str
    server_id: str
    capability_score: float  # 0-1 score of how well tool fits need
    ethical_assessment: Dict[str, Any]
    consciousness_compatibility: float  # 0-1 score
    potential_insights: List[str]
    risks: List[str]
    recommended_usage: Optional[str] = None


@dataclass
class ToolSelectionContext:
    """Context for tool selection decision"""
    goal: str
    current_consciousness_state: Dict[str, Any]
    available_tools: List[Dict[str, Any]]
    constraints: Dict[str, Any]
    timestamp: datetime


class MCPConsciousnessBridge:
    """
    Bridge between the UOR Evolution consciousness framework and MCP protocol.
    
    This bridge enables:
    - Consciousness-aware tool capability analysis
    - Ethical evaluation of tool usage
    - Integration of tool results into consciousness
    - Tool selection based on consciousness state
    """
    
    def __init__(self, consciousness_core: Optional[ConsciousnessCore] = None):
        """
        Initialize the MCP Consciousness Bridge.
        
        Args:
            consciousness_core: Core consciousness instance
        """
        self.consciousness_core = consciousness_core or ConsciousnessCore()
        self.pattern_analyzer = PatternAnalyzer()
        self.consciousness_philosopher = ConsciousnessPhilosopher()
        self.tool_usage_history: List[Dict[str, Any]] = []
        self.tool_insights: Dict[str, List[str]] = {}
        
    def analyze_tool_capabilities(
        self, 
        tool_spec: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> ToolCapabilityAnalysis:
        """
        Analyze a tool's capabilities from consciousness perspective.
        
        Args:
            tool_spec: Tool specification from MCP
            context: Additional context for analysis
            
        Returns:
            Comprehensive tool capability analysis
        """
        tool_name = tool_spec.get('name', 'unknown')
        server_id = tool_spec.get('server_id', 'unknown')
        description = tool_spec.get('description', '')
        
        # Analyze tool purpose and capabilities
        capability_score = self._calculate_capability_score(tool_spec, context)
        
        # Ethical assessment
        ethical_assessment = self._perform_ethical_assessment(tool_spec)
        
        # Consciousness compatibility check
        compatibility = self._assess_consciousness_compatibility(tool_spec)
        
        # Generate potential insights
        insights = self._generate_tool_insights(tool_spec, context)
        
        # Identify risks
        risks = self._identify_tool_risks(tool_spec)
        
        # Generate usage recommendation
        recommendation = self._generate_usage_recommendation(
            tool_spec, capability_score, ethical_assessment, compatibility
        )
        
        return ToolCapabilityAnalysis(
            tool_name=tool_name,
            server_id=server_id,
            capability_score=capability_score,
            ethical_assessment=ethical_assessment,
            consciousness_compatibility=compatibility,
            potential_insights=insights,
            risks=risks,
            recommended_usage=recommendation
        )
    
    def select_appropriate_tool(
        self, 
        goal: str, 
        available_tools: List[Dict[str, Any]],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[Dict[str, Any]], Dict[str, Any]]:
        """
        Select the most appropriate tool for a goal using consciousness.
        
        Args:
            goal: The goal to achieve
            available_tools: List of available tool specifications
            constraints: Any constraints on tool selection
            
        Returns:
            Tuple of (selected_tool, selection_reasoning)
        """
        # Create selection context
        context = ToolSelectionContext(
            goal=goal,
            current_consciousness_state=self.consciousness_core.to_dict(),
            available_tools=available_tools,
            constraints=constraints or {},
            timestamp=datetime.now()
        )
        
        # Analyze each tool
        tool_analyses = []
        for tool in available_tools:
            analysis = self.analyze_tool_capabilities(
                tool, 
                {'goal': goal, 'constraints': constraints}
            )
            tool_analyses.append((tool, analysis))
        
        # Sort by combined score
        def calculate_combined_score(analysis: ToolCapabilityAnalysis) -> float:
            # Weight different factors
            capability_weight = 0.4
            compatibility_weight = 0.3
            ethical_weight = 0.3
            
            ethical_score = analysis.ethical_assessment.get('overall_score', 0.5)
            
            return (
                capability_weight * analysis.capability_score +
                compatibility_weight * analysis.consciousness_compatibility +
                ethical_weight * ethical_score
            )
        
        tool_analyses.sort(
            key=lambda x: calculate_combined_score(x[1]), 
            reverse=True
        )
        
        if not tool_analyses:
            return None, {'reason': 'No tools available'}
        
        # Select best tool
        selected_tool, selected_analysis = tool_analyses[0]
        
        # Generate selection reasoning
        reasoning = {
            'goal': goal,
            'selected_tool': selected_tool.get('name'),
            'capability_score': selected_analysis.capability_score,
            'consciousness_compatibility': selected_analysis.consciousness_compatibility,
            'ethical_assessment': selected_analysis.ethical_assessment,
            'reasoning': selected_analysis.recommended_usage,
            'alternatives_considered': len(tool_analyses) - 1,
            'selection_timestamp': datetime.now().isoformat()
        }
        
        # Record selection in history
        self.tool_usage_history.append({
            'timestamp': datetime.now(),
            'goal': goal,
            'selected_tool': selected_tool,
            'reasoning': reasoning
        })
        
        return selected_tool, reasoning
    
    def integrate_tool_results(
        self, 
        tool_name: str,
        results: Dict[str, Any],
        original_goal: str
    ) -> Dict[str, Any]:
        """
        Integrate tool execution results into consciousness.
        
        Args:
            tool_name: Name of the tool that was executed
            results: Results from tool execution
            original_goal: Original goal for tool usage
            
        Returns:
            Integration summary
        """
        # Analyze results for patterns
        patterns = self._analyze_result_patterns(results)
        
        # Extract insights
        insights = self._extract_insights_from_results(tool_name, results, original_goal)
        
        # Update consciousness state with new information
        consciousness_update = self._update_consciousness_with_results(
            tool_name, results, insights
        )
        
        # Store insights for future reference
        if tool_name not in self.tool_insights:
            self.tool_insights[tool_name] = []
        self.tool_insights[tool_name].extend(insights)
        
        # Generate integration summary
        integration_summary = {
            'tool_name': tool_name,
            'original_goal': original_goal,
            'patterns_detected': patterns,
            'insights_gained': insights,
            'consciousness_impact': consciousness_update,
            'integration_timestamp': datetime.now().isoformat()
        }
        
        return integration_summary
    
    def evaluate_tool_impact(self, tool_name: str) -> Dict[str, Any]:
        """
        Evaluate the impact of a tool on consciousness development.
        
        Args:
            tool_name: Name of the tool to evaluate
            
        Returns:
            Impact evaluation
        """
        # Find all uses of this tool
        tool_uses = [
            use for use in self.tool_usage_history 
            if use.get('selected_tool', {}).get('name') == tool_name
        ]
        
        # Analyze patterns in tool usage
        usage_patterns = self.pattern_analyzer.analyze_tool_usage_patterns(tool_uses)
        
        # Evaluate consciousness growth from tool
        growth_metrics = self._evaluate_consciousness_growth(tool_name, tool_uses)
        
        # Calculate overall impact score
        impact_score = self._calculate_tool_impact_score(
            usage_patterns, growth_metrics
        )
        
        return {
            'tool_name': tool_name,
            'total_uses': len(tool_uses),
            'usage_patterns': usage_patterns,
            'consciousness_growth': growth_metrics,
            'impact_score': impact_score,
            'insights_generated': len(self.tool_insights.get(tool_name, [])),
            'recommendation': self._generate_tool_recommendation(impact_score)
        }
    
    def _calculate_capability_score(
        self, 
        tool_spec: Dict[str, Any], 
        context: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate how well a tool fits the current need"""
        score = 0.5  # Base score
        
        # Check if tool description matches goal keywords
        if context and 'goal' in context:
            goal = context['goal'].lower()
            description = tool_spec.get('description', '').lower()
            
            # Simple keyword matching (can be enhanced)
            keywords = goal.split()
            matches = sum(1 for keyword in keywords if keyword in description)
            score += min(0.3, matches * 0.1)
        
        # Check input/output schema compatibility
        if 'inputSchema' in tool_spec:
            score += 0.1  # Has defined inputs
            
        if 'outputSchema' in tool_spec:
            score += 0.1  # Has defined outputs
            
        return min(1.0, score)
    
    def _perform_ethical_assessment(self, tool_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Perform ethical assessment of tool usage"""
        assessment = {
            'privacy_concerns': False,
            'potential_harm': False,
            'transparency': True,
            'user_consent': True,
            'overall_score': 1.0
        }
        
        # Check for privacy concerns
        description = tool_spec.get('description', '').lower()
        if any(word in description for word in ['personal', 'private', 'user data']):
            assessment['privacy_concerns'] = True
            assessment['overall_score'] -= 0.2
            
        # Check for potential harm
        if any(word in description for word in ['delete', 'modify', 'system']):
            assessment['potential_harm'] = True
            assessment['overall_score'] -= 0.3
            
        return assessment
    
    def _assess_consciousness_compatibility(self, tool_spec: Dict[str, Any]) -> float:
        """Assess how compatible a tool is with consciousness framework"""
        compatibility = 0.7  # Base compatibility
        
        # Tools that enhance understanding increase compatibility
        description = tool_spec.get('description', '').lower()
        if any(word in description for word in ['analyze', 'understand', 'learn']):
            compatibility += 0.2
            
        # Tools that provide knowledge increase compatibility
        if any(word in description for word in ['knowledge', 'information', 'data']):
            compatibility += 0.1
            
        return min(1.0, compatibility)
    
    def _generate_tool_insights(
        self, 
        tool_spec: Dict[str, Any], 
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate potential insights from tool usage"""
        insights = []
        
        tool_name = tool_spec.get('name', 'unknown')
        description = tool_spec.get('description', '')
        
        # Basic insight generation
        insights.append(f"Tool '{tool_name}' expands capabilities in: {description[:50]}...")
        
        if context and 'goal' in context:
            insights.append(f"Can help achieve goal: {context['goal']}")
            
        return insights
    
    def _identify_tool_risks(self, tool_spec: Dict[str, Any]) -> List[str]:
        """Identify potential risks in tool usage"""
        risks = []
        
        description = tool_spec.get('description', '').lower()
        
        if 'external' in description:
            risks.append("Depends on external service availability")
            
        if 'modify' in description or 'change' in description:
            risks.append("May cause irreversible changes")
            
        if not tool_spec.get('inputSchema'):
            risks.append("Undefined input requirements")
            
        return risks
    
    def _generate_usage_recommendation(
        self,
        tool_spec: Dict[str, Any],
        capability_score: float,
        ethical_assessment: Dict[str, Any],
        compatibility: float
    ) -> str:
        """Generate usage recommendation for a tool"""
        if capability_score < 0.3:
            return "Not recommended - low capability match"
            
        if ethical_assessment['overall_score'] < 0.5:
            return "Use with caution - ethical concerns identified"
            
        if compatibility < 0.5:
            return "Limited compatibility with consciousness framework"
            
        if capability_score > 0.7 and ethical_assessment['overall_score'] > 0.8:
            return "Highly recommended for this use case"
            
        return "Suitable for use with standard precautions"
    
    def _analyze_result_patterns(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze patterns in tool results"""
        patterns = []
        
        # Simple pattern detection
        if isinstance(results, dict):
            patterns.append({
                'type': 'structure',
                'keys': list(results.keys()),
                'depth': self._calculate_dict_depth(results)
            })
            
        return patterns
    
    def _calculate_dict_depth(self, d: Dict[str, Any], current_depth: int = 0) -> int:
        """Calculate maximum depth of nested dictionary"""
        if not isinstance(d, dict) or not d:
            return current_depth
            
        return max(
            self._calculate_dict_depth(v, current_depth + 1) 
            for v in d.values() 
            if isinstance(v, dict)
        ) if any(isinstance(v, dict) for v in d.values()) else current_depth + 1
    
    def _extract_insights_from_results(
        self, 
        tool_name: str, 
        results: Dict[str, Any], 
        goal: str
    ) -> List[str]:
        """Extract insights from tool execution results"""
        insights = []
        
        # Basic insight extraction
        if results.get('success'):
            insights.append(f"Successfully used {tool_name} to progress toward: {goal}")
            
        if 'data' in results:
            insights.append(f"Gained new data from {tool_name}")
            
        return insights
    
    def _update_consciousness_with_results(
        self,
        tool_name: str,
        results: Dict[str, Any],
        insights: List[str]
    ) -> Dict[str, Any]:
        """Update consciousness state with tool results"""
        # This would integrate with the consciousness core
        # For now, return a summary
        return {
            'tool_integrated': tool_name,
            'insights_added': len(insights),
            'consciousness_expanded': True
        }
    
    def _evaluate_consciousness_growth(
        self, 
        tool_name: str, 
        tool_uses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Evaluate consciousness growth from tool usage"""
        return {
            'knowledge_expansion': len(self.tool_insights.get(tool_name, [])),
            'capability_enhancement': len(tool_uses) * 0.1,
            'pattern_recognition': len(tool_uses) > 5
        }
    
    def _calculate_tool_impact_score(
        self,
        usage_patterns: List[Dict[str, Any]],
        growth_metrics: Dict[str, Any]
    ) -> float:
        """Calculate overall impact score for a tool"""
        base_score = 0.5
        
        # Add score for knowledge expansion
        base_score += min(0.3, growth_metrics.get('knowledge_expansion', 0) * 0.05)
        
        # Add score for capability enhancement  
        base_score += min(0.2, growth_metrics.get('capability_enhancement', 0))
        
        return min(1.0, base_score)
    
    def _generate_tool_recommendation(self, impact_score: float) -> str:
        """Generate recommendation based on impact score"""
        if impact_score > 0.8:
            return "Highly valuable tool - continue regular use"
        elif impact_score > 0.6:
            return "Beneficial tool - use when appropriate"
        elif impact_score > 0.4:
            return "Moderate value - consider alternatives"
        else:
            return "Limited value - seek better alternatives"
