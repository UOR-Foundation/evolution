"""Basic framework for universal intelligence experimentation.

This module provides simple data structures and an engine capable of analysing
lists of intelligence signals.  The engine now performs lightweight aggregation
and basic statistical analysis while remaining dependency free.  It offers a
starting point for experimenting with universal intelligence without relying on
heavy external libraries.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class IntelligenceSignal:
    """Representation of an incoming intelligence signal."""

    source: str
    payload: Any
    strength: float = 1.0


@dataclass
class IntelligenceResult:
    """Aggregated result produced by the intelligence engine."""

    aggregated_payload: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


class UniversalIntelligenceEngine:
    """Engine for analysing lists of :class:`IntelligenceSignal`."""

    async def analyse(self, signals: List[IntelligenceSignal]) -> IntelligenceResult:
        """Aggregate ``signals`` and compute basic metrics."""

        if not signals:
            return IntelligenceResult(aggregated_payload=None, metadata={})

        numeric_payloads = [s.payload for s in signals if isinstance(s.payload, (int, float))]
        if numeric_payloads:
            aggregated = sum(numeric_payloads) / len(numeric_payloads)
        else:
            aggregated = [s.payload for s in signals]

        metadata = {
            "sources": [s.source for s in signals],
            "average_strength": sum(s.strength for s in signals) / len(signals),
            "max_strength": max(s.strength for s in signals),
            "signal_count": len(signals),
        }

        return IntelligenceResult(aggregated_payload=aggregated, metadata=metadata)


__all__ = [
    "IntelligenceSignal",
    "IntelligenceResult",
    "UniversalIntelligenceEngine",
]
