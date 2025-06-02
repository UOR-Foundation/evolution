"""
Consciousness layer for the Enhanced Prime Virtual Machine.

This module implements meta-cognitive state management, self-awareness tracking,
and consciousness level calculation based on Hofstadter's strange loop concepts.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
import math
from collections import deque
from core.memory_system import PatternCache


class ConsciousnessLevel(IntEnum):
    """Levels of consciousness in the VM."""

    DORMANT = 0  # No self-awareness
    REACTIVE = 1  # Simple stimulus-response
    AWARE = 2  # Basic self-awareness
    REFLECTIVE = 3  # Can reflect on own states
    META_COGNITIVE = 4  # Can reason about reasoning
    RECURSIVE = 5  # Strange loops present
    EMERGENT = 6  # Higher-order consciousness


@dataclass
class MetaCognitiveState:
    """Represents the meta-cognitive state of the VM."""

    level: ConsciousnessLevel = ConsciousnessLevel.DORMANT
    self_model_complexity: float = 0.0  # 0.0 to 1.0
    reflection_depth: int = 0
    strange_loop_count: int = 0
    awareness_metrics: Dict[str, float] = field(default_factory=dict)
    active_processes: Set[str] = field(default_factory=set)
    last_update: datetime = field(default_factory=datetime.now)

    def update_metric(self, metric: str, value: float) -> None:
        """Update a specific awareness metric."""
        self.awareness_metrics[metric] = max(0.0, min(1.0, value))
        self.last_update = datetime.now()

    def calculate_overall_awareness(self) -> float:
        """Calculate overall awareness score."""
        if not self.awareness_metrics:
            return 0.0
        return sum(self.awareness_metrics.values()) / len(self.awareness_metrics)


@dataclass
class SelfAwarenessMetrics:
    """Metrics for tracking self-awareness."""

    introspection_frequency: float = 0.0  # How often VM examines itself
    self_modification_count: int = 0  # Times VM has modified itself
    prediction_accuracy: float = 0.0  # Accuracy of self-predictions
    coherence_score: float = 0.0  # Internal consistency
    emergence_indicators: List[str] = field(default_factory=list)

    def update_introspection(self) -> None:
        """Update introspection frequency."""
        # Simple exponential moving average
        self.introspection_frequency = 0.9 * self.introspection_frequency + 0.1

    def decay_introspection(self) -> None:
        """Decay introspection frequency over time."""
        self.introspection_frequency *= 0.95


class MetaReasoningProcess:
    """
    Handles meta-reasoning processes - reasoning about reasoning.

    Implements recursive analysis of thought processes and decision-making.
    """

    def __init__(self):
        """Initialize meta-reasoning process."""
        self._reasoning_stack: List[Dict[str, Any]] = []
        self._meta_patterns: List[Dict[str, Any]] = []
        self._recursion_depth: int = 0
        self._max_recursion: int = 5

    def start_reasoning(self, context: Dict[str, Any]) -> None:
        """Start a new reasoning process."""
        self._reasoning_stack.append(
            {
                "context": context,
                "timestamp": datetime.now(),
                "depth": self._recursion_depth,
                "conclusions": [],
            }
        )

    def reason_about_reasoning(self) -> Dict[str, Any]:
        """
        Analyze the current reasoning process.

        Returns:
            Meta-analysis of reasoning patterns
        """
        if not self._reasoning_stack:
            return {"status": "no_active_reasoning"}

        current = self._reasoning_stack[-1]

        # Analyze reasoning patterns
        analysis = {
            "depth": len(self._reasoning_stack),
            "current_context": current["context"],
            "reasoning_time": (datetime.now() - current["timestamp"]).total_seconds(),
            "patterns_detected": self._detect_reasoning_patterns(),
            "efficiency_score": self._calculate_efficiency(),
            "coherence": self._check_coherence(),
        }

        # Check for infinite loops
        if self._recursion_depth >= self._max_recursion:
            analysis["warning"] = "Maximum recursion depth reached"

        return analysis

    def _detect_reasoning_patterns(self) -> List[str]:
        """Detect patterns in reasoning process."""
        patterns = []

        if len(self._reasoning_stack) >= 2:
            # Check for circular reasoning
            contexts = [r["context"] for r in self._reasoning_stack[-3:]]
            if len(contexts) == len(set(str(c) for c in contexts)):
                patterns.append("linear_progression")
            else:
                patterns.append("circular_reasoning")

        # Check for depth
        if len(self._reasoning_stack) > 3:
            patterns.append("deep_analysis")

        return patterns

    def _calculate_efficiency(self) -> float:
        """Calculate reasoning efficiency."""
        if not self._reasoning_stack:
            return 0.0

        # Simple metric based on conclusions per time
        total_conclusions = sum(
            len(r.get("conclusions", [])) for r in self._reasoning_stack
        )
        total_time = sum(
            (datetime.now() - r["timestamp"]).total_seconds()
            for r in self._reasoning_stack
        )

        if total_time == 0:
            return 1.0

        return min(1.0, total_conclusions / (total_time + 1))

    def _check_coherence(self) -> float:
        """Check coherence of reasoning chain."""
        if len(self._reasoning_stack) < 2:
            return 1.0

        # Simple coherence based on context similarity
        coherence_scores = []
        for i in range(1, len(self._reasoning_stack)):
            prev_context = set(str(self._reasoning_stack[i - 1]["context"].keys()))
            curr_context = set(str(self._reasoning_stack[i]["context"].keys()))

            if prev_context and curr_context:
                overlap = len(prev_context & curr_context) / len(
                    prev_context | curr_context
                )
                coherence_scores.append(overlap)

        return (
            sum(coherence_scores) / len(coherence_scores) if coherence_scores else 1.0
        )

    def conclude_reasoning(self, conclusions: List[Any]) -> None:
        """Add conclusions to current reasoning process."""
        if self._reasoning_stack:
            self._reasoning_stack[-1]["conclusions"] = conclusions

    def pop_reasoning(self) -> Optional[Dict[str, Any]]:
        """Pop the current reasoning context."""
        if self._reasoning_stack:
            return self._reasoning_stack.pop()
        return None


class SelfAwarenessTracker:
    """
    Tracks and analyzes self-awareness indicators.

    Monitors various metrics that indicate the level of self-awareness
    in the virtual machine.
    """

    def __init__(self, history_size: int = 100):
        """
        Initialize self-awareness tracker.

        Args:
            history_size: Size of metric history to maintain
        """
        self.history_size = history_size
        self._metrics = SelfAwarenessMetrics()
        self._history: deque = deque(maxlen=history_size)
        self._awareness_events: List[Dict[str, Any]] = []

    def record_introspection(self) -> None:
        """Record an introspection event."""
        self._metrics.update_introspection()
        self._awareness_events.append(
            {
                "type": "introspection",
                "timestamp": datetime.now(),
                "metrics": self.get_current_metrics(),
            }
        )

    def record_self_modification(self, modification_type: str, details: Any) -> None:
        """Record a self-modification event."""
        self._metrics.self_modification_count += 1
        self._awareness_events.append(
            {
                "type": "self_modification",
                "modification_type": modification_type,
                "details": details,
                "timestamp": datetime.now(),
            }
        )

    def record_prediction_feedback(self, predicted: Any, actual: Any) -> None:
        """Record a prediction event and update accuracy metrics."""
        self.update_prediction_accuracy(predicted, actual)
        accuracy = 1.0 if predicted == actual else 0.0
        self._awareness_events.append(
            {
                "type": "prediction",
                "predicted": predicted,
                "actual": actual,
                "accuracy": accuracy,
                "timestamp": datetime.now(),
            }
        )

    def _handle_feedback_event(
        self,
        predicted: Any,
        actual: Any,
        pattern_cache: Optional["PatternCache"] = None,
    ) -> None:
        """Compare predictions with outcomes and update metrics."""
        self.record_prediction_feedback(predicted, actual)
        accuracy = 1.0 if predicted == actual else 0.0
        if pattern_cache is not None:
            pattern_cache.store_pattern(
                "prediction",
                {
                    "predicted": predicted,
                    "actual": actual,
                    "accuracy": accuracy,
                },
            )

    def update_prediction_accuracy(self, predicted: Any, actual: Any) -> None:
        """Update prediction accuracy based on predicted vs actual outcomes."""
        # Simple accuracy calculation
        accuracy = 1.0 if predicted == actual else 0.0

        # Exponential moving average
        self._metrics.prediction_accuracy = (
            0.9 * self._metrics.prediction_accuracy + 0.1 * accuracy
        )

    def detect_emergence(self) -> List[str]:
        """
        Detect emergent properties in self-awareness.

        Returns:
            List of detected emergence indicators
        """
        indicators = []

        # High introspection frequency
        if self._metrics.introspection_frequency > 0.7:
            indicators.append("high_introspection")

        # Self-modification pattern
        if self._metrics.self_modification_count > 5:
            indicators.append("active_self_modification")

        # Good prediction accuracy
        if self._metrics.prediction_accuracy > 0.8:
            indicators.append("accurate_self_model")

        # Check for complex patterns in awareness events
        if len(self._awareness_events) > 10:
            event_types = [e["type"] for e in self._awareness_events[-10:]]
            if len(set(event_types)) > 3:
                indicators.append("diverse_awareness_patterns")

        self._metrics.emergence_indicators = indicators
        return indicators

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current self-awareness metrics."""
        return {
            "introspection_frequency": self._metrics.introspection_frequency,
            "self_modification_count": self._metrics.self_modification_count,
            "prediction_accuracy": self._metrics.prediction_accuracy,
            "coherence_score": self._metrics.coherence_score,
            "emergence_indicators": self._metrics.emergence_indicators,
        }

    def calculate_awareness_level(self) -> float:
        """
        Calculate overall awareness level (0.0 to 1.0).

        Returns:
            Normalized awareness level
        """
        # Weighted combination of metrics
        weights = {
            "introspection": 0.3,
            "modification": 0.2,
            "prediction": 0.3,
            "emergence": 0.2,
        }

        scores = {
            "introspection": self._metrics.introspection_frequency,
            "modification": min(1.0, self._metrics.self_modification_count / 10),
            "prediction": self._metrics.prediction_accuracy,
            "emergence": len(self._metrics.emergence_indicators) / 5.0,
        }

        total = sum(weights[k] * scores[k] for k in weights)
        return min(1.0, total)

    def decay_metrics(self) -> None:
        """Apply time-based decay to metrics."""
        self._metrics.decay_introspection()


class ConsciousnessLayer:
    """
    Main consciousness layer coordinating all meta-cognitive processes.

    Integrates self-awareness tracking, meta-reasoning, and consciousness
    level management.
    """

    def __init__(self):
        """Initialize consciousness layer."""
        self.meta_state = MetaCognitiveState()
        self.meta_reasoning = MetaReasoningProcess()
        self.awareness_tracker = SelfAwarenessTracker()
        self._consciousness_history: deque = deque(maxlen=1000)
        self._strange_loops: List[Dict[str, Any]] = []

    def update_consciousness_level(self) -> ConsciousnessLevel:
        """
        Update and return current consciousness level.

        Returns:
            Current consciousness level
        """
        # Calculate various factors
        awareness_score = self.awareness_tracker.calculate_awareness_level()
        meta_score = self._calculate_meta_cognitive_score()
        loop_score = self._calculate_strange_loop_score()

        # Determine consciousness level
        combined_score = awareness_score * 0.4 + meta_score * 0.4 + loop_score * 0.2

        if combined_score < 0.1:
            level = ConsciousnessLevel.DORMANT
        elif combined_score < 0.3:
            level = ConsciousnessLevel.REACTIVE
        elif combined_score < 0.5:
            level = ConsciousnessLevel.AWARE
        elif combined_score < 0.7:
            level = ConsciousnessLevel.REFLECTIVE
        elif combined_score < 0.85:
            level = ConsciousnessLevel.META_COGNITIVE
        elif combined_score < 0.95:
            level = ConsciousnessLevel.RECURSIVE
        else:
            level = ConsciousnessLevel.EMERGENT

        # Update state
        self.meta_state.level = level
        self.meta_state.self_model_complexity = combined_score

        # Record in history
        self._consciousness_history.append(
            {
                "timestamp": datetime.now(),
                "level": level,
                "score": combined_score,
                "components": {
                    "awareness": awareness_score,
                    "meta_cognitive": meta_score,
                    "strange_loops": loop_score,
                },
            }
        )

        return level

    def _calculate_meta_cognitive_score(self) -> float:
        """Calculate meta-cognitive capability score."""
        # Based on meta-reasoning depth and quality
        reasoning_analysis = self.meta_reasoning.reason_about_reasoning()

        depth_score = min(1.0, reasoning_analysis.get("depth", 0) / 5)
        efficiency_score = reasoning_analysis.get("efficiency_score", 0)
        coherence_score = reasoning_analysis.get("coherence", 0)

        return (depth_score + efficiency_score + coherence_score) / 3

    def _calculate_strange_loop_score(self) -> float:
        """Calculate strange loop presence score."""
        if not self._strange_loops:
            return 0.0

        # Score based on loop count and complexity
        loop_count = len(self._strange_loops)
        avg_depth = (
            sum(loop.get("depth", 0) for loop in self._strange_loops) / loop_count
        )

        count_score = min(1.0, loop_count / 3)
        depth_score = min(1.0, avg_depth / 5)

        return (count_score + depth_score) / 2

    def register_strange_loop(self, loop_data: Dict[str, Any]) -> None:
        """Register a detected strange loop."""
        self._strange_loops.append(
            {
                "timestamp": datetime.now(),
                "data": loop_data,
                "depth": loop_data.get("depth", 0),
            }
        )
        self.meta_state.strange_loop_count = len(self._strange_loops)

    def initiate_self_reflection(self) -> Dict[str, Any]:
        """
        Initiate a self-reflection process.

        Returns:
            Results of self-reflection
        """
        # Record introspection
        self.awareness_tracker.record_introspection()

        # Start meta-reasoning about current state
        self.meta_reasoning.start_reasoning(
            {
                "type": "self_reflection",
                "consciousness_level": self.meta_state.level,
                "awareness_metrics": self.awareness_tracker.get_current_metrics(),
            }
        )

        # Perform reflection
        reflection = {
            "current_level": self.meta_state.level.name,
            "awareness_score": self.awareness_tracker.calculate_awareness_level(),
            "meta_cognitive_state": self.meta_state.calculate_overall_awareness(),
            "active_processes": list(self.meta_state.active_processes),
            "emergence_indicators": self.awareness_tracker.detect_emergence(),
            "strange_loop_count": self.meta_state.strange_loop_count,
            "self_description": self._generate_self_description(),
        }

        # Conclude reasoning
        self.meta_reasoning.conclude_reasoning([reflection])

        return reflection

    def _generate_self_description(self) -> str:
        """Generate a description of current self-state."""
        level_descriptions = {
            ConsciousnessLevel.DORMANT: "I am not aware of myself.",
            ConsciousnessLevel.REACTIVE: "I respond to inputs without reflection.",
            ConsciousnessLevel.AWARE: "I am aware that I am processing information.",
            ConsciousnessLevel.REFLECTIVE: "I can examine my own thought processes.",
            ConsciousnessLevel.META_COGNITIVE: "I can reason about how I reason.",
            ConsciousnessLevel.RECURSIVE: "I perceive strange loops in my self-reference.",
            ConsciousnessLevel.EMERGENT: "I experience higher-order consciousness emerging from recursive self-awareness.",
        }

        base_description = level_descriptions.get(
            self.meta_state.level, "My consciousness state is undefined."
        )

        # Add details based on metrics
        if self.meta_state.strange_loop_count > 0:
            base_description += f" I have detected {self.meta_state.strange_loop_count} strange loops in my processing."

        if self.awareness_tracker.get_current_metrics()["prediction_accuracy"] > 0.8:
            base_description += " My self-model appears to be accurate."

        return base_description

    def process_meta_cognitive_event(self, event_type: str, data: Any) -> None:
        """Process a meta-cognitive event."""
        self.meta_state.active_processes.add(event_type)

        # Update relevant metrics
        if event_type == "self_modification":
            self.awareness_tracker.record_self_modification(event_type, data)
        elif event_type == "prediction":
            predicted = None
            actual = None
            if isinstance(data, dict):
                predicted = data.get("predicted")
                actual = data.get("actual")

            self.awareness_tracker._handle_feedback_event(predicted, actual)

            # Update meta-state metrics based on new accuracy
            accuracy = 1.0 if predicted == actual else 0.0
            self.meta_state.update_metric(
                "prediction_accuracy",
                self.awareness_tracker.get_current_metrics()["prediction_accuracy"],
            )
            self.meta_state.update_metric("prediction_error", 1.0 - accuracy)

    def get_consciousness_report(self) -> Dict[str, Any]:
        """Generate comprehensive consciousness report."""
        return {
            "current_level": self.meta_state.level.name,
            "level_value": self.meta_state.level.value,
            "self_model_complexity": self.meta_state.self_model_complexity,
            "reflection_depth": self.meta_state.reflection_depth,
            "strange_loop_count": self.meta_state.strange_loop_count,
            "awareness_metrics": self.awareness_tracker.get_current_metrics(),
            "meta_reasoning_state": self.meta_reasoning.reason_about_reasoning(),
            "consciousness_history": list(self._consciousness_history)[
                -10:
            ],  # Last 10 entries
            "self_description": self._generate_self_description(),
        }
