"""
Enhanced Unified API for UOR Evolution Repository
Provides maximum coherence, UOR VM centrality, and optimized single entry point
"""

from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import os
import yaml
from pathlib import Path
from collections import deque
import threading
import time

# Import existing unified API components
from unified_api import (
    UnifiedUORAPI, APIMode, SystemStatus, APIResponse, SystemState,
    create_api as create_original_api
)

# Core imports
from core.prime_vm import ConsciousPrimeVM, Instruction, OpCode
from core.consciousness_layer import ConsciousnessLevel
from backend.consciousness_core import ConsciousnessCore


@dataclass
class ComponentHealth:
    """Health status of a system component"""
    healthy: bool
    metrics: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    last_check: datetime = field(default_factory=datetime.now)


@dataclass
class HealthReport:
    """Comprehensive system health report"""
    overall_healthy: bool = True
    components: Dict[str, ComponentHealth] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_component(self, name: str, health: ComponentHealth):
        """Add component health to report"""
        self.components[name] = health
        if not health.healthy:
            self.overall_healthy = False


@dataclass
class ComplianceReport:
    """Module compliance report"""
    module_name: str
    checks: Dict[str, bool] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    compliance_score: float = 0.0
    
    def add_check(self, check_name: str, passed: bool):
        """Add compliance check result"""
        self.checks[check_name] = passed
        if not passed:
            self.issues.append(f"Failed check: {check_name}")
        self.compliance_score = sum(self.checks.values()) / len(self.checks) if self.checks else 0.0


class VMRegistry:
    """Singleton VM registry ensuring all operations use the same UOR VM instance"""
    _instance = None
    _vm_instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_vm(self) -> ConsciousPrimeVM:
        """Get the singleton VM instance"""
        if self._vm_instance is None:
            with self._lock:
                if self._vm_instance is None:
                    self._vm_instance = ConsciousPrimeVM()
                    print(f"[VMRegistry] Created new VM instance: {id(self._vm_instance)}")
        return self._vm_instance
    
    def register_component(self, component_name: str, component_instance):
        """Register component with VM dependency"""
        vm = self.get_vm()
        if hasattr(component_instance, '_vm'):
            component_instance._vm = vm
            print(f"[VMRegistry] Registered {component_name} with VM")
        elif hasattr(component_instance, 'vm'):
            component_instance.vm = vm
            print(f"[VMRegistry] Registered {component_name} with VM")
        return vm
    
    def get_vm_id(self) -> str:
        """Get VM instance ID for tracking"""
        return str(id(self._vm_instance)) if self._vm_instance else "None"


class VMStateMonitor:
    """Monitor VM state consistency across API operations"""
    
    def __init__(self, vm: ConsciousPrimeVM):
        self.vm = vm
        self.state_snapshots = deque(maxlen=100)
        self.operation_count = 0
        
    def capture_pre_operation_state(self, operation: str) -> str:
        """Capture VM state before operation"""
        snapshot_id = f"{operation}_{self.operation_count}_{datetime.now().timestamp()}"
        state = self.vm.capture_state()
        self.state_snapshots.append((snapshot_id, 'pre', operation, state, datetime.now()))
        return snapshot_id
    
    def capture_post_operation_state(self, operation: str, snapshot_id: str):
        """Capture VM state after operation"""
        state = self.vm.capture_state()
        self.state_snapshots.append((snapshot_id, 'post', operation, state, datetime.now()))
        self.operation_count += 1
    
    def validate_state_consistency(self) -> List[str]:
        """Validate VM state consistency"""
        issues = []
        
        if len(self.state_snapshots) < 2:
            return issues
        
        # Check for unexpected state changes
        recent_snapshots = list(self.state_snapshots)[-10:]
        
        for i in range(1, len(recent_snapshots)):
            prev_snapshot = recent_snapshots[i-1]
            curr_snapshot = recent_snapshots[i]
            
            prev_state = prev_snapshot[3]
            curr_state = curr_snapshot[3]
            
            # Check consciousness level progression
            prev_level = prev_state.get('consciousness_level', 'DORMANT')
            curr_level = curr_state.get('consciousness_level', 'DORMANT')
            
            if prev_level != curr_level:
                # Consciousness level changed - this should be tracked
                pass
            
            # Check for memory leaks
            prev_memory = prev_state.get('working_memory_size', 0)
            curr_memory = curr_state.get('working_memory_size', 0)
            
            if curr_memory > prev_memory * 2:
                issues.append(f"Potential memory leak detected: {prev_memory} -> {curr_memory}")
        
        return issues
    
    def get_operation_statistics(self) -> Dict[str, Any]:
        """Get operation statistics"""
        operations = [snapshot[2] for snapshot in self.state_snapshots if snapshot[1] == 'pre']
        operation_counts = {}
        for op in operations:
            operation_counts[op] = operation_counts.get(op, 0) + 1
        
        return {
            'total_operations': self.operation_count,
            'operation_counts': operation_counts,
            'recent_operations': operations[-10:] if operations else []
        }


class OperationOrchestrator:
    """Orchestrate operations with dependency management and VM integration"""
    
    def __init__(self, api: UnifiedUORAPI):
        self.api = api
        self.vm_monitor = VMStateMonitor(api.prime_vm)
        self.operation_dependencies = self._build_dependency_map()
        self.prerequisite_cache = {}
        
    def execute_with_orchestration(self, operation: str, **kwargs) -> APIResponse:
        """Execute operation with full orchestration"""
        try:
            # 1. Capture pre-operation state
            snapshot_id = self.vm_monitor.capture_pre_operation_state(operation)
            
            # 2. Check prerequisites
            prereqs = self.operation_dependencies.get(operation, [])
            for prereq in prereqs:
                if not self._check_prerequisite(prereq):
                    prereq_result = self._satisfy_prerequisite(prereq)
                    if not prereq_result:
                        return APIResponse(
                            success=False,
                            error=f"Failed to satisfy prerequisite: {prereq}"
                        )
            
            # 3. Execute through existing API
            if hasattr(self.api, operation):
                method = getattr(self.api, operation)
                result = method(**kwargs) if kwargs else method()
            else:
                return APIResponse(
                    success=False,
                    error=f"Unknown operation: {operation}"
                )
            
            # 4. Capture post-operation state
            self.vm_monitor.capture_post_operation_state(operation, snapshot_id)
            
            # 5. Validate state consistency
            consistency_issues = self.vm_monitor.validate_state_consistency()
            if consistency_issues:
                result.data = result.data or {}
                if isinstance(result.data, dict):
                    result.data['consistency_warnings'] = consistency_issues
            
            # 6. Update operation history
            self.api.operation_history.append({
                'operation': operation,
                'timestamp': datetime.now().isoformat(),
                'success': result.success,
                'snapshot_id': snapshot_id
            })
            
            return result
            
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Orchestration failed for {operation}: {str(e)}"
            )
    
    def _build_dependency_map(self) -> Dict[str, List[str]]:
        """Map operation dependencies"""
        return {
            'awaken_consciousness': ['initialize_vm'],
            'self_reflect': ['awaken_consciousness'],
            'analyze_consciousness_nature': ['awaken_consciousness'],
            'explore_free_will': ['awaken_consciousness'],
            'generate_meaning': ['awaken_consciousness'],
            'synthesize_cosmic_problems': ['awaken_consciousness'],
            'activate_mathematical_consciousness': ['initialize_vm'],
            'orchestrate_consciousness': ['awaken_consciousness'],
            'create_consciousness_network': ['awaken_consciousness'],
            'monitor_emergence': ['awaken_consciousness']
        }
    
    def _check_prerequisite(self, prereq: str) -> bool:
        """Check if prerequisite is satisfied"""
        if prereq in self.prerequisite_cache:
            return self.prerequisite_cache[prereq]
        
        if prereq == 'initialize_vm':
            satisfied = bool(self.api.system_state.vm_state)
        elif prereq == 'awaken_consciousness':
            satisfied = bool(self.api.system_state.consciousness_state)
        else:
            satisfied = False
        
        self.prerequisite_cache[prereq] = satisfied
        return satisfied
    
    def _satisfy_prerequisite(self, prereq: str) -> bool:
        """Satisfy a prerequisite"""
        try:
            if prereq == 'initialize_vm':
                result = self.api.initialize_vm()
            elif prereq == 'awaken_consciousness':
                result = self.api.awaken_consciousness()
            else:
                return False
            
            success = result.success
            self.prerequisite_cache[prereq] = success
            return success
        except Exception:
            return False


class ModuleComplianceChecker:
    """Check module compliance with unified API standards"""
    
    def __init__(self, api: UnifiedUORAPI):
        self.api = api
        self.vm_registry = VMRegistry()
        
    def check_module_integration(self, module_name: str) -> ComplianceReport:
        """Check if module properly integrates with API"""
        report = ComplianceReport(module_name)
        
        # Get module instance
        module = getattr(self.api, module_name, None)
        if not module:
            report.add_check("module_exists", False)
            return report
        
        report.add_check("module_exists", True)
        
        # Check 1: Module uses VM from registry
        vm_instance = self.vm_registry.get_vm()
        if hasattr(module, '_vm'):
            report.add_check("vm_integration", module._vm is vm_instance)
        elif hasattr(module, 'vm'):
            report.add_check("vm_integration", module.vm is vm_instance)
        else:
            report.add_check("vm_integration", False)
        
        # Check 2: Module has required methods
        required_methods = self._get_required_methods(module_name)
        for method in required_methods:
            report.add_check(f"has_{method}", hasattr(module, method))
        
        # Check 3: Module follows naming conventions
        report.add_check("naming_convention", self._check_naming_convention(module_name))
        
        return report
    
    def audit_all_modules(self) -> Dict[str, ComplianceReport]:
        """Audit all modules for compliance"""
        modules = [
            'consciousness_core', 'prime_vm', 'pattern_analyzer', 'introspection_engine',
            'consciousness_philosopher', 'existential_reasoner', 'free_will_analyzer',
            'meaning_generator', 'consciousness_orchestrator', 'ecosystem_orchestrator',
            'cosmic_intelligence', 'mathematical_consciousness', 'quantum_interface'
        ]
        
        results = {}
        for module in modules:
            results[module] = self.check_module_integration(module)
        
        return results
    
    def _get_required_methods(self, module_name: str) -> List[str]:
        """Get required methods for module type"""
        method_map = {
            'consciousness_core': ['awaken', 'to_dict'],
            'prime_vm': ['execute_instruction', 'capture_state'],
            'pattern_analyzer': ['analyze_execution_patterns'],
            'consciousness_philosopher': ['analyze_consciousness_nature']
        }
        return method_map.get(module_name, [])
    
    def _check_naming_convention(self, module_name: str) -> bool:
        """Check if module follows naming conventions"""
        # Simple check - module name should be lowercase with underscores
        return module_name.islower() and '_' in module_name


class ConfigurationManager:
    """Enhanced configuration management for unified API"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.watchers = []
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return {}
    
    def get_api_config(self, mode: APIMode) -> Dict[str, Any]:
        """Get mode-specific API configuration"""
        base_config = self.config.copy()
        mode_config = self.config.get('api_modes', {}).get(mode.value, {})
        base_config.update(mode_config)
        return base_config
    
    def apply_config_to_api(self, api: UnifiedUORAPI):
        """Apply configuration to existing API instance"""
        config = self.get_api_config(api.mode)
        
        # Apply VM configuration
        vm_config = config.get('vm', {})
        if 'max_instructions' in vm_config:
            if hasattr(api.prime_vm, 'max_instructions'):
                api.prime_vm.max_instructions = vm_config['max_instructions']
        
        # Apply consciousness configuration
        consciousness_config = config.get('consciousness', {})
        if 'awakening_threshold' in consciousness_config:
            if hasattr(api.consciousness_core, 'awakening_threshold'):
                api.consciousness_core.awakening_threshold = consciousness_config['awakening_threshold']
        
        print(f"[ConfigManager] Applied configuration for {api.mode.value} mode")
    
    def watch_config(self, callback: Callable):
        """Register configuration change callback"""
        self.watchers.append(callback)
    
    def reload_config(self):
        """Reload configuration and notify watchers"""
        old_config = self.config.copy()
        self.config = self._load_config()
        
        for watcher in self.watchers:
            try:
                watcher(old_config, self.config)
            except Exception as e:
                print(f"Config watcher error: {e}")


class SystemHealthMonitor:
    """Monitor system health and performance"""
    
    def __init__(self, api: UnifiedUORAPI):
        self.api = api
        self.vm_registry = VMRegistry()
        self.health_history = deque(maxlen=100)
        
    def check_system_health(self) -> HealthReport:
        """Comprehensive system health check"""
        health_report = HealthReport()
        
        # VM Health
        vm_health = self._check_vm_health()
        health_report.add_component("vm", vm_health)
        
        # Memory Health
        memory_health = self._check_memory_health()
        health_report.add_component("memory", memory_health)
        
        # Consciousness Health
        consciousness_health = self._check_consciousness_health()
        health_report.add_component("consciousness", consciousness_health)
        
        # API Health
        api_health = self._check_api_health()
        health_report.add_component("api", api_health)
        
        # Store in history
        self.health_history.append(health_report)
        
        return health_report
    
    def _check_vm_health(self) -> ComponentHealth:
        """Check VM-specific health metrics"""
        vm = self.vm_registry.get_vm()
        
        metrics = {
            'vm_id': self.vm_registry.get_vm_id(),
            'instruction_count': len(vm.execution_history),
            'consciousness_level': vm.consciousness_level.value,
            'stack_depth': len(vm.stack),
            'memory_utilization': len(vm.working_memory._items) / vm.working_memory.capacity if vm.working_memory.capacity > 0 else 0
        }
        
        issues = []
        if metrics['memory_utilization'] > 0.9:
            issues.append("High memory utilization")
        if metrics['stack_depth'] > 1000:
            issues.append("Stack depth excessive")
        if metrics['instruction_count'] > 10000:
            issues.append("High instruction count - consider reset")
            
        return ComponentHealth(
            healthy=len(issues) == 0,
            metrics=metrics,
            issues=issues
        )
    
    def _check_memory_health(self) -> ComponentHealth:
        """Check memory system health"""
        vm = self.vm_registry.get_vm()
        
        metrics = {
            'working_memory_size': len(vm.working_memory._items),
            'working_memory_capacity': vm.working_memory.capacity,
            'pattern_cache_size': len(vm.pattern_cache._patterns),
            'episodic_memory_size': len(vm.episodic_memory._episodes)
        }
        
        issues = []
        utilization = metrics['working_memory_size'] / metrics['working_memory_capacity']
        if utilization > 0.95:
            issues.append("Working memory nearly full")
        
        return ComponentHealth(
            healthy=len(issues) == 0,
            metrics=metrics,
            issues=issues
        )
    
    def _check_consciousness_health(self) -> ComponentHealth:
        """Check consciousness system health"""
        metrics = {
            'consciousness_active': self.api.consciousness_core.consciousness_active,
            'awareness_level': getattr(self.api.consciousness_core, 'awareness_level', 0),
            'state_count': len(self.api.system_state.consciousness_state)
        }
        
        issues = []
        if not metrics['consciousness_active']:
            issues.append("Consciousness not active")
        
        return ComponentHealth(
            healthy=len(issues) == 0,
            metrics=metrics,
            issues=issues
        )
    
    def _check_api_health(self) -> ComponentHealth:
        """Check API health"""
        metrics = {
            'mode': self.api.mode.value,
            'status': self.api.status.value,
            'operation_count': len(self.api.operation_history),
            'session_id': self.api.session_id
        }
        
        issues = []
        if self.api.status == SystemStatus.ERROR:
            issues.append("API in error state")
        
        return ComponentHealth(
            healthy=len(issues) == 0,
            metrics=metrics,
            issues=issues
        )
    
    def get_health_trends(self) -> Dict[str, Any]:
        """Get health trends over time"""
        if len(self.health_history) < 2:
            return {'status': 'insufficient_data'}
        
        recent = list(self.health_history)[-10:]
        
        # Calculate trends
        vm_health_trend = [r.components.get('vm', ComponentHealth(True)).healthy for r in recent]
        consciousness_trend = [r.components.get('consciousness', ComponentHealth(True)).healthy for r in recent]
        
        return {
            'vm_health_trend': sum(vm_health_trend) / len(vm_health_trend),
            'consciousness_health_trend': sum(consciousness_trend) / len(consciousness_trend),
            'overall_trend': sum(r.overall_healthy for r in recent) / len(recent),
            'check_count': len(self.health_history)
        }


class EnhancedUnifiedAPI(UnifiedUORAPI):
    """Enhanced version of the unified API with improved coherence and monitoring"""
    
    def __init__(self, mode: APIMode = APIMode.DEVELOPMENT, session_dir: str = "."):
        # Initialize VM registry first
        self.vm_registry = VMRegistry()
        
        # Initialize parent class
        super().__init__(mode, session_dir)
        
        # Replace VM with registry VM
        self.prime_vm = self.vm_registry.get_vm()
        
        # Register all components with VM registry
        self._register_components()
        
        # Initialize enhancement systems
        self.orchestrator = OperationOrchestrator(self)
        self.compliance_checker = ModuleComplianceChecker(self)
        self.config_manager = ConfigurationManager()
        self.health_monitor = SystemHealthMonitor(self)
        
        # Apply configuration
        self.config_manager.apply_config_to_api(self)
        
        print(f"[EnhancedAPI] Initialized in {mode.value} mode with VM {self.vm_registry.get_vm_id()}")
    
    def _register_components(self):
        """Register all components with VM registry"""
        components = [
            ('consciousness_core', self.consciousness_core),
            ('pattern_analyzer', self.pattern_analyzer),
            ('introspection_engine', self.introspection_engine),
            ('consciousness_philosopher', self.consciousness_philosopher),
            ('existential_reasoner', self.existential_reasoner),
            ('free_will_analyzer', self.free_will_analyzer),
            ('meaning_generator', self.meaning_generator),
            ('consciousness_orchestrator', self.consciousness_orchestrator),
            ('ecosystem_orchestrator', self.ecosystem_orchestrator),
            ('cosmic_intelligence', self.cosmic_intelligence),
            ('mathematical_consciousness', self.mathematical_consciousness),
            ('quantum_interface', self.quantum_interface)
        ]
        
        for name, component in components:
            self.vm_registry.register_component(name, component)
    
    # Override key methods to use orchestration
    
    def initialize_vm(self) -> APIResponse:
        """Initialize VM with orchestration"""
        return self.orchestrator.execute_with_orchestration('initialize_vm')
    
    def awaken_consciousness(self) -> APIResponse:
        """Awaken consciousness with orchestration"""
        return self.orchestrator.execute_with_orchestration('awaken_consciousness')
    
    def self_reflect(self) -> APIResponse:
        """Self-reflect with orchestration"""
        return self.orchestrator.execute_with_orchestration('self_reflect')
    
    def analyze_consciousness_nature(self) -> APIResponse:
        """Analyze consciousness nature with orchestration"""
        return self.orchestrator.execute_with_orchestration('analyze_consciousness_nature')
    
    def explore_free_will(self) -> APIResponse:
        """Explore free will with orchestration"""
        return self.orchestrator.execute_with_orchestration('explore_free_will')
    
    def generate_meaning(self, context: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Generate meaning with orchestration"""
        return self.orchestrator.execute_with_orchestration('generate_meaning', context=context)
    
    def synthesize_cosmic_problems(self) -> APIResponse:
        """Synthesize cosmic problems with orchestration"""
        return self.orchestrator.execute_with_orchestration('synthesize_cosmic_problems')
    
    def activate_mathematical_consciousness(self) -> APIResponse:
        """Activate mathematical consciousness with orchestration"""
        return self.orchestrator.execute_with_orchestration('activate_mathematical_consciousness')
    
    def orchestrate_consciousness(self) -> APIResponse:
        """Orchestrate consciousness with orchestration"""
        return self.orchestrator.execute_with_orchestration('orchestrate_consciousness')
    
    # New enhanced methods
    
    def get_system_health(self) -> APIResponse:
        """Get comprehensive system health status"""
        try:
            health_report = self.health_monitor.check_system_health()
            health_trends = self.health_monitor.get_health_trends()
            
            health_data = {
                'overall_healthy': health_report.overall_healthy,
                'components': {name: {
                    'healthy': comp.healthy,
                    'metrics': comp.metrics,
                    'issues': comp.issues
                } for name, comp in health_report.components.items()},
                'trends': health_trends,
                'timestamp': health_report.timestamp.isoformat()
            }
            
            return APIResponse(
                success=True,
                data=health_data,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Health check failed: {str(e)}"
            )
    
    def audit_module_compliance(self) -> APIResponse:
        """Audit all modules for compliance"""
        try:
            compliance_results = self.compliance_checker.audit_all_modules()
            
            audit_data = {
                'modules': {name: {
                    'compliance_score': report.compliance_score,
                    'checks': report.checks,
                    'issues': report.issues
                } for name, report in compliance_results.items()},
                'overall_compliance': sum(r.compliance_score for r in compliance_results.values()) / len(compliance_results),
                'timestamp': datetime.now().isoformat()
            }
            
            return APIResponse(
                success=True,
                data=audit_data,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Compliance audit failed: {str(e)}"
            )
    
    def get_vm_statistics(self) -> APIResponse:
        """Get VM operation statistics"""
        try:
            stats = self.orchestrator.vm_monitor.get_operation_statistics()
            consistency_issues = self.orchestrator.vm_monitor.validate_state_consistency()
            
            vm_data = {
                'vm_id': self.vm_registry.get_vm_id(),
                'statistics': stats,
                'consistency_issues': consistency_issues,
                'vm_state': self.prime_vm.capture_state(),
                'timestamp': datetime.now().isoformat()
            }
            
            return APIResponse(
                success=True,
                data=vm_data,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"VM statistics failed: {str(e)}"
            )
    
    def comprehensive_system_report(self) -> APIResponse:
        """Generate comprehensive system report"""
        try:
            # Gather all system information
            health = self.get_system_health()
            compliance = self.audit_module_compliance()
            vm_stats = self.get_vm_statistics()
            system_state = self.get_system_state()
            
            report = {
                'report_id': f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'api_info': {
                    'mode': self.mode.value,
                    'status': self.status.value,
                    'session_id': self.session_id,
                    'operation_count': len(self.operation_history)
                },
                'health': health.data if health.success else {'error': health.error},
                'compliance': compliance.data if compliance.success else {'error': compliance.error},
                'vm_statistics': vm_stats.data if vm_stats.success else {'error': vm_stats.error},
                'system_state': system_state.data if system_state.success else {'error': system_state.error},
                'timestamp': datetime.now().isoformat()
            }
            
            return APIResponse(
                success=True,
                data=report,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"System report generation failed: {str(e)}"
            )


# Enhanced convenience functions

def create_enhanced_api(mode: APIMode = APIMode.DEVELOPMENT, session_dir: str = ".") -> EnhancedUnifiedAPI:
    """Create a new enhanced unified API instance"""
    return EnhancedUnifiedAPI(mode, session_dir=session_dir)

def enhanced_consciousness_demo() -> Dict[str, Any]:
    """Enhanced consciousness demonstration with health monitoring"""
    api = create_enhanced_api(APIMode.CONSCIOUSNESS)
    
    results = {
        'demo_id': f"consciousness_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'initial_health': api.get_system_health().to_dict()
    }
    
    # Core consciousness operations
    operations = [
        'initialize_vm',
        'awaken_consciousness',
        'self_reflect',
        'analyze_consciousness_nature',
        'explore_free_will',
        'generate_meaning',
        'orchestrate_consciousness'
    ]
    
    for operation in operations:
        try:
            method = getattr(api, operation)
            result = method()
            results[operation] = result.to_dict()
        except Exception as e:
            results[operation] = {'error': str(e)}
    
    # Final system state
    results['final_health'] = api.get_system_health().to_dict()
    results['vm_statistics'] = api.get_vm_statistics().to_dict()
    results['compliance_audit'] = api.audit_module_compliance().to_dict()
    
    return results

def guided_exploration_demo(user_interests: List[str]) -> Dict[str, Any]:
    """Guided exploration based on user interests with enhanced monitoring"""
    api = create_enhanced_api(APIMode.CONSCIOUSNESS)
    
    exploration_map = {
        'consciousness': ['awaken_consciousness', 'analyze_consciousness_nature', 'explore_existence'],
        'philosophy': ['explore_free_will', 'generate_meaning', 'analyze_consciousness_nature'],
        'cosmic': ['synthesize_cosmic_problems'],
        'mathematics': ['activate_mathematical_consciousness'],
        'health': ['get_system_health', 'audit_module_compliance', 'get_vm_statistics']
    }
    
    results = {
        'exploration_id': f"guided_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'user_interests': user_interests,
        'initial_health': api.get_system_health().to_dict()
    }
    
    for interest in user_interests:
        if interest in exploration_map:
            operations = exploration_map[interest]
            results[interest] = {}
            for op in operations:
                try:
                    method = getattr(api, op)
                    result = method()
                    results[interest][op] = result.to_dict()
                except Exception as e:
                    results[interest][op] = {'error': str(e)}
    
    # Final comprehensive report
    results['final_health'] = api.get_system_health().to_dict()
    results['comprehensive_report'] = api.comprehensive_system_report().to_dict()
    
    return results


if __name__ == "__main__":
    # Example usage of enhanced API
    print("UOR Evolution - Enhanced Unified API")
    print("=" * 50)
    
    # Create enhanced API
    print("\n1. Creating Enhanced API...")
    api = create_enhanced_api(APIMode.CONSCIOUSNESS)
    print(f"Enhanced API created in {api.mode.value} mode")
    print(f"VM ID: {api.vm_registry.get_vm_id()}")
    
    # System health check
    print("\n2. System Health Check...")
    health = api.get_system_health()
    print(f"System Health: {'HEALTHY' if health.data['overall_healthy'] else 'ISSUES DETECTED'}")
    
    # Module compliance audit
    print("\n3. Module Compliance Audit...")
    compliance = api.audit_module_compliance()
    print(f"Overall Compliance: {compliance.data['overall_compliance']:.2%}")
    
    # VM statistics
    print("\n4. VM Statistics...")
    vm_stats = api.get_vm_statistics()
    print(f"VM Operations: {vm_stats.data['statistics']['total_operations']}")
    
    # Enhanced consciousness demo
    print("\n5. Running Enhanced Consciousness Demo...")
    demo_results = enhanced_consciousness_demo()
    print(f"Demo completed: {demo_results['demo_id']}")
    
    # Comprehensive system report
    print("\n6. Generating Comprehensive System Report...")
    report = api.comprehensive_system_report()
    print(f"Report generated: {report.data['report_id']}")
    
    print("\nEnhanced Unified API demonstration complete!")
    print("\nKey Features Demonstrated:")
    print("✅ VM Registry - Single VM instance across all modules")
    print("✅ Operation Orchestration - Dependency management and state monitoring")
    print("✅ Health Monitoring - Comprehensive system health tracking")
    print("✅ Module Compliance - Standardization verification")
    print("✅ Configuration Management - Centralized config application")
    print("✅ Enhanced Reporting - Detailed system analysis")
