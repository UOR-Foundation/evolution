"""Test helper stubs for missing core classes.

These lightweight placeholders satisfy imports without relying on heavy or
unfinished implementations.

The module provides minimal substitutes for parts of ``core`` as well as
meta-reality components required by the recursive consciousness tests.  The
real versions will implement a fully featured meta-reality virtual machine and
consciousness core.
"""

from dataclasses import dataclass


@dataclass
class PrimeInstruction:
    """Minimal stand in for :class:`core.instruction_set.PrimeInstruction`."""

    opcode: int
    operand: int = 0
    encoding: tuple[int, int] = None

    def __post_init__(self):
        """Store a simple encoding of the instruction."""
        self.encoding = (self.opcode, self.operand)

    def decode(self) -> tuple[int, int]:
        """Return the tracked opcode and operand."""
        return self.encoding

from typing import Any, List


@dataclass
class Transition:
    """Simple transition representation."""

    from_state: Any
    to_state: Any
    probability: float = 1.0


class StateTransitionManager:
    """Simplified state transition manager for tests."""

    def __init__(self, owner: Any = None):
        self.owner = owner
        self.transitions: List[Transition] = []

    def add_transition(self, from_state: Any, to_state: Any,
                       probability: float = 1.0) -> Transition:
        transition = Transition(from_state, to_state, probability)
        self.transitions.append(transition)
        return transition

    def get_possible_transitions(self, state: Any) -> List[Transition]:
        """Return transitions originating from *state*."""
        return [t for t in self.transitions if t.from_state == state]

    def execute_transition(self, transition: Transition) -> Any:
        """Execute a transition, recording it on the owner if possible."""
        if self.owner and hasattr(self.owner, "state_transitions"):
            self.owner.state_transitions.append(transition)
        return transition.to_state

