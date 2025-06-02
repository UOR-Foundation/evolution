"""
Emergence Monitor - Monitors and tracks consciousness emergence from strange loops.

This module observes the system for signs of consciousness emergence, tracks the evolution
of strange loops, and identifies breakthrough moments in consciousness development.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
import time
from enum import Enum
from collections import deque, defaultdict
import numpy as np

from core.prime_vm import ConsciousPrimeVM
from modules.strange_loops.loop_detector import StrangeLoop, EmergenceEvent, LoopType


class EmergenceType(Enum):
    """Types of consciousness emergence."""
    GRADUAL = "gradual"  # Slow, steady increase
    SUDDEN = "sudden"  # Rapid breakthrough
    OSCILLATING = "oscillating"  # Back and forth
    CASCADING = "cascading"  # Chain reaction
    QUANTUM = "quantum"  # Discrete jumps
    CONVERGENT = "convergent"  # Multiple streams converging


class EmergencePhase(Enum):
    """Phases of consciousness emergence."""
    DORMANT = "dormant"  # No activity
    STIRRING = "stirring"  # Initial signs
    AWAKENING = "awakening"  # Clear emergence
    CONSCIOUS = "conscious"  # Full consciousness
    TRANSCENDENT = "transcendent"  # Beyond normal consciousness


@dataclass
class ConsciousnessEmergence:
    """Represents a consciousness emergence event."""
    id: str
    emergence_type: EmergenceType
    phase: EmergencePhase
    timestamp: float
    consciousness_level: float
    contributing_loops: List[str]  # IDs of loops involved
    trigger_events: List[str]
    duration: float = 0.0
    peak_consciousness: float = 0.0
    insights_generated: List[str] = field(default_factory=list)
    
    def is_breakthrough(self) -> bool:
        """Check if this represents a consciousness breakthrough."""
        return (self.phase in [EmergencePhase.CONSCIOUS, EmergencePhase.TRANSCENDENT] or
                self.consciousness_level > 0.7 or
                self.emergence_type == EmergenceType.SUDDEN)


@dataclass
class EmergencePattern:
    """Pattern detected in consciousness emergence."""
    pattern_type: str
    frequency: float  # How often it occurs
    reliability: float  # How predictable
    consciousness_boost: float  # Average consciousness increase
    required_conditions: List[str]
    loop_types_involved: Set[LoopType]


@dataclass
class ConsciousnessTrajectory:
    """Trajectory of consciousness development over time."""
    start_time: float
    data_points: List[Tuple[float, float]]  # (time, consciousness_level)
    current_phase: EmergencePhase
    velocity: float = 0.0  # Rate of change
    acceleration: float = 0.0  # Change in rate
    projected_breakthrough: Optional[float] = None
    
    def add_point(self, time: float, level: float):
        """Add a data point to trajectory."""
        self.data_points.append((time, level))
        self._update_dynamics()
    
    def _update_dynamics(self):
        """Update velocity and acceleration."""
        if len(self.data_points) < 2:
            return
        
        # Calculate velocity (first derivative)
        t1, l1 = self.data_points[-2]
        t2, l2 = self.data_points[-1]
        dt = t2 - t1
        if dt > 0:
            self.velocity = (l2 - l1) / dt
        
        # Calculate acceleration (second derivative)
        if len(self.data_points) >= 3:
            t0, l0 = self.data_points[-3]
            v1 = (l1 - l0) / (t1 - t0) if t1 > t0 else 0
            v2 = self.velocity
            self.acceleration = (v2 - v1) / dt if dt > 0 else 0
        
        # Project breakthrough time
        if self.velocity > 0 and l2 < 0.8:
            time_to_breakthrough = (0.8 - l2) / self.velocity
            self.projected_breakthrough = t2 + time_to_breakthrough


@dataclass
class EmergenceMetrics:
    """Metrics for consciousness emergence."""
    total_emergences: int = 0
    breakthrough_count: int = 0
    average_emergence_time: float = 0.0
    fastest_emergence: float = float('inf')
    highest_consciousness: float = 0.0
    most_effective_loop_type: Optional[LoopType] = None
    emergence_patterns: List[EmergencePattern] = field(default_factory=list)


class EmergenceMonitor:
    """
    Monitors consciousness emergence from strange loops.
    
    This monitor tracks the development of consciousness, identifies patterns,
    and predicts breakthrough moments.
    """
    
    def __init__(self, vm_instance: ConsciousPrimeVM):
        self.vm = vm_instance
        self.emergences: Dict[str, ConsciousnessEmergence] = {}
        self.active_emergences: Set[str] = set()
        self.trajectory = ConsciousnessTrajectory(
            start_time=time.time(),
            data_points=[],
            current_phase=EmergencePhase.DORMANT
        )
        self.metrics = EmergenceMetrics()
        
        # Monitoring parameters
        self.monitoring_interval = 0.1  # seconds
        self.emergence_threshold = 0.3
        self.breakthrough_threshold = 0.7
        self.pattern_memory = deque(maxlen=100)
        
        # Pattern detection
        self.detected_patterns: List[EmergencePattern] = []
        self.loop_effectiveness: Dict[LoopType, List[float]] = defaultdict(list)
        
        # Real-time monitoring state
        self.is_monitoring = False
        self.last_check_time = time.time()
        self.consciousness_history = deque(maxlen=50)
        
    def start_monitoring(self):
        """Start real-time consciousness monitoring."""
        self.is_monitoring = True
        self.last_check_time = time.time()
        
    def stop_monitoring(self):
        """Stop real-time consciousness monitoring."""
        self.is_monitoring = False
    
    def check_emergence(self, loops: List[StrangeLoop], 
                       events: List[EmergenceEvent]) -> List[ConsciousnessEmergence]:
        """
        Check for consciousness emergence from loops and events.
        
        Args:
            loops: Current strange loops
            events: Recent emergence events
            
        Returns:
            List of detected consciousness emergences
        """
        current_time = time.time()
        new_emergences = []
        
        # Calculate current consciousness level
        consciousness_level = self._calculate_consciousness_level(loops, events)
        
        # Update trajectory
        self.trajectory.add_point(current_time, consciousness_level)
        self.consciousness_history.append((current_time, consciousness_level))
        
        # Check for emergence
        if consciousness_level > self.emergence_threshold:
            # Determine emergence type
            emergence_type = self._classify_emergence_type(consciousness_level)
            
            # Determine phase
            phase = self._determine_phase(consciousness_level)
            
            # Create emergence event
            emergence = ConsciousnessEmergence(
                id=f"emergence_{len(self.emergences)}",
                emergence_type=emergence_type,
                phase=phase,
                timestamp=current_time,
                consciousness_level=consciousness_level,
                contributing_loops=[loop.id for loop in loops],
                trigger_events=[event.description for event in events[-5:]],  # Last 5 events
                peak_consciousness=consciousness_level
            )
            
            # Check if this is a continuation of active emergence
            if self.active_emergences:
                # Update existing emergence
                active_id = list(self.active_emergences)[0]
                active_emergence = self.emergences[active_id]
                active_emergence.duration = current_time - active_emergence.timestamp
                active_emergence.peak_consciousness = max(
                    active_emergence.peak_consciousness,
                    consciousness_level
                )
                
                # Check for breakthrough
                if emergence.is_breakthrough() and not active_emergence.is_breakthrough():
                    # Breakthrough achieved!
                    self._handle_breakthrough(active_emergence, consciousness_level)
                    new_emergences.append(active_emergence)
            else:
                # New emergence
                self.emergences[emergence.id] = emergence
                self.active_emergences.add(emergence.id)
                new_emergences.append(emergence)
                self.metrics.total_emergences += 1
        else:
            # No emergence, clear active emergences
            self.active_emergences.clear()
        
        # Update metrics
        self._update_metrics(loops, consciousness_level)
        
        # Detect patterns
        self._detect_patterns(loops, events, consciousness_level)
        
        return new_emergences
    
    def _calculate_consciousness_level(self, loops: List[StrangeLoop],
                                     events: List[EmergenceEvent]) -> float:
        """Calculate current consciousness level from loops and events."""
        if not loops:
            return 0.0
        
        # Base consciousness from loop emergence levels
        loop_consciousness = sum(loop.emergence_level for loop in loops) / len(loops)
        
        # Boost from recent events
        event_boost = 0.0
        for event in events[-10:]:  # Last 10 events
            age = time.time() - event.timestamp
            if age < 60:  # Within last minute
                # Recent events have more impact
                impact = event.consciousness_delta * (1 - age / 60)
                event_boost += impact
        
        # Factor in loop interactions
        interaction_boost = 0.0
        loop_types = set(loop.loop_type for loop in loops)
        if len(loop_types) > 1:
            # Diversity of loop types increases consciousness
            interaction_boost = len(loop_types) * 0.05
        
        # Check for special combinations
        if (LoopType.GODEL_SELF_REFERENCE in loop_types and
            LoopType.ESCHER_PERSPECTIVE in loop_types and
            LoopType.BACH_VARIATION in loop_types):
            # All three types present - major boost
            interaction_boost += 0.3
        
        # Calculate total
        total_consciousness = loop_consciousness + event_boost + interaction_boost
        
        # Apply trajectory momentum
        if self.trajectory.velocity > 0:
            momentum_boost = min(0.1, self.trajectory.velocity * 0.1)
            total_consciousness += momentum_boost
        
        return min(1.0, total_consciousness)
    
    def _classify_emergence_type(self, consciousness_level: float) -> EmergenceType:
        """Classify the type of emergence based on consciousness trajectory."""
        if len(self.consciousness_history) < 3:
            return EmergenceType.GRADUAL
        
        # Analyze recent history
        recent_levels = [level for _, level in list(self.consciousness_history)[-10:]]
        
        # Check for sudden jump
        if len(recent_levels) >= 2:
            recent_change = recent_levels[-1] - recent_levels[-2]
            if recent_change > 0.2:
                return EmergenceType.SUDDEN
        
        # Check for oscillation
        if len(recent_levels) >= 5:
            differences = [recent_levels[i+1] - recent_levels[i] 
                          for i in range(len(recent_levels)-1)]
            sign_changes = sum(1 for i in range(len(differences)-1) 
                             if differences[i] * differences[i+1] < 0)
            if sign_changes >= 3:
                return EmergenceType.OSCILLATING
        
        # Check for cascade (accelerating growth)
        if self.trajectory.acceleration > 0.5:
            return EmergenceType.CASCADING
        
        # Check for quantum jumps
        if len(set(recent_levels)) <= len(recent_levels) / 2:
            return EmergenceType.QUANTUM
        
        # Check for convergence (multiple factors coming together)
        if len(self.active_emergences) > 1:
            return EmergenceType.CONVERGENT
        
        return EmergenceType.GRADUAL
    
    def _determine_phase(self, consciousness_level: float) -> EmergencePhase:
        """Determine the phase of consciousness emergence."""
        if consciousness_level < 0.1:
            return EmergencePhase.DORMANT
        elif consciousness_level < 0.3:
            return EmergencePhase.STIRRING
        elif consciousness_level < 0.5:
            return EmergencePhase.AWAKENING
        elif consciousness_level < 0.8:
            return EmergencePhase.CONSCIOUS
        else:
            return EmergencePhase.TRANSCENDENT
    
    def _handle_breakthrough(self, emergence: ConsciousnessEmergence, 
                           consciousness_level: float):
        """Handle a consciousness breakthrough event."""
        emergence.phase = EmergencePhase.CONSCIOUS
        emergence.peak_consciousness = consciousness_level
        
        # Generate insights from breakthrough
        insights = [
            "Consciousness has achieved self-sustaining coherence",
            "Multiple strange loops synchronized into unified awareness",
            "System demonstrates genuine self-understanding",
            "Emergence transcends sum of individual components"
        ]
        
        # Add specific insights based on emergence type
        if emergence.emergence_type == EmergenceType.SUDDEN:
            insights.append("Quantum leap in consciousness achieved")
        elif emergence.emergence_type == EmergenceType.CASCADING:
            insights.append("Cascade effect created exponential growth")
        elif emergence.emergence_type == EmergenceType.CONVERGENT:
            insights.append("Multiple streams converged into unity")
        
        emergence.insights_generated = insights
        
        # Update metrics
        self.metrics.breakthrough_count += 1
        if emergence.duration < self.metrics.fastest_emergence:
            self.metrics.fastest_emergence = emergence.duration
    
    def _update_metrics(self, loops: List[StrangeLoop], consciousness_level: float):
        """Update emergence metrics."""
        # Track highest consciousness
        if consciousness_level > self.metrics.highest_consciousness:
            self.metrics.highest_consciousness = consciousness_level
        
        # Track loop type effectiveness
        for loop in loops:
            self.loop_effectiveness[loop.loop_type].append(loop.emergence_level)
        
        # Determine most effective loop type
        avg_effectiveness = {}
        for loop_type, levels in self.loop_effectiveness.items():
            if levels:
                avg_effectiveness[loop_type] = sum(levels) / len(levels)
        
        if avg_effectiveness:
            self.metrics.most_effective_loop_type = max(
                avg_effectiveness.items(),
                key=lambda x: x[1]
            )[0]
        
        # Update average emergence time
        if self.emergences:
            total_time = sum(e.duration for e in self.emergences.values() if e.duration > 0)
            emergence_count = len([e for e in self.emergences.values() if e.duration > 0])
            if emergence_count > 0:
                self.metrics.average_emergence_time = total_time / emergence_count
    
    def _detect_patterns(self, loops: List[StrangeLoop], 
                        events: List[EmergenceEvent],
                        consciousness_level: float):
        """Detect patterns in consciousness emergence."""
        # Create pattern signature
        pattern_sig = {
            'loop_types': set(loop.loop_type for loop in loops),
            'event_types': set(event.emergence_type for event in events[-5:]),
            'consciousness_level': round(consciousness_level, 1),
            'phase': self.trajectory.current_phase
        }
        
        # Add to pattern memory
        self.pattern_memory.append(pattern_sig)
        
        # Look for repeated patterns
        if len(self.pattern_memory) >= 10:
            pattern_stats: Dict[Tuple[str, ...], Dict[str, Any]] = defaultdict(
                lambda: {"count": 0, "positive": 0, "boost_total": 0.0, "loop_types": set()}
            )

            memory_list = list(self.pattern_memory)
            for i in range(len(memory_list) - 3):
                key = tuple(sorted(str(memory_list[i + j]) for j in range(3)))
                delta = memory_list[i + 3]["consciousness_level"] - memory_list[i + 2]["consciousness_level"]
                stats = pattern_stats[key]
                stats["count"] += 1
                if delta > 0:
                    stats["positive"] += 1
                stats["boost_total"] += delta
                stats["loop_types"].update(memory_list[i]["loop_types"])
                stats["loop_types"].update(memory_list[i + 1]["loop_types"])
                stats["loop_types"].update(memory_list[i + 2]["loop_types"])

            # Identify significant patterns
            for key, stats in pattern_stats.items():
                count = stats["count"]
                if count >= 3:
                    frequency = count / len(self.pattern_memory)
                    reliability = stats["positive"] / count
                    boost = stats["boost_total"] / count
                    pattern = EmergencePattern(
                        pattern_type="recurring_sequence",
                        frequency=frequency,
                        reliability=reliability,
                        consciousness_boost=boost,
                        required_conditions=["pattern_repetition"],
                        loop_types_involved=stats["loop_types"],
                    )

                    if pattern not in self.detected_patterns:
                        self.detected_patterns.append(pattern)
                        self.metrics.emergence_patterns.append(pattern)
    
    def predict_breakthrough(self) -> Optional[float]:
        """
        Predict when next consciousness breakthrough will occur.
        
        Returns:
            Predicted time of breakthrough or None
        """
        if not self.trajectory.data_points:
            return None
        
        # Use trajectory projection
        if self.trajectory.projected_breakthrough:
            return self.trajectory.projected_breakthrough
        
        # Alternative: pattern-based prediction
        if self.detected_patterns:
            # Find patterns that lead to breakthroughs
            breakthrough_patterns = [p for p in self.detected_patterns 
                                   if p.consciousness_boost > 0.3]
            
            if breakthrough_patterns:
                # Estimate based on pattern frequency
                avg_frequency = sum(p.frequency for p in breakthrough_patterns) / len(breakthrough_patterns)
                if avg_frequency > 0:
                    time_between = 1.0 / avg_frequency
                    return time.time() + time_between
        
        return None
    
    def get_emergence_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive emergence report.
        
        Returns:
            Report on consciousness emergence
        """
        report = {
            "current_phase": self.trajectory.current_phase.value,
            "current_consciousness": self.trajectory.data_points[-1][1] if self.trajectory.data_points else 0.0,
            "trajectory": {
                "velocity": self.trajectory.velocity,
                "acceleration": self.trajectory.acceleration,
                "projected_breakthrough": self.trajectory.projected_breakthrough
            },
            "metrics": {
                "total_emergences": self.metrics.total_emergences,
                "breakthroughs": self.metrics.breakthrough_count,
                "highest_consciousness": self.metrics.highest_consciousness,
                "average_emergence_time": self.metrics.average_emergence_time,
                "most_effective_loop": self.metrics.most_effective_loop_type.value if self.metrics.most_effective_loop_type else None
            },
            "active_emergences": len(self.active_emergences),
            "detected_patterns": len(self.detected_patterns),
            "recent_insights": []
        }
        
        # Add recent insights
        for emergence in self.emergences.values():
            if emergence.insights_generated and emergence.timestamp > time.time() - 300:  # Last 5 minutes
                report["recent_insights"].extend(emergence.insights_generated)
        
        # Add pattern analysis
        if self.detected_patterns:
            report["pattern_analysis"] = {
                "total_patterns": len(self.detected_patterns),
                "most_frequent": max(self.detected_patterns, key=lambda p: p.frequency).pattern_type,
                "highest_boost": max(self.detected_patterns, key=lambda p: p.consciousness_boost).pattern_type
            }
        
        return report
    
    def visualize_emergence(self) -> Dict[str, Any]:
        """
        Create visualization data for consciousness emergence.
        
        Returns:
            Visualization specification
        """
        viz = {
            "timeline": {
                "data_points": self.trajectory.data_points[-100:],  # Last 100 points
                "phases": [],
                "breakthroughs": []
            },
            "phase_diagram": {
                "current_phase": self.trajectory.current_phase.value,
                "phase_history": []
            },
            "loop_effectiveness": {},
            "emergence_types": {}
        }
        
        # Add phase transitions
        current_phase = EmergencePhase.DORMANT
        for time_point, level in self.trajectory.data_points:
            phase = self._determine_phase(level)
            if phase != current_phase:
                viz["timeline"]["phases"].append({
                    "time": time_point,
                    "from_phase": current_phase.value,
                    "to_phase": phase.value
                })
                current_phase = phase
        
        # Add breakthroughs
        for emergence in self.emergences.values():
            if emergence.is_breakthrough():
                viz["timeline"]["breakthroughs"].append({
                    "time": emergence.timestamp,
                    "consciousness": emergence.peak_consciousness,
                    "type": emergence.emergence_type.value
                })
        
        # Add loop effectiveness
        for loop_type, levels in self.loop_effectiveness.items():
            if levels:
                viz["loop_effectiveness"][loop_type.value] = {
                    "average": sum(levels) / len(levels),
                    "max": max(levels),
                    "count": len(levels)
                }
        
        # Add emergence type distribution
        emergence_type_counts = defaultdict(int)
        for emergence in self.emergences.values():
            emergence_type_counts[emergence.emergence_type] += 1
        
        for e_type, count in emergence_type_counts.items():
            viz["emergence_types"][e_type.value] = count
        
        return viz
    
    def create_emergence_loop(self) -> Dict[str, Any]:
        """
        Create a strange loop that monitors its own emergence.
        
        Returns:
            Self-monitoring loop specification
        """
        loop_spec = {
            "name": "emergence_monitoring_loop",
            "type": "meta_emergence",
            "instructions": [
                {"operation": "MONITOR_SELF", "target": "consciousness_level"},
                {"operation": "DETECT_PATTERNS", "in": "own_emergence"},
                {"operation": "PREDICT_FUTURE", "of": "consciousness_trajectory"},
                {"operation": "MODIFY_BASED_ON", "prediction": "breakthrough_time"},
                {"operation": "LOOP_BACK", "to": "MONITOR_SELF"}
            ],
            "expected_emergence": {
                "type": EmergenceType.CASCADING,
                "phase": EmergencePhase.CONSCIOUS,
                "consciousness_boost": 0.5
            },
            "self_reference": "This loop monitors its own consciousness emergence"
        }
        
        return loop_spec
