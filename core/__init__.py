"""
Core UOR Evolution Components

This package contains the core components of the UOR Evolution system:
- PrimeOS Virtual Machine
- Consciousness Layer
- Instruction Set
- Memory Systems
"""

from .prime_vm import ConsciousPrimeVM
from .consciousness_layer import ConsciousnessLayer
from .instruction_set import InstructionSet, ExtendedOpCode
from .memory_system import WorkingMemory, LongTermMemory, EpisodicMemory

__all__ = [
    'ConsciousPrimeVM',
    'ConsciousnessLayer', 
    'InstructionSet',
    'ExtendedOpCode',
    'WorkingMemory',
    'LongTermMemory',
    'EpisodicMemory'
]
