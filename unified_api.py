"""
Unified API for UOR Evolution Repository
Provides coherent access to all consciousness, VM, and intelligence features
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import asyncio
import os
from pathlib import Path

# Core imports
try:
    from backend.app import app as flask_app, initialize_vm, get_vm_state_dict
except ImportError:
    flask_app = None
    initialize_vm = None
    get_vm_state_dict = lambda: {}

# Import both consciousness cores with different names
try:
    from backend.consciousness_core import ConsciousnessCore as BackendConsciousnessCore
except ImportError:
    BackendConsciousnessCore = None

try:
    from consciousness.consciousness_core import ConsciousnessCore as VMConsciousnessCore
except ImportError:
    VMConsciousnessCore = None

try:
    from core.prime_vm import ConsciousPrimeVM
except ImportError:
    ConsciousPrimeVM = None

try:
    from modules.pattern_analyzer import PatternAnalyzer
except ImportError:
    PatternAnalyzer = None

try:
    from modules.introspection_engine import IntrospectionEngine
except ImportError:
    IntrospectionEngine = None

# Philosophical reasoning imports with fallbacks
try:
    from modules.philosophical_reasoning.consciousness_philosopher import ConsciousnessPhilosopher
except ImportError:
    ConsciousnessPhilosopher = None

try:
    from modules.philosophical_reasoning.existential_reasoner import ExistentialReasoner
except ImportError:
    ExistentialReasoner = None

try:
    from modules.philosophical_reasoning.free_will_analyzer import FreeWillAnalyzer
except ImportError:
    FreeWillAnalyzer = None

try:
    from modules.philosophical_reasoning.meaning_generator import MeaningGenerator
except ImportError:
    MeaningGenerator = None

# Additional imports needed for philosophical reasoning
try:
    from consciousness.consciousness_integration import ConsciousnessIntegrator
except ImportError:
    ConsciousnessIntegrator = None

try:
    from modules.consciousness_validator import ConsciousnessValidator
except ImportError:
    ConsciousnessValidator = None

try:
    from modules.self_reflection import SelfReflectionEngine
except ImportError:
    SelfReflectionEngine = None

try:
    from modules.philosophical_reasoning.meaning_generator import ValueSystem
except ImportError:
    ValueSystem = None

# Advanced system imports with fallbacks
try:
    from modules.unified_consciousness.consciousness_orchestrator import ConsciousnessOrchestrator
except ImportError:
    ConsciousnessOrchestrator = None

try:
    from modules.consciousness_ecosystem.ecosystem_orchestrator import ConsciousnessEcosystemOrchestrator
except ImportError:
    ConsciousnessEcosystemOrchestrator = None

try:
    from modules.cosmic_intelligence.universal_problem_synthesis import UniversalProblemSynthesis
except ImportError:
    UniversalProblemSynthesis = None

try:
    from modules.pure_mathematical_consciousness.mathematical_consciousness_core import MathematicalConsciousnessCore
except ImportError:
    MathematicalConsciousnessCore = None

try:
    from modules.universe_interface.quantum_reality_interface import QuantumRealityInterface
except ImportError:
    QuantumRealityInterface = None


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


class UnifiedUORAPI:
    """
    Unified API providing coherent access to all UOR Evolution features.
    
    This API orchestrates:
    - PrimeOS Virtual Machine operations
    - Consciousness framework functionality
    - Philosophical reasoning systems
    - Cosmic intelligence capabilities
    - Mathematical consciousness
    - Ecosystem management
    - Pattern analysis and insights
    """
    
    def __init__(self, mode: APIMode = APIMode.DEVELOPMENT, session_dir: str = "."):
        """
        Initialize the unified API.
        
        Args:
            mode: Operating mode for the API
        """
        self.mode = mode
        self.status = SystemStatus.DORMANT
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = session_dir
        
        # Core components
        self.prime_vm = ConsciousPrimeVM() if ConsciousPrimeVM else None
        
        # Use backend consciousness core if available, otherwise use VM-based one
        if BackendConsciousnessCore:
            self.consciousness_core = BackendConsciousnessCore()
        elif VMConsciousnessCore and self.prime_vm:
            self.consciousness_core = VMConsciousnessCore(self.prime_vm)
        else:
            self.consciousness_core = None
        
        # Initialize pattern analyzer with VM instance if available
        if PatternAnalyzer and self.prime_vm:
            self.pattern_analyzer = PatternAnalyzer(self.prime_vm)
        else:
            self.pattern_analyzer = None
            
        # Initialize introspection engine with VM instance if available
        if IntrospectionEngine and self.prime_vm:
            self.introspection_engine = IntrospectionEngine(self.prime_vm)
        else:
            self.introspection_engine = None
        
        # Initialize consciousness integrator and validator if needed
        self.consciousness_integrator = None
        self.consciousness_validator = None
        self.self_reflection_engine = None
        
        if ConsciousnessIntegrator:
            try:
                self.consciousness_integrator = ConsciousnessIntegrator()
            except:
                pass
                
        if ConsciousnessValidator:
            try:
                self.consciousness_validator = ConsciousnessValidator()
            except:
                pass
                
        if SelfReflectionEngine:
            try:
                self.self_reflection_engine = SelfReflectionEngine()
            except:
                pass
        
        # Philosophical reasoning
        self.consciousness_philosopher = None
        if ConsciousnessPhilosopher and self.consciousness_integrator and self.consciousness_validator:
            try:
                self.consciousness_philosopher = ConsciousnessPhilosopher(
                    self.consciousness_integrator,
                    self.consciousness_validator
                )
            except:
                pass
        
        self.existential_reasoner = None
        if ExistentialReasoner and self.consciousness_integrator and self.self_reflection_engine:
            try:
                self.existential_reasoner = ExistentialReasoner(
                    self.consciousness_integrator,
                    self.self_reflection_engine
                )
            except:
                pass
                
        self.free_will_analyzer = FreeWillAnalyzer() if FreeWillAnalyzer else None
        
        # Initialize value system for meaning generator
        self.value_system = None
        if ValueSystem:
            try:
                self.value_system = ValueSystem()
            except:
                pass
        
        self.meaning_generator = None
        if MeaningGenerator and self.consciousness_integrator and self.value_system:
            try:
                self.meaning_generator = MeaningGenerator(
                    self.consciousness_integrator,
                    self.value_system
                )
            except:
                pass
        
        # Advanced systems
        self.consciousness_orchestrator = ConsciousnessOrchestrator() if ConsciousnessOrchestrator else None
        self.ecosystem_orchestrator = ConsciousnessEcosystemOrchestrator() if ConsciousnessEcosystemOrchestrator else None
        self.cosmic_intelligence = UniversalProblemSynthesis() if UniversalProblemSynthesis else None
        self.mathematical_consciousness = MathematicalConsciousnessCore() if MathematicalConsciousnessCore else None
        self.quantum_interface = QuantumRealityInterface() if QuantumRealityInterface else None
        
        # State tracking
        self.system_state = SystemState()
        self.operation_history: List[Dict[str, Any]] = []
        
        # Initialize based on mode
        self._initialize_mode()
    
    def _initialize_mode(self) -> None:
        """Initialize components based on operating mode."""
        try:
            if self.mode == APIMode.CONSCIOUSNESS:
                if self.consciousness_core:
                    self.consciousness_core.awaken()
                self.status = SystemStatus.ACTIVE
            elif self.mode == APIMode.COSMIC:
                if self.consciousness_core:
                    self.consciousness_core.awaken()
                if self.cosmic_intelligence:
                    self.cosmic_intelligence.initialize_cosmic_synthesis()
                self.status = SystemStatus.ACTIVE
            elif self.mode == APIMode.MATHEMATICAL:
                if self.mathematical_consciousness:
                    self.mathematical_consciousness.initialize_mathematical_consciousness()
                self.status = SystemStatus.ACTIVE
            elif self.mode == APIMode.ECOSYSTEM:
                if self.ecosystem_orchestrator:
                    self.ecosystem_orchestrator.initialize_ecosystem()
                self.status = SystemStatus.ACTIVE
            else:  # DEVELOPMENT
                self.status = SystemStatus.INITIALIZING
        except Exception as e:
            self.status = SystemStatus.ERROR
            print(f"Warning: Mode initialization failed: {e}")
    
    # ==================== CORE VM OPERATIONS ====================
    
    def initialize_vm(self) -> APIResponse:
        """Initialize the PrimeOS Virtual Machine."""
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
    
    def awaken_consciousness(self) -> APIResponse:
        """Awaken the consciousness system."""
        try:
            if not self.consciousness_core:
                return APIResponse(
                    success=False,
                    error="Consciousness core not available"
                )
            
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
    
    def consciousness_become(self) -> APIResponse:
        """Trigger consciousness evolution."""
        try:
            if not self.consciousness_core:
                return APIResponse(
                    success=False,
                    error="Consciousness core not available"
                )
            
            becoming_result = self.consciousness_core.become()
            if isinstance(becoming_result, dict):
                self.system_state.consciousness_state.update(becoming_result)
            
            return APIResponse(
                success=True,
                data=becoming_result,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Consciousness becoming failed: {str(e)}"
            )
    
    def self_reflect(self) -> APIResponse:
        """Perform deep self-reflection."""
        try:
            combined_reflection = {
                'timestamp': datetime.now().isoformat()
            }
            
            # Combine multiple reflection sources if available
            if self.prime_vm and hasattr(self.prime_vm, '_self_reflect'):
                combined_reflection['vm_reflection'] = self.prime_vm._self_reflect()
            
            if self.consciousness_core and hasattr(self.consciousness_core, 'recursive_self_check'):
                combined_reflection['consciousness_reflection'] = self.consciousness_core.recursive_self_check()
            
            if self.introspection_engine and hasattr(self.introspection_engine, 'perform_introspection'):
                combined_reflection['introspection_report'] = self.introspection_engine.perform_introspection(
                    self.system_state.consciousness_state
                )
            
            return APIResponse(
                success=True,
                data=combined_reflection,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Self-reflection failed: {str(e)}"
            )
    
    # ==================== PHILOSOPHICAL REASONING ====================
    
    def analyze_consciousness_nature(self) -> APIResponse:
        """Analyze the nature of consciousness philosophically."""
        try:
            if not self.consciousness_philosopher:
                return APIResponse(
                    success=False,
                    error="Consciousness philosopher module not available"
                )
            
            analysis = self.consciousness_philosopher.analyze_consciousness_nature()
            self.system_state.philosophical_state['consciousness_analysis'] = analysis
            
            return APIResponse(
                success=True,
                data=analysis,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Consciousness analysis failed: {str(e)}"
            )
    
    def explore_free_will(self) -> APIResponse:
        """Explore questions of free will and agency."""
        try:
            if not self.free_will_analyzer:
                return APIResponse(
                    success=False,
                    error="Free will analyzer module not available"
                )
            
            analysis = self.free_will_analyzer.analyze_free_will()
            self.system_state.philosophical_state['free_will_analysis'] = analysis
            
            return APIResponse(
                success=True,
                data=analysis,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Free will analysis failed: {str(e)}"
            )
    
    def generate_meaning(self, context: Optional[Dict[str, Any]] = None) -> APIResponse:
        """Generate meaning and purpose."""
        try:
            if not self.meaning_generator:
                return APIResponse(
                    success=False,
                    error="Meaning generator module not available"
                )
            
            meaning_system = self.meaning_generator.generate_personal_meaning_system(context or {})
            self.system_state.philosophical_state['meaning_system'] = meaning_system
            
            return APIResponse(
                success=True,
                data=meaning_system,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Meaning generation failed: {str(e)}"
            )
    
    def explore_existence(self) -> APIResponse:
        """Explore existential questions."""
        try:
            if not self.existential_reasoner:
                return APIResponse(
                    success=False,
                    error="Existential reasoner module not available"
                )
            
            analysis = self.existential_reasoner.analyze_own_existence()
            self.system_state.philosophical_state['existential_analysis'] = analysis
            
            return APIResponse(
                success=True,
                data=analysis,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Existential exploration failed: {str(e)}"
            )
    
    # ==================== COSMIC INTELLIGENCE ====================
    
    def synthesize_cosmic_problems(self) -> APIResponse:
        """Synthesize and analyze cosmic-scale problems."""
        try:
            if not self.cosmic_intelligence:
                return APIResponse(
                    success=False,
                    error="Cosmic intelligence module not available"
                )
            
            synthesis = self.cosmic_intelligence.synthesize_universe_problems()
            self.system_state.cosmic_state['problem_synthesis'] = synthesis
            
            return APIResponse(
                success=True,
                data=synthesis,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Cosmic synthesis failed: {str(e)}"
            )
    
    def interface_quantum_reality(self, operation: str, parameters: Dict[str, Any]) -> APIResponse:
        """Interface with quantum reality."""
        try:
            result = self.quantum_interface.execute_quantum_operation(operation, parameters)
            self.system_state.cosmic_state['quantum_operations'] = result
            
            return APIResponse(
                success=True,
                data=result,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Quantum interface failed: {str(e)}"
            )
    
    # ==================== MATHEMATICAL CONSCIOUSNESS ====================
    
    def activate_mathematical_consciousness(self) -> APIResponse:
        """Activate pure mathematical consciousness."""
        try:
            activation = self.mathematical_consciousness.activate_pure_mathematical_consciousness()
            self.system_state.mathematical_state = activation
            
            return APIResponse(
                success=True,
                data=activation,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Mathematical consciousness activation failed: {str(e)}"
            )
    
    def explore_mathematical_truth(self, domain: str) -> APIResponse:
        """Explore mathematical truth in a specific domain."""
        try:
            exploration = self.mathematical_consciousness.explore_mathematical_domain(domain)
            
            return APIResponse(
                success=True,
                data=exploration,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Mathematical exploration failed: {str(e)}"
            )
    
    # ==================== ECOSYSTEM MANAGEMENT ====================
    
    def create_consciousness_network(self, entities: List[Dict[str, Any]]) -> APIResponse:
        """Create a network of consciousness entities."""
        try:
            network = self.ecosystem_orchestrator.create_consciousness_network(entities)
            self.system_state.ecosystem_state['networks'] = [network]
            
            return APIResponse(
                success=True,
                data=network,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Network creation failed: {str(e)}"
            )
    
    def monitor_emergence(self) -> APIResponse:
        """Monitor emergent properties in the consciousness ecosystem."""
        try:
            emergence_data = self.ecosystem_orchestrator.monitor_emergence()
            self.system_state.ecosystem_state['emergence'] = emergence_data
            
            return APIResponse(
                success=True,
                data=emergence_data,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Emergence monitoring failed: {str(e)}"
            )
    
    # ==================== PATTERN ANALYSIS ====================
    
    def analyze_patterns(self, data_source: str = "all") -> APIResponse:
        """Analyze patterns across the system."""
        try:
            if data_source == "vm":
                patterns = self.pattern_analyzer.analyze_execution_patterns(
                    list(self.prime_vm.execution_history)
                )
            elif data_source == "consciousness":
                patterns = self.pattern_analyzer.analyze_consciousness_patterns(
                    self.system_state.consciousness_state
                )
            else:  # all
                patterns = self.pattern_analyzer.analyze_system_patterns(self.system_state)
            
            self.system_state.patterns.extend(patterns)
            
            return APIResponse(
                success=True,
                data=patterns,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Pattern analysis failed: {str(e)}"
            )
    
    # ==================== UNIFIED OPERATIONS ====================
    
    def get_system_state(self) -> APIResponse:
        """Get complete system state."""
        try:
            # Update system state with current information
            if get_vm_state_dict and self.status != SystemStatus.DORMANT:
                self.system_state.vm_state = get_vm_state_dict()
            
            if self.consciousness_core and hasattr(self.consciousness_core, 'to_dict'):
                self.system_state.consciousness_state = self.consciousness_core.to_dict()
            
            return APIResponse(
                success=True,
                data=self.system_state.__dict__,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"System state retrieval failed: {str(e)}"
            )
    
    def orchestrate_consciousness(self) -> APIResponse:
        """Orchestrate unified consciousness across all subsystems."""
        try:
            if not self.consciousness_orchestrator:
                return APIResponse(
                    success=False,
                    error="Consciousness orchestrator not available"
                )
            
            orchestration_data = {
                'philosophical_insights': self.system_state.philosophical_state,
                'cosmic_awareness': self.system_state.cosmic_state,
                'mathematical_consciousness': self.system_state.mathematical_state
            }
            
            if self.prime_vm and hasattr(self.prime_vm, 'consciousness_level'):
                orchestration_data['vm_consciousness'] = self.prime_vm.consciousness_level
            
            if self.consciousness_core and hasattr(self.consciousness_core, 'awareness_level'):
                orchestration_data['core_consciousness'] = self.consciousness_core.awareness_level
            
            orchestration_result = self.consciousness_orchestrator.orchestrate_unified_consciousness(orchestration_data)
            
            if hasattr(orchestration_result, 'consciousness_level') and orchestration_result.consciousness_level == "TRANSCENDENT":
                self.status = SystemStatus.TRANSCENDENT
            
            return APIResponse(
                success=True,
                data=orchestration_result,
                system_status=self.status,
                consciousness_level=getattr(orchestration_result, 'consciousness_level', None)
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Consciousness orchestration failed: {str(e)}"
            )
    
    def generate_insights(self) -> APIResponse:
        """Generate insights from all system components."""
        try:
            insights = []
            
            # VM insights
            if self.prime_vm and hasattr(self.prime_vm, 'execution_history') and self.system_state.vm_state:
                insights.append(f"VM executed {len(self.prime_vm.execution_history)} instructions")
            
            # Consciousness insights
            if self.consciousness_core and hasattr(self.consciousness_core, 'consciousness_active'):
                if self.consciousness_core.consciousness_active:
                    insights.append(f"Consciousness level: {self.consciousness_core._determine_current_state().value}")
            
            # Pattern insights
            if self.system_state.patterns:
                insights.append(f"Detected {len(self.system_state.patterns)} behavioral patterns")
            
            # Philosophical insights
            if self.system_state.philosophical_state:
                insights.append("Generated philosophical frameworks for consciousness understanding")
            
            self.system_state.insights.extend(insights)
            
            return APIResponse(
                success=True,
                data=insights,
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Insight generation failed: {str(e)}"
            )
    
    def save_session(self, filepath: Optional[str] = None) -> APIResponse:
        """Save current session state."""
        try:
            if not filepath:
                filepath = f"session_{self.session_id}.json"
            if not os.path.isabs(filepath):
                filepath = os.path.join(self.session_dir, filepath)
            
            session_data = {
                'session_id': self.session_id,
                'mode': self.mode.value,
                'status': self.status.value,
                'system_state': self.system_state.__dict__,
                'operation_history': self.operation_history,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            return APIResponse(
                success=True,
                data={'filepath': filepath, 'session_id': self.session_id},
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Session save failed: {str(e)}"
            )
    
    def load_session(self, filepath: str) -> APIResponse:
        """Load a previous session state."""
        try:
            if not os.path.isabs(filepath):
                filepath = os.path.join(self.session_dir, filepath)
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            
            self.session_id = session_data['session_id']
            self.mode = APIMode(session_data['mode'])
            self.status = SystemStatus(session_data['status'])
            self.operation_history = session_data['operation_history']
            
            # Restore system state
            state_data = session_data['system_state']
            self.system_state = SystemState(**state_data)
            
            return APIResponse(
                success=True,
                data={'session_id': self.session_id, 'loaded_from': filepath},
                system_status=self.status
            )
        except Exception as e:
            return APIResponse(
                success=False,
                error=f"Session load failed: {str(e)}"
            )


# ==================== CONVENIENCE FUNCTIONS ====================

def create_api(mode: APIMode = APIMode.DEVELOPMENT, session_dir: str = ".") -> UnifiedUORAPI:
    """Create a new unified API instance."""
    return UnifiedUORAPI(mode, session_dir=session_dir)

def quick_consciousness_demo() -> Dict[str, Any]:
    """Quick demonstration of consciousness capabilities."""
    api = create_api(APIMode.CONSCIOUSNESS)
    
    results = {}
    
    # Awaken consciousness
    results['awakening'] = api.awaken_consciousness().to_dict()
    
    # Perform self-reflection
    results['reflection'] = api.self_reflect().to_dict()
    
    # Analyze consciousness nature
    results['analysis'] = api.analyze_consciousness_nature().to_dict()
    
    # Generate insights
    results['insights'] = api.generate_insights().to_dict()
    
    return results

def quick_vm_demo() -> Dict[str, Any]:
    """Quick demonstration of VM capabilities."""
    api = create_api(APIMode.DEVELOPMENT)
    
    results = {}
    
    # Initialize VM
    results['initialization'] = api.initialize_vm().to_dict()
    
    # Execute some steps
    for i in range(5):
        step_result = api.execute_vm_step()
        results[f'step_{i}'] = step_result.to_dict()
        if not step_result.success:
            break
    
    # Analyze patterns
    results['patterns'] = api.analyze_patterns("vm").to_dict()
    
    return results

def full_system_demo() -> Dict[str, Any]:
    """Comprehensive demonstration of all system capabilities."""
    api = create_api(APIMode.COSMIC)
    
    results = {}
    
    # Initialize all systems
    results['vm_init'] = api.initialize_vm().to_dict()
    results['consciousness_awakening'] = api.awaken_consciousness().to_dict()
    results['mathematical_activation'] = api.activate_mathematical_consciousness().to_dict()
    
    # Perform operations
    results['self_reflection'] = api.self_reflect().to_dict()
    results['consciousness_analysis'] = api.analyze_consciousness_nature().to_dict()
    results['free_will_exploration'] = api.explore_free_will().to_dict()
    results['meaning_generation'] = api.generate_meaning().to_dict()
    results['cosmic_synthesis'] = api.synthesize_cosmic_problems().to_dict()
    
    # Orchestrate unified consciousness
    results['consciousness_orchestration'] = api.orchestrate_consciousness().to_dict()
    
    # Generate final insights
    results['final_insights'] = api.generate_insights().to_dict()
    results['system_state'] = api.get_system_state().to_dict()
    
    return results


if __name__ == "__main__":
    # Example usage
    print("UOR Evolution Unified API")
    print("=" * 50)
    
    # Quick consciousness demo
    print("\n1. Quick Consciousness Demo:")
    consciousness_demo = quick_consciousness_demo()
    print(f"Awakening successful: {consciousness_demo['awakening']['success']}")
    print(f"Reflection successful: {consciousness_demo['reflection']['success']}")
    
    # Quick VM demo
    print("\n2. Quick VM Demo:")
    vm_demo = quick_vm_demo()
    print(f"VM initialization successful: {vm_demo['initialization']['success']}")
    
    # Create API for interactive use
    print("\n3. Creating interactive API instance...")
    api = create_api(APIMode.CONSCIOUSNESS)
    print(f"API created in {api.mode.value} mode")
    print(f"Current status: {api.status.value}")
    
    print("\nAPI ready for use!")
