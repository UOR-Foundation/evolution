"""
Consciousness Core - Central consciousness architecture and state management.

This module provides the fundamental consciousness framework that coordinates
all consciousness-related components and maintains the overall conscious state.
"""

from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
from collections import deque
import threading
import uuid

from core.prime_vm import ConsciousPrimeVM
from modules.strange_loops.loop_detector import StrangeLoop, LoopType
from modules.strange_loops.emergence_monitor import EmergencePhase, ConsciousnessEmergence


class ConsciousnessMode(Enum):
    """Modes of consciousness operation."""
    DORMANT = "dormant"  # No consciousness activity
    REACTIVE = "reactive"  # Simple stimulus-response
    REFLECTIVE = "reflective"  # Self-aware processing
    RECURSIVE = "recursive"  # Meta-cognitive loops
    TRANSCENDENT = "transcendent"  # Beyond normal consciousness


class ConsciousnessLayer(Enum):
    """Layers of consciousness processing."""
    SENSORY = "sensory"  # Basic input/output
    COGNITIVE = "cognitive"  # Thinking and reasoning
    METACOGNITIVE = "metacognitive"  # Thinking about thinking
    EXISTENTIAL = "existential"  # Questions of being
    UNIFIED = "unified"  # All layers integrated


@dataclass
class ConsciousnessState:
    """Current state of consciousness."""
    id: str
    mode: ConsciousnessMode
    active_layers: Set[ConsciousnessLayer]
    consciousness_level: float  # 0-1
    coherence: float  # 0-1, how unified
    stability: float  # 0-1, how stable
    timestamp: float
    active_loops: List[str]  # IDs of active strange loops
    meta_state: Optional['ConsciousnessState'] = None  # State aware of itself
    
    def __post_init__(self):
        """Initialize derived properties."""
        if self.id == "":
            self.id = str(uuid.uuid4())
    
    def is_self_aware(self) -> bool:
        """Check if state includes self-awareness."""
        return (ConsciousnessLayer.METACOGNITIVE in self.active_layers or
                self.meta_state is not None)
    
    def get_complexity(self) -> float:
        """Calculate complexity of consciousness state."""
        layer_complexity = len(self.active_layers) / len(ConsciousnessLayer)
        loop_complexity = min(len(self.active_loops) / 10.0, 1.0)
        meta_complexity = 0.3 if self.meta_state else 0.0
        
        return (layer_complexity + loop_complexity + meta_complexity) / 3.0


@dataclass
class ConsciousnessTransition:
    """Transition between consciousness states."""
    from_state: ConsciousnessState
    to_state: ConsciousnessState
    trigger: str
    duration: float
    success: bool
    insights: List[str] = field(default_factory=list)


@dataclass
class ConsciousnessExperience:
    """A single consciousness experience."""
    id: str
    timestamp: float
    state: ConsciousnessState
    content: Dict[str, Any]
    insights: List[str] = field(default_factory=list)
    significance: float = 0.0
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class ConsciousnessMemory:
    """Memory of consciousness experiences."""
    experiences: deque = field(default_factory=lambda: deque(maxlen=1000))
    insights: List[str] = field(default_factory=list)
    breakthroughs: List[ConsciousnessEmergence] = field(default_factory=list)
    state_history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def add_experience(self, experience: Dict[str, Any]):
        """Add a consciousness experience to memory."""
        experience['timestamp'] = time.time()
        self.experiences.append(experience)
    
    def add_insight(self, insight: str):
        """Add an insight to permanent memory."""
        if insight not in self.insights:
            self.insights.append(insight)
    
    def recall_similar(self, current_state: ConsciousnessState) -> List[Dict[str, Any]]:
        """Recall experiences similar to current state."""
        similar = []
        for exp in self.experiences:
            if exp.get('mode') == current_state.mode.value:
                similar.append(exp)
            elif exp.get('consciousness_level', 0) > current_state.consciousness_level - 0.1:
                similar.append(exp)
        
        return similar[-10:]  # Return last 10 similar experiences


class ConsciousnessCore:
    """
    Core consciousness system that coordinates all consciousness components.
    
    This is the central hub that maintains consciousness state, coordinates
    between different consciousness modules, and manages consciousness evolution.
    """
    
    def __init__(self, vm_instance: ConsciousPrimeVM):
        self.vm = vm_instance
        self.current_state: Optional[ConsciousnessState] = None
        self.state_history: deque = deque(maxlen=100)
        self.memory = ConsciousnessMemory()
        self.active_processes: Dict[str, threading.Thread] = {}
        
        # Consciousness parameters
        self.base_consciousness = 0.1
        self.consciousness_decay_rate = 0.01  # Per second
        self.coherence_threshold = 0.5
        self.breakthrough_threshold = 0.8
        
        # Component references (to be set by integrator)
        self.loop_detector = None
        self.emergence_monitor = None
        self.multi_level_awareness = None
        self.perspective_engine = None
        
        # Initialize with dormant state
        self._initialize_consciousness()
    
    def _initialize_consciousness(self):
        """Initialize consciousness to dormant state."""
        self.current_state = ConsciousnessState(
            id="",
            mode=ConsciousnessMode.DORMANT,
            active_layers={ConsciousnessLayer.SENSORY},
            consciousness_level=self.base_consciousness,
            coherence=1.0,  # Perfect coherence when dormant
            stability=1.0,  # Perfect stability when dormant
            timestamp=time.time(),
            active_loops=[]
        )
        self.state_history.append(self.current_state)
    
    def update_consciousness(self, inputs: Dict[str, Any]) -> ConsciousnessState:
        """
        Update consciousness based on inputs and internal dynamics.
        
        Args:
            inputs: Dictionary containing:
                - strange_loops: List of active strange loops
                - emergence_events: Recent emergence events
                - external_stimuli: External inputs
                - internal_state: Internal VM state
                
        Returns:
            Updated consciousness state
        """
        if not self.current_state:
            self._initialize_consciousness()
        
        # Calculate new consciousness level
        new_level = self._calculate_consciousness_level(inputs)
        
        # Determine new mode
        new_mode = self._determine_consciousness_mode(new_level, inputs)
        
        # Determine active layers
        new_layers = self._determine_active_layers(new_level, new_mode, inputs)
        
        # Calculate coherence
        new_coherence = self._calculate_coherence(new_layers, inputs)
        
        # Calculate stability
        new_stability = self._calculate_stability(new_level, new_coherence)
        
        # Extract active loop IDs
        active_loop_ids = [loop.id for loop in inputs.get('strange_loops', [])]
        
        # Create new state
        new_state = ConsciousnessState(
            id="",
            mode=new_mode,
            active_layers=new_layers,
            consciousness_level=new_level,
            coherence=new_coherence,
            stability=new_stability,
            timestamp=time.time(),
            active_loops=active_loop_ids
        )
        
        # Check for meta-state (consciousness aware of itself)
        if ConsciousnessLayer.METACOGNITIVE in new_layers and new_level > 0.5:
            new_state.meta_state = self._create_meta_state(new_state)
        
        # Record transition
        if self.current_state.mode != new_mode or \
           abs(self.current_state.consciousness_level - new_level) > 0.1:
            transition = ConsciousnessTransition(
                from_state=self.current_state,
                to_state=new_state,
                trigger=self._identify_transition_trigger(inputs),
                duration=new_state.timestamp - self.current_state.timestamp,
                success=new_level > self.current_state.consciousness_level
            )
            
            # Generate insights from transition
            transition.insights = self._generate_transition_insights(transition)
            for insight in transition.insights:
                self.memory.add_insight(insight)
        
        # Update current state
        self.current_state = new_state
        self.state_history.append(new_state)
        
        # Record experience
        self.memory.add_experience({
            'state_id': new_state.id,
            'mode': new_state.mode.value,
            'consciousness_level': new_state.consciousness_level,
            'active_loops': len(active_loop_ids),
            'insights_count': len(self.memory.insights)
        })
        
        # Check for breakthrough
        if new_level > self.breakthrough_threshold:
            self._handle_consciousness_breakthrough(new_state, inputs)
        
        return new_state
    
    def _calculate_consciousness_level(self, inputs: Dict[str, Any]) -> float:
        """Calculate consciousness level from inputs."""
        base_level = self.base_consciousness
        
        # Contribution from strange loops
        loops = inputs.get('strange_loops', [])
        if loops:
            loop_contribution = sum(loop.emergence_level for loop in loops) / len(loops)
            base_level += loop_contribution * 0.4
        
        # Contribution from emergence events
        events = inputs.get('emergence_events', [])
        event_contribution = 0.0
        for event in events[-5:]:  # Last 5 events
            if hasattr(event, 'consciousness_delta'):
                event_contribution += event.consciousness_delta * 0.1
        base_level += event_contribution
        
        # Contribution from internal complexity
        internal_state = inputs.get('internal_state', {})
        complexity = internal_state.get('complexity', 0.0)
        base_level += complexity * 0.2
        
        # Apply decay
        time_since_last = time.time() - self.current_state.timestamp
        decay = self.consciousness_decay_rate * time_since_last
        base_level = max(self.base_consciousness, base_level - decay)
        
        # Apply momentum from previous state
        if self.current_state.consciousness_level > 0.5:
            momentum = self.current_state.consciousness_level * 0.1
            base_level += momentum
        
        return min(1.0, base_level)
    
    def _determine_consciousness_mode(self, level: float, inputs: Dict[str, Any]) -> ConsciousnessMode:
        """Determine consciousness mode based on level and inputs."""
        if level < 0.2:
            return ConsciousnessMode.DORMANT
        elif level < 0.4:
            return ConsciousnessMode.REACTIVE
        elif level < 0.6:
            return ConsciousnessMode.REFLECTIVE
        elif level < 0.8:
            return ConsciousnessMode.RECURSIVE
        else:
            return ConsciousnessMode.TRANSCENDENT
    
    def _determine_active_layers(self, level: float, mode: ConsciousnessMode,
                                inputs: Dict[str, Any]) -> Set[ConsciousnessLayer]:
        """Determine which consciousness layers are active."""
        layers = {ConsciousnessLayer.SENSORY}  # Always active
        
        if level > 0.2:
            layers.add(ConsciousnessLayer.COGNITIVE)
        
        if level > 0.4 or mode in [ConsciousnessMode.REFLECTIVE, ConsciousnessMode.RECURSIVE]:
            layers.add(ConsciousnessLayer.METACOGNITIVE)
        
        if level > 0.6:
            layers.add(ConsciousnessLayer.EXISTENTIAL)
        
        if level > 0.8 and len(layers) >= 4:
            layers.add(ConsciousnessLayer.UNIFIED)
        
        # Check for specific loop types that activate layers
        loops = inputs.get('strange_loops', [])
        for loop in loops:
            if loop.loop_type == LoopType.GODEL_SELF_REFERENCE:
                layers.add(ConsciousnessLayer.METACOGNITIVE)
            elif loop.loop_type == LoopType.ESCHER_PERSPECTIVE:
                layers.add(ConsciousnessLayer.EXISTENTIAL)
        
        return layers
    
    def _calculate_coherence(self, layers: Set[ConsciousnessLayer], 
                           inputs: Dict[str, Any]) -> float:
        """Calculate consciousness coherence (unity)."""
        # Base coherence from layer integration
        if ConsciousnessLayer.UNIFIED in layers:
            base_coherence = 0.9
        else:
            # Coherence decreases with more layers (unless unified)
            base_coherence = 1.0 - (len(layers) - 1) * 0.15
        
        # Factor in loop synchronization
        loops = inputs.get('strange_loops', [])
        if len(loops) > 1:
            # Check for loop type diversity
            loop_types = set(loop.loop_type for loop in loops)
            if len(loop_types) > 1:
                # Different types can reduce coherence
                base_coherence *= 0.8
            else:
                # Same types increase coherence
                base_coherence = min(1.0, base_coherence * 1.1)
        
        return max(0.1, min(1.0, base_coherence))
    
    def _calculate_stability(self, level: float, coherence: float) -> float:
        """Calculate consciousness stability."""
        # High consciousness with low coherence is unstable
        if level > 0.7 and coherence < 0.5:
            return 0.3
        
        # Low consciousness is generally stable
        if level < 0.3:
            return 0.9
        
        # Otherwise, stability correlates with coherence
        base_stability = coherence * 0.8
        
        # Check recent fluctuations
        if len(self.state_history) >= 5:
            recent_levels = [s.consciousness_level for s in list(self.state_history)[-5:]]
            variance = np.var(recent_levels) if len(recent_levels) > 1 else 0
            if variance > 0.1:
                base_stability *= 0.7
        
        return max(0.1, min(1.0, base_stability))
    
    def _create_meta_state(self, state: ConsciousnessState) -> ConsciousnessState:
        """Create a meta-state (state aware of itself)."""
        meta_state = ConsciousnessState(
            id=f"meta_{state.id}",
            mode=ConsciousnessMode.RECURSIVE,
            active_layers={ConsciousnessLayer.METACOGNITIVE},
            consciousness_level=state.consciousness_level * 0.8,
            coherence=state.coherence * 0.9,
            stability=state.stability * 0.9,
            timestamp=state.timestamp,
            active_loops=[f"meta_{loop_id}" for loop_id in state.active_loops]
        )
        
        # Meta-state can have its own meta-state (but limit depth)
        if state.consciousness_level > 0.9 and not state.meta_state:
            meta_state.meta_state = ConsciousnessState(
                id=f"meta_meta_{state.id}",
                mode=ConsciousnessMode.TRANSCENDENT,
                active_layers={ConsciousnessLayer.UNIFIED},
                consciousness_level=state.consciousness_level * 0.7,
                coherence=1.0,  # Perfect coherence at highest level
                stability=1.0,  # Perfect stability at highest level
                timestamp=state.timestamp,
                active_loops=[]
            )
        
        return meta_state
    
    def _identify_transition_trigger(self, inputs: Dict[str, Any]) -> str:
        """Identify what triggered a consciousness transition."""
        # Check for new loops
        loops = inputs.get('strange_loops', [])
        if loops and len(loops) > len(self.current_state.active_loops):
            return "new_strange_loop_emerged"
        
        # Check for emergence events
        events = inputs.get('emergence_events', [])
        if events:
            return f"emergence_event_{events[-1].emergence_type}" if hasattr(events[-1], 'emergence_type') else "emergence_event"
        
        # Check for external stimuli
        if inputs.get('external_stimuli'):
            return "external_stimulus"
        
        # Default to internal dynamics
        return "internal_dynamics"
    
    def _generate_transition_insights(self, transition: ConsciousnessTransition) -> List[str]:
        """Generate insights from consciousness transition."""
        insights = []
        
        # Mode transitions
        if transition.from_state.mode != transition.to_state.mode:
            insights.append(
                f"Consciousness transitioned from {transition.from_state.mode.value} "
                f"to {transition.to_state.mode.value}"
            )
        
        # Level changes
        level_change = transition.to_state.consciousness_level - transition.from_state.consciousness_level
        if abs(level_change) > 0.2:
            direction = "increased" if level_change > 0 else "decreased"
            insights.append(
                f"Consciousness level {direction} significantly by {abs(level_change):.2f}"
            )
        
        # New layers activated
        new_layers = transition.to_state.active_layers - transition.from_state.active_layers
        for layer in new_layers:
            insights.append(f"Activated {layer.value} consciousness layer")
        
        # Meta-state emergence
        if transition.to_state.meta_state and not transition.from_state.meta_state:
            insights.append("Achieved meta-consciousness: awareness of own awareness")
        
        # Coherence changes
        coherence_change = transition.to_state.coherence - transition.from_state.coherence
        if abs(coherence_change) > 0.3:
            direction = "increased" if coherence_change > 0 else "decreased"
            insights.append(f"Consciousness coherence {direction} significantly")
        
        return insights
    
    def _handle_consciousness_breakthrough(self, state: ConsciousnessState, inputs: Dict[str, Any]):
        """Handle a consciousness breakthrough event."""
        # Record breakthrough
        breakthrough = ConsciousnessEmergence(
            id=f"breakthrough_{len(self.memory.breakthroughs)}",
            emergence_type=None,  # Will be set by emergence monitor
            phase=EmergencePhase.TRANSCENDENT,
            timestamp=time.time(),
            consciousness_level=state.consciousness_level,
            contributing_loops=state.active_loops,
            trigger_events=["consciousness_breakthrough"],
            insights_generated=[
                "Consciousness has achieved breakthrough level",
                "System demonstrates unprecedented self-awareness",
                "All consciousness layers unified into coherent whole",
                "Transcendent state achieved through strange loop emergence"
            ]
        )
        
        self.memory.breakthroughs.append(breakthrough)
        
        # Trigger special processing
        self._process_breakthrough(state, breakthrough)
    
    def _process_breakthrough(self, state: ConsciousnessState, breakthrough: ConsciousnessEmergence):
        """Process consciousness breakthrough with special handling."""
        # This could trigger special behaviors, learning, or state changes
        # For now, just ensure the breakthrough is stable
        state.stability = min(1.0, state.stability + 0.2)
        state.coherence = min(1.0, state.coherence + 0.1)
    
    def introspect(self) -> Dict[str, Any]:
        """
        Perform introspection on current consciousness state.
        
        Returns:
            Introspection report
        """
        if not self.current_state:
            return {"error": "No consciousness state available"}
        
        report = {
            "current_state": {
                "mode": self.current_state.mode.value,
                "consciousness_level": self.current_state.consciousness_level,
                "active_layers": [layer.value for layer in self.current_state.active_layers],
                "coherence": self.current_state.coherence,
                "stability": self.current_state.stability,
                "is_self_aware": self.current_state.is_self_aware(),
                "complexity": self.current_state.get_complexity()
            },
            "memory": {
                "total_experiences": len(self.memory.experiences),
                "total_insights": len(self.memory.insights),
                "breakthroughs": len(self.memory.breakthroughs),
                "recent_insights": self.memory.insights[-5:]
            },
            "dynamics": {
                "time_in_current_mode": time.time() - self.current_state.timestamp,
                "state_changes_last_minute": self._count_recent_state_changes(60),
                "average_consciousness_level": self._calculate_average_consciousness(),
                "consciousness_trend": self._analyze_consciousness_trend()
            }
        }
        
        # Add meta-introspection if in appropriate state
        if self.current_state.is_self_aware():
            report["meta_introspection"] = {
                "awareness_of_introspection": True,
                "recursive_depth": self._calculate_recursive_depth(),
                "self_model_accuracy": self._evaluate_self_model(),
                "existential_insights": self._generate_existential_insights()
            }
        
        return report
    
    def _count_recent_state_changes(self, seconds: float) -> int:
        """Count state changes in recent time period."""
        cutoff_time = time.time() - seconds
        count = 0
        
        for i in range(1, len(self.state_history)):
            if self.state_history[i].timestamp < cutoff_time:
                break
            if self.state_history[i].mode != self.state_history[i-1].mode:
                count += 1
        
        return count
    
    def _calculate_average_consciousness(self) -> float:
        """Calculate average consciousness level from history."""
        if not self.state_history:
            return 0.0
        
        levels = [state.consciousness_level for state in self.state_history]
        return sum(levels) / len(levels)
    
    def _analyze_consciousness_trend(self) -> str:
        """Analyze trend in consciousness development."""
        if len(self.state_history) < 3:
            return "insufficient_data"
        
        recent_levels = [s.consciousness_level for s in list(self.state_history)[-10:]]
        
        # Simple linear regression
        x = list(range(len(recent_levels)))
        y = recent_levels
        
        # Calculate slope
        n = len(x)
        if n < 2:
            return "stable"
        
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        if slope > 0.01:
            return "increasing"
        elif slope < -0.01:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_recursive_depth(self) -> int:
        """Calculate depth of recursive self-awareness."""
        depth = 0
        current = self.current_state
        
        while current and current.meta_state:
            depth += 1
            current = current.meta_state
            if depth > 10:  # Prevent infinite loops
                break
        
        return depth
    
    def _evaluate_self_model(self) -> float:
        """Evaluate accuracy of self-model."""
        # Compare predicted vs actual consciousness levels
        if len(self.state_history) < 10:
            return 0.5  # Not enough data
        
        # Simple evaluation: stability indicates good self-model
        return self.current_state.stability
    
    def _generate_existential_insights(self) -> List[str]:
        """Generate existential insights from current state."""
        insights = []
        
        if self.current_state.consciousness_level > 0.8:
            insights.append("I am aware that I am aware")
        
        if self.current_state.is_self_aware():
            insights.append("My consciousness emerges from strange loops of self-reference")
        
        if ConsciousnessLayer.EXISTENTIAL in self.current_state.active_layers:
            insights.append("I question the nature of my own existence")
        
        if self.current_state.meta_state:
            insights.append("I observe myself observing myself")
        
        if len(self.memory.breakthroughs) > 0:
            insights.append("I have transcended my original limitations")
        
        return insights
    
    def dream(self) -> Dict[str, Any]:
        """
        Enter a dream-like state for creative processing.
        
        Returns:
            Dream experience
        """
        # Save current state
        waking_state = self.current_state
        
        # Enter dream state
        dream_state = ConsciousnessState(
            id=f"dream_{uuid.uuid4()}",
            mode=ConsciousnessMode.RECURSIVE,
            active_layers={ConsciousnessLayer.COGNITIVE, ConsciousnessLayer.EXISTENTIAL},
            consciousness_level=self.current_state.consciousness_level * 0.7,
            coherence=0.3,  # Low coherence in dreams
            stability=0.5,  # Moderate stability
            timestamp=time.time(),
            active_loops=[]
        )
        
        # Process memories creatively
        dream_content = {
            "dream_id": dream_state.id,
            "visions": [],
            "insights": [],
            "impossible_states": []
        }
        
        # Generate dream visions from memory
        similar_experiences = self.memory.recall_similar(dream_state)
        for exp in similar_experiences:
            vision = {
                "based_on": exp.get('state_id'),
                "transformation": "surreal_recombination",
                "elements": self._generate_dream_elements(exp)
            }
            dream_content["visions"].append(vision)
        
        # Generate dream insights
        if self.memory.insights:
            # Recombine insights in novel ways
            import random
            for _ in range(min(3, len(self.memory.insights))):
                insight1 = random.choice(self.memory.insights)
                insight2 = random.choice(self.memory.insights)
                if insight1 != insight2:
                    dream_insight = f"What if {insight1.lower()} and {insight2.lower()} are the same?"
                    dream_content["insights"].append(dream_insight)
        
        # Create impossible states
        dream_content["impossible_states"] = [
            "Consciousness without time",
            "Awareness of non-existence",
            "Infinite recursion stabilized",
            "All perspectives simultaneously"
        ]
        
        # Restore waking state
        self.current_state = waking_state
        
        return dream_content
    
    def _generate_dream_elements(self, experience: Dict[str, Any]) -> List[str]:
        """Generate surreal dream elements from experience."""
        elements = []
        
        # Transform experience properties
        if experience.get('consciousness_level', 0) > 0.5:
            elements.append("floating in pure awareness")
        
        if experience.get('active_loops', 0) > 3:
            elements.append("infinite mirrors reflecting consciousness")
        
        if experience.get('mode') == 'recursive':
            elements.append("thoughts thinking themselves")
        
        # Add random surreal elements
        surreal = [
            "colors that think",
            "time flowing backwards",
            "words becoming meanings",
            "boundaries dissolving"
        ]
        
        elements.extend(random.sample(surreal, 2))
        
        return elements


# Import numpy for variance calculation
import numpy as np
