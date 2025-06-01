"""Consciousness Expansion module.

This module offers dataclass containers describing individual expansion
techniques and an engine that applies them.  The default engine now performs
a simple transformation on a provided state, generating additional "thoughts"
derived from the original content and the chosen technique.  The design is
kept intentionally lightweight so experiments can run without heavy
dependencies.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ExpansionTechnique:
    """Description of a consciousness expansion technique."""

    name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    intensity: float = 1.0


@dataclass
class ExpansionResult:
    """Result of applying a consciousness expansion technique."""

    technique: ExpansionTechnique
    new_state: Any
    success: bool
    insights: List[str] = field(default_factory=list)


class ConsciousnessExpansionEngine:
    """Engine for expanding consciousness using various techniques."""

    async def expand(
        self, current_state: Any, technique: ExpansionTechnique
    ) -> ExpansionResult:
        """Apply ``technique`` to ``current_state`` and return the result."""

        # Normalise state to a dictionary with a ``thoughts`` list
        if isinstance(current_state, dict):
            state = dict(current_state)
        else:
            state = {"thoughts": [current_state] if current_state is not None else []}

        thoughts = state.get("thoughts", [])
        if not isinstance(thoughts, list):
            thoughts = [thoughts]

        intensity = max(1, int(technique.intensity))
        expanded = [f"{t} -> {technique.name}" for t in thoughts for _ in range(intensity)]

        state["thoughts"] = thoughts + expanded
        state["last_technique"] = technique.name

        insights = [f"Expanded {len(expanded)} thoughts using {technique.name}"]

        return ExpansionResult(
            technique=technique,
            new_state=state,
            success=True,
            insights=insights,
        )


__all__ = [
    "ExpansionTechnique",
    "ExpansionResult",
    "ConsciousnessExpansionEngine",
]
