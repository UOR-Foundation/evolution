"""
Core UOR Evolution Components

This package contains the core components of the UOR Evolution system:
- PrimeOS Virtual Machine
- Consciousness Layer
- Instruction Set
- Memory Systems
"""

from core.prime_vm import ConsciousPrimeVM
from core.consciousness_layer import ConsciousnessLayer
from core.instruction_set import InstructionSet, ExtendedOpCode
from core.memory_system import WorkingMemory, LongTermMemory, EpisodicMemory

__all__ = [
    'ConsciousPrimeVM',
    'ConsciousnessLayer', 
    'InstructionSet',
    'ExtendedOpCode',
    'WorkingMemory',
    'LongTermMemory',
    'EpisodicMemory'
]
