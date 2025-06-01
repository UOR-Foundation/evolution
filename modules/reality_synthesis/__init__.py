"""Basic tools for modelling and simulating a simple reality.

This module defines lightweight dataclass containers along with a small
physics-inspired engine for advancing a simulation.  Objects may contain
``position`` and ``velocity`` fields and will be updated each tick using a
simple Euler integration step with optional noise.  The engine remains
dependency free while providing behaviour that is more realistic than the
previous stub implementation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
import random


@dataclass
class RealityModel:
    """Representation of the current simulated reality state."""

    objects: Dict[str, Any] = field(default_factory=dict)
    tick: int = 0


@dataclass
class SimulationParameters:
    """Parameters controlling a single simulation step."""

    time_delta: float = 1.0
    randomness: float = 0.0
    user_input: Dict[str, Any] = field(default_factory=dict)


class RealitySynthesisEngine:
    """Utility for creating models and advancing their state."""

    def create_model(self) -> RealityModel:
        """Return a new, empty :class:`RealityModel`."""

        return RealityModel()

    def simulate_step(self, model: RealityModel, params: SimulationParameters) -> RealityModel:
        """Advance ``model`` using ``params`` and return it.

        Objects containing ``position`` and ``velocity`` fields will have their
        position updated according to ``velocity * time_delta``.  Random noise
        can be injected via ``params.randomness`` to introduce stochasticity.
        Any ``user_input`` is merged into ``model.objects``.
        """

        model.tick += 1
        dt = params.time_delta
        for name, state in model.objects.items():
            if isinstance(state, dict) and "position" in state and "velocity" in state:
                noise = random.gauss(0.0, params.randomness) if params.randomness else 0.0
                state["position"] = state.get("position", 0.0) + state.get("velocity", 0.0) * dt + noise

        if params.user_input:
            for key, value in params.user_input.items():
                model.objects[key] = value

        return model


__all__ = [
    "RealityModel",
    "SimulationParameters",
    "RealitySynthesisEngine",
]
