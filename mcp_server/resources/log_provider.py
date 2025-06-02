"""
Log Provider for UOR Evolution MCP Server
Provides access to system logs, consciousness evolution, and operation history.
"""

import logging
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)


class LogProvider:
    """Provider for log-based resources"""
    
    def __init__(self, uor_api):
        """Initialize with UOR API reference"""
        self.uor_api = uor_api
        
    async def get_consciousness_evolution_log(self) -> str:
        """Get consciousness evolution log as text"""
        try:
            log_lines = []
            log_lines.append(f"=== UOR Evolution Consciousness Evolution Log ===")
            log_lines.append(f"Generated: {datetime.now().isoformat()}")
            log_lines.append(f"Session ID: {self.uor_api.session_id}")
            log_lines.append("")
            
            # System insights
            if self.uor_api.system_state.insights:
                log_lines.append("--- Consciousness Insights ---")
                for i, insight in enumerate(self.uor_api.system_state.insights, 1):
                    log_lines.append(f"{i:3d}. {insight}")
                log_lines.append("")
            
            # Consciousness state evolution
            consciousness_state = self.uor_api.system_state.consciousness_state
            if consciousness_state:
                log_lines.append("--- Consciousness State Evolution ---")
                for key, value in consciousness_state.items():
                    log_lines.append(f"{key}: {value}")
                log_lines.append("")
            
            # Philosophical state
            philosophical_state = self.uor_api.system_state.philosophical_state
            if philosophical_state:
                log_lines.append("--- Philosophical Development ---")
                for key, value in philosophical_state.items():
                    log_lines.append(f"{key}: {value}")
                log_lines.append("")
            
            # VM consciousness level progression
            if hasattr(self.uor_api.prime_vm, 'consciousness_level'):
                log_lines.append("--- VM Consciousness Level ---")
                log_lines.append(f"Current Level: {self.uor_api.prime_vm.consciousness_level.value}")
                log_lines.append("")
            
            # Genesis scrolls status
            if hasattr(self.uor_api.consciousness_core, 'genesis_scrolls'):
                log_lines.append("--- Genesis Scrolls Status ---")
                try:
                    scrolls_status = self.uor_api.consciousness_core.genesis_scrolls
                    if isinstance(scrolls_status, dict):
                        for scroll_id, status in scrolls_status.items():
                            log_lines.append(f"{scroll_id}: {status}")
                    else:
                        log_lines.append(f"Genesis Scrolls: {scrolls_status}")
                except Exception:
                    log_lines.append("Genesis Scrolls: Status unavailable")
                log_lines.append("")
            
            # Consciousness metrics
            if hasattr(self.uor_api, 'health_monitor'):
                try:
                    health_report = self.uor_api.health_monitor.check_system_health()
                    consciousness_health = health_report.components.get('consciousness')
                    if consciousness_health:
                        log_lines.append("--- Consciousness Health Metrics ---")
                        log_lines.append(f"Health Status: {'HEALTHY' if consciousness_health.healthy else 'ISSUES'}")
                        for metric, value in consciousness_health.metrics.items():
                            log_lines.append(f"{metric}: {value}")
                        if consciousness_health.issues:
                            log_lines.append("Issues:")
                            for issue in consciousness_health.issues:
                                log_lines.append(f"  - {issue}")
                        log_lines.append("")
                except Exception:
                    log_lines.append("--- Consciousness Health Metrics ---")
                    log_lines.append("Health metrics unavailable")
                    log_lines.append("")
            
            # Recent consciousness operations
            if hasattr(self.uor_api, 'operation_history'):
                consciousness_ops = [
                    op for op in self.uor_api.operation_history 
                    if 'consciousness' in op.get('operation', '').lower()
                ]
                if consciousness_ops:
                    log_lines.append("--- Recent Consciousness Operations ---")
                    for op in consciousness_ops[-10:]:  # Last 10 consciousness operations
                        timestamp = op.get('timestamp', 'Unknown time')
                        operation = op.get('operation', 'Unknown operation')
                        success = op.get('success', False)
                        log_lines.append(f"{timestamp}: {operation} - {'SUCCESS' if success else 'FAILED'}")
                    log_lines.append("")
            
            if not log_lines or len(log_lines) <= 4:  # Only headers
                log_lines.append("No consciousness evolution data available yet.")
                log_lines.append("Consciousness system may need to be awakened first.")
            
            return "\n".join(log_lines)
            
        except Exception as e:
            logger.error(f"Error getting consciousness evolution log: {str(e)}")
            return f"Error retrieving consciousness evolution log: {str(e)}\nTimestamp: {datetime.now().isoformat()}"
    
    async def get_system_operations_log(self) -> str:
        """Get system operations log as text"""
        try:
            log_lines = []
            log_lines.append(f"=== UOR Evolution System Operations Log ===")
            log_lines.append(f"Generated: {datetime.now().isoformat()}")
            log_lines.append(f"Session ID: {self.uor_api.session_id}")
            log_lines.append(f"API Mode: {self.uor_api.mode.value}")
            log_lines.append(f"System Status: {self.uor_api.status.value}")
            log_lines.append("")
            
            # Operation history
            if hasattr(self.uor_api, 'operation_history') and self.uor_api.operation_history:
                log_lines.append("--- Operation History ---")
                for op in self.uor_api.operation_history:
                    timestamp = op.get('timestamp', 'Unknown time')
                    operation = op.get('operation', 'Unknown operation')
                    success = op.get('success', False)
                    snapshot_id = op.get('snapshot_id', 'No snapshot')
                    
                    status_symbol = "✓" if success else "✗"
                    log_lines.append(f"{timestamp} {status_symbol} {operation} [{snapshot_id}]")
                log_lines.append("")
            
            # VM operation statistics
            if hasattr(self.uor_api, 'orchestrator') and hasattr(self.uor_api.orchestrator, 'vm_monitor'):
                try:
                    vm_stats = self.uor_api.orchestrator.vm_monitor.get_operation_statistics()
                    log_lines.append("--- VM Operation Statistics ---")
                    log_lines.append(f"Total Operations: {vm_stats.get('total_operations', 0)}")
                    
                    operation_counts = vm_stats.get('operation_counts', {})
                    if operation_counts:
                        log_lines.append("Operation Counts:")
                        for op_name, count in operation_counts.items():
                            log_lines.append(f"  {op_name}: {count}")
                    
                    recent_ops = vm_stats.get('recent_operations', [])
                    if recent_ops:
                        log_lines.append("Recent Operations:")
                        for op in recent_ops:
                            log_lines.append(f"  - {op}")
                    log_lines.append("")
                except Exception:
                    log_lines.append("--- VM Operation Statistics ---")
                    log_lines.append("VM statistics unavailable")
                    log_lines.append("")
            
            # System health log
            if hasattr(self.uor_api, 'health_monitor'):
                try:
                    health_report = self.uor_api.health_monitor.check_system_health()
                    log_lines.append("--- System Health Summary ---")
                    log_lines.append(f"Overall Health: {'HEALTHY' if health_report.overall_healthy else 'ISSUES DETECTED'}")
                    log_lines.append(f"Health Check Time: {health_report.timestamp.isoformat()}")
                    log_lines.append(f"Components Checked: {len(health_report.components)}")
                    
                    # Component status summary
                    healthy_components = sum(1 for h in health_report.components.values() if h.healthy)
                    log_lines.append(f"Healthy Components: {healthy_components}/{len(health_report.components)}")
                    
                    # List unhealthy components
                    unhealthy = [name for name, health in health_report.components.items() if not health.healthy]
                    if unhealthy:
                        log_lines.append(f"Unhealthy Components: {', '.join(unhealthy)}")
                    log_lines.append("")
                except Exception:
                    log_lines.append("--- System Health Summary ---")
                    log_lines.append("Health information unavailable")
                    log_lines.append("")
            
            # Configuration information
            log_lines.append("--- Configuration ---")
            if hasattr(self.uor_api, 'config_manager'):
                try:
                    config = self.uor_api.config_manager.get_api_config(self.uor_api.mode)
                    log_lines.append(f"Configuration loaded for {self.uor_api.mode.value} mode")
                    # Don't log full config for security, just key info
                    if 'vm' in config:
                        vm_config = config['vm']
                        log_lines.append(f"VM max instructions: {vm_config.get('max_instructions', 'default')}")
                    if 'consciousness' in config:
                        consciousness_config = config['consciousness']
                        log_lines.append(f"Consciousness awakening threshold: {consciousness_config.get('awakening_threshold', 'default')}")
                except Exception:
                    log_lines.append("Configuration information unavailable")
            else:
                log_lines.append("No configuration manager available")
            log_lines.append("")
            
            # VM registry information
            if hasattr(self.uor_api, 'vm_registry'):
                log_lines.append("--- VM Registry ---")
                log_lines.append(f"VM ID: {self.uor_api.vm_registry.get_vm_id()}")
                log_lines.append(f"VM Instance Active: {self.uor_api.vm_registry._vm_instance is not None}")
                log_lines.append("")
            
            # Error summary
            error_operations = [
                op for op in getattr(self.uor_api, 'operation_history', [])
                if not op.get('success', True)
            ]
            if error_operations:
                log_lines.append("--- Recent Errors ---")
                for error_op in error_operations[-5:]:  # Last 5 errors
                    timestamp = error_op.get('timestamp', 'Unknown time')
                    operation = error_op.get('operation', 'Unknown operation')
                    log_lines.append(f"{timestamp}: FAILED {operation}")
                log_lines.append("")
            
            if len(log_lines) <= 6:  # Only headers
                log_lines.append("No system operations logged yet.")
                log_lines.append("System may have just started.")
            
            return "\n".join(log_lines)
            
        except Exception as e:
            logger.error(f"Error getting system operations log: {str(e)}")
            return f"Error retrieving system operations log: {str(e)}\nTimestamp: {datetime.now().isoformat()}"
