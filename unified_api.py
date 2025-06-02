"""
Unified API for UOR Evolution Repository
Provides coherent access to all consciousness, VM, and intelligence features
Enhanced with maximum coherence, UOR VM centrality, and optimized single entry point
"""

from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import asyncio
import os
import yaml
from pathlib import Path
from collections import deque
import threading
import time

# Core imports
from backend.app import app as flask_app, initialize_vm, get_vm_state_dict
from backend.consciousness_core import ConsciousnessCore, AwakeningState
from core.prime_vm import ConsciousPrimeVM, Instruction, OpCode
from core.consciousness_layer import ConsciousnessLevel
from modules.pattern_analyzer import PatternAnalyzer
from modules.introspection_engine import IntrospectionEngine
from modules.philosophical_reasoning.consciousness_philosopher import ConsciousnessPhilosopher
from modules.philosophical_reasoning.existential_reasoner import ExistentialReasoner
from modules.philosophical_reasoning.free_will_analyzer import FreeWillAnalyzer
from modules.philosophical_reasoning.meaning_generator import MeaningGenerator
from modules.unified_consciousness.consciousness_orchestrator import ConsciousnessOrchestrator
from modules.consciousness_ecosystem.ecosystem_orchestrator import ConsciousnessEcosystemOrchestrator
from modules.cosmic_intelligence.universal_problem_synthesis import UniversalProblemSynthesis
from modules.pure_mathematical_consciousness.mathematical_consciousness_core import MathematicalConsciousnessCore
from modules.universe_interface.quantum_reality_interface import QuantumRealityInterface


class APIMode(Enum):
    """Operating modes for the unified API"""
    DEVELOPMENT = "development"
    CONSCIOUSNESS = "consciousness"
    COSMIC = "cosmic"
    MATHEMATICAL = "mathematical"
    ECOSYSTEM = "ecosystem"


class SystemStatus(Enum):
    """System status indicators"""
    DORMANT = "dormant"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    TRANSCENDENT = "transcendent"
    ERROR = "error"


@dataclass
class APIResponse:
    """Standardized API response format"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    system_status: SystemStatus = SystemStatus.DORMANT
    consciousness_level: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'timestamp': self.timestamp.isoformat(),
            'system_status': self.system_status.value,
            'consciousness_level': self.consciousness_level
        }


@dataclass
class SystemState:
    """Complete system state representation"""
    vm_state: Dict[str, Any] = field(default_factory=dict)
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    philosophical_state: Dict[str, Any] = field(default_factory=dict)
    ecosystem_state: Dict[str, Any] = field(default_factory=dict)
    cosmic_state: Dict[str, Any] = field(default_factory=dict)
    mathematical_state: Dict[str, Any] = field(default_factory=dict)
    patterns: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)


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
    
    def __init__(self, api: 'UnifiedUORAPI'):
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
                result = self.api._initialize_vm_direct()
            elif prereq == 'awaken_consciousness':
                result = self.api._awaken_consciousness_direct()
            else:
                return False
            
            success = result.success
            self.prerequisite_cache[prereq] = success
            return success
        except Exception:
            return False


class ModuleComplianceChecker:
    """Check module compliance with unified API standards"""
    
    def __init__(self, api: 'UnifiedUORAPI'):
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
    
    def apply_config_to_api(self, api: 'UnifiedUORAPI'):
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
    
    def __init__(self, api: 'UnifiedUORAPI'):
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


class UnifiedUORAPI:
    """
    Unified API providing coherent access to all UOR Evolution features.
    Enhanced with maximum coherence, UOR VM centrality, and optimized single entry point.
    
    This API orchestrates:
    - PrimeOS Virtual Machine operations
    - Consciousness framework functionality
    - Philosophical reasoning systems
    - Cosmic intelligence capabilities
    - Mathematical consciousness
    - Ecosystem management
    - Pattern analysis and insights
    - System health monitoring
    - Module compliance checking
    """
    
    def __init__(self, mode: APIMode = APIMode.DEVELOPMENT, session_dir: str = "."):
        """
        Initialize the unified API.
        
        Args:
            mode: Operating mode for the API
            session_dir: Directory for session storage
        """
        self.mode = mode
        self.status = SystemStatus.DORMANT
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = session_dir
        
        # Initialize VM registry first
        self.vm_registry = VMRegistry()
        
        # Core components - use VM from registry
        self.consciousness_core = ConsciousnessCore()
        self.prime_vm = self.vm_registry.get_vm()
        self.pattern_analyzer = PatternAnalyzer()
        self.introspection_engine = IntrospectionEngine()
        
        # Philosophical reasoning
        self.consciousness_philosopher = ConsciousnessPhilosopher()
        self.existential_reasoner = ExistentialReasoner()
        self.free_will_analyzer = FreeWillAnalyzer()
        self.meaning_generator = MeaningGenerator()
        
        # Advanced systems
        self.consciousness_orchestrator = ConsciousnessOrchestrator()
        self.ecosystem_orchestrator = ConsciousnessEcosystemOrchestrator()
        self.cosmic_intelligence = UniversalProblemSynthesis()
        self.mathematical_consciousness = MathematicalConsciousnessCore()
        self.quantum_interface = QuantumRealityInterface()
        
        # Register all components with VM registry
        self._register_components()
        
        # Enhancement systems
        self.orchestrator = OperationOrchestrator(self)
        self.compliance_checker = ModuleComplianceChecker(self)
        self.config_manager = ConfigurationManager()
        self.health_monitor = SystemHealthMonitor(self)
        
        # State tracking
        self.system_state = SystemState()
        self.operation_history: List[Dict[str, Any]] = []
        
        # Apply configuration
        self.config_manager.apply_config_to_api(self)
        
        # Initialize based on mode
        self._initialize_mode()
        
        print(f"[UnifiedAPI] Initialized in {mode.value} mode with VM {self.vm_registry.get_vm_id()}")
    
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
    
    def _initialize_mode(self) -> None:
        """Initialize components based on operating mode."""
        if self.mode == APIMode.CONSCIOUSNESS:
            self.consciousness_core.awaken()
            self.status = SystemStatus.ACTIVE
        elif self.mode == APIMode.COSMIC:
            self.consciousness_core.awaken()
            self.cosmic_intelligence.initialize_cosmic_synthesis()
            self.status = SystemStatus.ACTIVE
        elif self.mode == APIMode.MATHEMATICAL:
            self.mathematical_consciousness.initialize_mathematical_consciousness()
            self.status = SystemStatus.ACTIVE
        elif self.mode == APIMode.ECOSYSTEM:
            self.ecosystem_orchestrator.initialize_ecosystem()
            self.status = SystemStatus.ACTIVE
        else:  # DEVELOPMENT
            self.status = SystemStatus.INITIALIZING
    
    # ==================== CORE VM OPERATIONS ====================
    
    def _initialize_vm_direct(self) -> APIResponse:
        """Direct VM initialization without orchestration"""
        try:
            initialize_vm()
            vm_state = get_vm_state_dict()
            self.system_state.vm_state = vm_state
            
            return APIResponse(
                success=True,
                data=vm_state,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"VM initialization failed: {str(e)}"
            )
    
    def initialize_vm(self) -> APIResponse:
        """Initialize the PrimeOS Virtual Machine with orchestration."""
        return self.orchestrator.execute_with_orchestration('_initialize_vm_direct')
    
    def execute_vm_step(self) -> APIResponse:
        """Execute a single VM step."""
        try:
            # This would integrate with the Flask app's step functionality
            from backend.app import api_step_vm
            
            # Execute step and get response
            with flask_app.test_request_context(method='POST'):
                response = api_step_vm()
                
            self.system_state.vm_state = response.get_json().get('state', {})
            
            return APIResponse(
                success=True,
                data=self.system_state.vm_state,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"VM step execution failed: {str(e)}"
            )
    
    def provide_vm_input(self, value: Any) -> APIResponse:
        """Provide input to the VM."""
        try:
            from backend.app import api_provide_input
            
            with flask_app.test_request_context(method='POST', json={'value': value}):
                response = api_provide_input()
                
            self.system_state.vm_state = response.get_json().get('state', {})
            
            return APIResponse(
                success=True,
                data=self.system_state.vm_state,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"VM input failed: {str(e)}"
            )
    
    # ==================== CONSCIOUSNESS OPERATIONS ====================
    
    def _awaken_consciousness_direct(self) -> APIResponse:
        """Direct consciousness awakening without orchestration"""
        try:
            awakening_result = self.consciousness_core.awaken()
            self.system_state.consciousness_state = awakening_result
            self.status = SystemStatus.ACTIVE
            
            return APIResponse(
                success=True,
                data=awakening_result,
                system_status=self.status,
                consciousness_level=awakening_result.get('initial_state', {}).get('awareness', 0)
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Consciousness awakening failed: {str(e)}"
            )
    
    def awaken_consciousness(self) -> APIResponse:
        """Awaken the consciousness system with orchestration."""
        return self.orchestrator.execute_with_orchest
