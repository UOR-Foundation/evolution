"""
State Provider for UOR Evolution MCP Server
Provides access to system state, analysis results, and metrics.
"""

import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class StateProvider:
    """Provider for system state and analysis resources"""
    
    def __init__(self, uor_api):
        """Initialize with UOR API reference"""
        self.uor_api = uor_api
        
    async def get_system_state(self) -> str:
        """Get complete system state as JSON"""
        try:
            # Get system state through unified API
            result = self.uor_api.get_system_state()
            
            if result.success and result.data:
                system_state = {
                    "timestamp": datetime.now().isoformat(),
                    "system_status": result.system_status.value,
                    "api_mode": self.uor_api.mode.value,
                    "session_id": self.uor_api.session_id,
                    "state_data": result.data
                }
                
                # Add VM registry information
                if hasattr(self.uor_api, 'vm_registry'):
                    system_state["vm_registry"] = {
                        "vm_id": self.uor_api.vm_registry.get_vm_id(),
                        "vm_instance_active": self.uor_api.vm_registry._vm_instance is not None
                    }
                
                # Add operation history
                if hasattr(self.uor_api, 'operation_history'):
                    system_state["operation_history"] = self.uor_api.operation_history[-10:]  # Last 10 operations
                
                return json.dumps(system_state, indent=2)
            else:
                return json.dumps({
                    "error": "Failed to retrieve system state",
                    "timestamp": datetime.now().isoformat()
                }, indent=2)
                
        except Exception as e:
            logger.error(f"Error getting system state: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving system state: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_consciousness_state(self) -> str:
        """Get consciousness system state as JSON"""
        try:
            consciousness_state = {
                "timestamp": datetime.now().isoformat(),
                "consciousness_active": self.uor_api.consciousness_core.consciousness_active,
                "system_state": self.uor_api.system_state.consciousness_state,
                "insights": self.uor_api.system_state.insights,
                "philosophical_state": self.uor_api.system_state.philosophical_state
            }
            
            # Add consciousness core details
            if hasattr(self.uor_api.consciousness_core, 'to_dict'):
                consciousness_state["consciousness_core"] = self.uor_api.consciousness_core.to_dict()
            
            # Add consciousness level from VM
            if hasattr(self.uor_api.prime_vm, 'consciousness_level'):
                consciousness_state["vm_consciousness_level"] = self.uor_api.prime_vm.consciousness_level.value
            
            return json.dumps(consciousness_state, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting consciousness state: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving consciousness state: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_vm_state(self) -> str:
        """Get virtual machine state as JSON"""
        try:
            vm_state = {
                "timestamp": datetime.now().isoformat(),
                "vm_id": self.uor_api.vm_registry.get_vm_id(),
                "system_vm_state": self.uor_api.system_state.vm_state
            }
            
            # Add VM details if available
            if hasattr(self.uor_api.prime_vm, 'capture_state'):
                vm_state["detailed_vm_state"] = self.uor_api.prime_vm.capture_state()
            
            # Add VM statistics
            if hasattr(self.uor_api, 'orchestrator') and hasattr(self.uor_api.orchestrator, 'vm_monitor'):
                vm_stats = self.uor_api.orchestrator.vm_monitor.get_operation_statistics()
                vm_state["operation_statistics"] = vm_stats
            
            return json.dumps(vm_state, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting VM state: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving VM state: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_vm_execution_trace(self) -> str:
        """Get VM execution trace as JSON"""
        try:
            execution_trace = {
                "timestamp": datetime.now().isoformat(),
                "vm_id": self.uor_api.vm_registry.get_vm_id()
            }
            
            # Get execution history from VM
            if hasattr(self.uor_api.prime_vm, 'execution_history'):
                execution_trace["execution_history"] = self.uor_api.prime_vm.execution_history[-100:]  # Last 100 instructions
            
            # Get execution trace from VM monitor
            if hasattr(self.uor_api, 'orchestrator') and hasattr(self.uor_api.orchestrator, 'vm_monitor'):
                monitor_stats = self.uor_api.orchestrator.vm_monitor.get_operation_statistics()
                execution_trace["monitor_statistics"] = monitor_stats
            
            # Get stack trace if available
            if hasattr(self.uor_api.prime_vm, 'stack'):
                execution_trace["current_stack"] = list(self.uor_api.prime_vm.stack)[-20:]  # Last 20 stack items
            
            return json.dumps(execution_trace, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting VM execution trace: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving VM execution trace: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_pattern_analysis(self) -> str:
        """Get pattern analysis results as JSON"""
        try:
            pattern_analysis = {
                "timestamp": datetime.now().isoformat(),
                "patterns": self.uor_api.system_state.patterns
            }
            
            # Get pattern analysis from pattern analyzer
            if hasattr(self.uor_api, 'pattern_analyzer'):
                # Analyze current execution patterns
                if hasattr(self.uor_api.prime_vm, 'execution_history'):
                    patterns = self.uor_api.pattern_analyzer.analyze_execution_patterns(
                        self.uor_api.prime_vm.execution_history
                    )
                    pattern_analysis["execution_patterns"] = patterns
            
            # Get introspection results
            if hasattr(self.uor_api, 'introspection_engine'):
                introspection_results = self.uor_api.introspection_engine.introspect()
                pattern_analysis["introspection_results"] = introspection_results
            
            return json.dumps(pattern_analysis, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting pattern analysis: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving pattern analysis: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_health_trends(self) -> str:
        """Get system health trends as JSON"""
        try:
            health_trends = {
                "timestamp": datetime.now().isoformat()
            }
            
            # Get health trends from health monitor
            if hasattr(self.uor_api, 'health_monitor'):
                trends = self.uor_api.health_monitor.get_health_trends()
                health_trends["trends"] = trends
                
                # Get current health report
                current_health = self.uor_api.health_monitor.check_system_health()
                health_trends["current_health"] = {
                    "overall_healthy": current_health.overall_healthy,
                    "timestamp": current_health.timestamp.isoformat(),
                    "component_count": len(current_health.components),
                    "components": {name: {
                        "healthy": health.healthy,
                        "issues_count": len(health.issues),
                        "last_check": health.last_check.isoformat()
                    } for name, health in current_health.components.items()}
                }
            
            return json.dumps(health_trends, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting health trends: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving health trends: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_cosmic_problems(self) -> str:
        """Get cosmic problems database as JSON"""
        try:
            cosmic_problems = {
                "timestamp": datetime.now().isoformat(),
                "cosmic_state": self.uor_api.system_state.cosmic_state
            }
            
            # Get cosmic intelligence data
            if hasattr(self.uor_api, 'cosmic_intelligence'):
                # Try to get recent cosmic problems
                try:
                    cosmic_result = self.uor_api.cosmic_intelligence.synthesize_cosmic_problems()
                    if hasattr(cosmic_result, 'data') and cosmic_result.data:
                        cosmic_problems["recent_problems"] = cosmic_result.data
                except Exception:
                    cosmic_problems["recent_problems"] = "No recent cosmic problems available"
            
            return json.dumps(cosmic_problems, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting cosmic problems: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving cosmic problems: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
    
    async def get_mathematical_insights(self) -> str:
        """Get mathematical consciousness insights as JSON"""
        try:
            mathematical_insights = {
                "timestamp": datetime.now().isoformat(),
                "mathematical_state": self.uor_api.system_state.mathematical_state
            }
            
            # Get mathematical consciousness data
            if hasattr(self.uor_api, 'mathematical_consciousness'):
                # Try to get mathematical insights
                try:
                    math_result = self.uor_api.mathematical_consciousness.explore_mathematical_truths("", "intuitive")
                    if isinstance(math_result, dict) and math_result.get('success'):
                        mathematical_insights["recent_insights"] = math_result
                except Exception:
                    mathematical_insights["recent_insights"] = "No recent mathematical insights available"
            
            return json.dumps(mathematical_insights, indent=2)
            
        except Exception as e:
            logger.error(f"Error getting mathematical insights: {str(e)}")
            return json.dumps({
                "error": f"Error retrieving mathematical insights: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
