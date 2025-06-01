from dataclasses import dataclass
from typing import Any, List

@dataclass
class Transition:
    """Simple transition representation."""
    from_state: Any
    to_state: Any
    probability: float = 1.0


class StateTransitionManager:
    """Manage and execute state transitions for consciousness components."""

    def __init__(self, owner: Any | None = None) -> None:
        self.owner = owner
        self.transitions: List[Transition] = []

    def add_transition(self, from_state: Any, to_state: Any, probability: float = 1.0) -> Transition:
        transition = Transition(from_state, to_state, probability)
        self.transitions.append(transition)
        return transition

    def get_possible_transitions(self, state: Any) -> List[Transition]:
        return [t for t in self.transitions if t.from_state == state]

    def execute_transition(self, transition: Transition) -> Any:
        if self.owner and hasattr(self.owner, "state_transitions"):
            self.owner.state_transitions.append(transition)
        return transition.to_state
