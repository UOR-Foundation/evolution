"""
Extended instruction set for the Enhanced Prime Virtual Machine.

This module defines all opcodes including consciousness-aware operations
and provides utilities for instruction encoding/decoding.
"""

from enum import IntEnum
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


class ExtendedOpCode(IntEnum):
    """Extended opcodes including original UOR and new consciousness operations."""
    
    # Original UOR opcodes (using first primes)
    NOP = 2              # No operation
    PUSH = 3             # Push value to stack
    POP = 5              # Pop value from stack
    ADD = 7              # Addition
    SUB = 11             # Subtraction
    MUL = 13             # Multiplication
    DIV = 17             # Division
    MOD = 19             # Modulo
    EQ = 23              # Equality check
    LT = 29              # Less than
    GT = 31              # Greater than
    JMP = 37             # Jump
    JZ = 39              # Jump if zero
    
    # New consciousness-aware opcodes
    SELF_REFLECT = 41        # Analyze own current state
    META_REASON = 43         # Reason about reasoning processes
    PATTERN_MATCH = 47       # Find patterns in execution
    CREATE_ANALOGY = 53      # Find structural similarities
    PERSPECTIVE_SHIFT = 59   # Change viewpoint on problem
    CREATIVE_SEARCH = 61     # Generate novel solutions
    CONSCIOUSNESS_TEST = 67  # Evaluate own awareness
    STRANGE_LOOP = 71        # Create self-referential loop
    ANALYZE_SELF = 73        # Deep self-analysis
    MODIFY_SELF_MODEL = 79   # Update self-understanding
    
    # Memory operations
    STORE_PATTERN = 83       # Store recognized pattern
    RECALL_PATTERN = 89      # Recall stored pattern
    CONSOLIDATE_MEMORY = 97  # Consolidate short to long term
    
    # Meta-cognitive operations
    TRACE_EXECUTION = 101    # Enable execution tracing
    ANALYZE_TRACE = 103      # Analyze execution trace
    PREDICT_OUTCOME = 107    # Predict execution outcome
    EVALUATE_STRATEGY = 109  # Evaluate problem-solving strategy


@dataclass
class PrimeInstruction:
    """Lightweight instruction used by legacy modules."""

    opcode: int
    operand: int = 0
    encoding: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        self.encoding = (int(self.opcode), self.operand)

    def decode(self) -> tuple[int, int]:
        return self.encoding


@dataclass
class InstructionMetadata:
    """Metadata for instruction execution and analysis."""
    
    opcode: ExtendedOpCode
    complexity: int  # Computational complexity estimate
    consciousness_impact: float  # Impact on consciousness level (0.0-1.0)
    requires_reflection: bool  # Whether this op triggers self-reflection
    modifies_self: bool  # Whether this op can modify VM state
    description: str


class InstructionSet:
    """Manages the complete instruction set with metadata and utilities."""
    
    def __init__(self):
        """Initialize instruction set with metadata."""
        self._metadata: Dict[ExtendedOpCode, InstructionMetadata] = self._build_metadata()
        self._prime_cache: Dict[int, List[int]] = {}  # Cache for prime factorizations
        
    def _build_metadata(self) -> Dict[ExtendedOpCode, InstructionMetadata]:
        """Build metadata for all instructions."""
        return {
            # Basic operations
            ExtendedOpCode.NOP: InstructionMetadata(
                ExtendedOpCode.NOP, 1, 0.0, False, False,
                "No operation"
            ),
            ExtendedOpCode.PUSH: InstructionMetadata(
                ExtendedOpCode.PUSH, 1, 0.0, False, False,
                "Push value to stack"
            ),
            ExtendedOpCode.ADD: InstructionMetadata(
                ExtendedOpCode.ADD, 1, 0.0, False, False,
                "Add two values"
            ),
            
            # Consciousness operations
            ExtendedOpCode.SELF_REFLECT: InstructionMetadata(
                ExtendedOpCode.SELF_REFLECT, 10, 0.8, True, False,
                "Analyze and report on current internal state"
            ),
            ExtendedOpCode.META_REASON: InstructionMetadata(
                ExtendedOpCode.META_REASON, 15, 0.9, True, True,
                "Reason about reasoning processes"
            ),
            ExtendedOpCode.PATTERN_MATCH: InstructionMetadata(
                ExtendedOpCode.PATTERN_MATCH, 8, 0.5, False, False,
                "Find patterns in execution history"
            ),
            ExtendedOpCode.CREATE_ANALOGY: InstructionMetadata(
                ExtendedOpCode.CREATE_ANALOGY, 12, 0.7, True, False,
                "Find structural similarities between concepts"
            ),
            ExtendedOpCode.PERSPECTIVE_SHIFT: InstructionMetadata(
                ExtendedOpCode.PERSPECTIVE_SHIFT, 10, 0.6, True, True,
                "Change viewpoint on current problem"
            ),
            ExtendedOpCode.CREATIVE_SEARCH: InstructionMetadata(
                ExtendedOpCode.CREATIVE_SEARCH, 20, 0.8, True, False,
                "Generate novel solution approaches"
            ),
            ExtendedOpCode.CONSCIOUSNESS_TEST: InstructionMetadata(
                ExtendedOpCode.CONSCIOUSNESS_TEST, 25, 1.0, True, False,
                "Evaluate own awareness level"
            ),
            ExtendedOpCode.STRANGE_LOOP: InstructionMetadata(
                ExtendedOpCode.STRANGE_LOOP, 30, 1.0, True, True,
                "Create self-referential execution loop"
            ),
            ExtendedOpCode.ANALYZE_SELF: InstructionMetadata(
                ExtendedOpCode.ANALYZE_SELF, 20, 0.9, True, False,
                "Perform deep self-analysis"
            ),
            ExtendedOpCode.MODIFY_SELF_MODEL: InstructionMetadata(
                ExtendedOpCode.MODIFY_SELF_MODEL, 15, 0.8, True, True,
                "Update internal self-model"
            ),
        }
        
    def get_metadata(self, opcode: ExtendedOpCode) -> Optional[InstructionMetadata]:
        """Get metadata for a specific opcode."""
        return self._metadata.get(opcode)
        
    def encode_instruction(self, opcode: ExtendedOpCode, operand: int = 0, 
                          params: Optional[Dict[str, Any]] = None) -> int:
        """
        Encode an instruction as a prime factorization.
        
        Args:
            opcode: The operation code
            operand: Primary operand (default 0)
            params: Additional parameters
            
        Returns:
            Prime factorization encoding of the instruction
        """
        # Basic encoding: opcode^2 * operand_prime^1 * param_encoding
        encoding = opcode.value ** 2
        
        if operand > 0:
            operand_prime = self._nth_prime(operand)
            encoding *= operand_prime
            
        if params:
            # Encode params as product of primes
            param_encoding = self._encode_params(params)
            encoding *= param_encoding
            
        return encoding
        
    def decode_instruction(self, encoding: int) -> tuple[ExtendedOpCode, int, Dict[str, Any]]:
        """
        Decode a prime factorization into an instruction.
        
        Args:
            encoding: Prime factorization encoding
            
        Returns:
            Tuple of (opcode, operand, params)
        """
        factors = self._factorize(encoding)
        
        # Find opcode (appears with power 2)
        opcode = None
        for prime, power in factors.items():
            if power == 2 and prime in [op.value for op in ExtendedOpCode]:
                opcode = ExtendedOpCode(prime)
                break
                
        if not opcode:
            raise ValueError(f"Invalid instruction encoding: {encoding}")
            
        # Extract operand and params
        operand = 0
        params = {}
        
        # Simplified decoding for this implementation
        remaining_factors = {p: pow for p, pow in factors.items() if p != opcode.value}
        if remaining_factors:
            # First remaining prime is operand
            operand_prime = min(remaining_factors.keys())
            operand = self._prime_to_index(operand_prime)
            
        return opcode, operand, params
        
    def _factorize(self, n: int) -> Dict[int, int]:
        """
        Factorize a number into prime factors.
        
        Args:
            n: Number to factorize
            
        Returns:
            Dictionary mapping prime factors to their powers
        """
        if n in self._prime_cache:
            return self._prime_cache[n]
            
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
            
        self._prime_cache[n] = factors
        return factors
        
    def _nth_prime(self, n: int) -> int:
        """Get the nth prime number (1-indexed)."""
        if n <= 0:
            return 1
            
        primes = [2]
        candidate = 3
        
        while len(primes) < n:
            is_prime = True
            for p in primes:
                if p * p > candidate:
                    break
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(candidate)
            candidate += 2
            
        return primes[n - 1]
        
    def _prime_to_index(self, prime: int) -> int:
        """Convert a prime number to its index (1-indexed)."""
        if prime < 2:
            return 0
            
        if prime == 2:
            return 1
            
        count = 1
        candidate = 3
        while candidate < prime:
            is_prime = True
            for d in range(2, int(candidate ** 0.5) + 1):
                if candidate % d == 0:
                    is_prime = False
                    break
            if is_prime:
                count += 1
            candidate += 2
            
        return count
        
    def _encode_params(self, params: Dict[str, Any]) -> int:
        """Encode parameters as a prime product."""
        # Simplified encoding for demonstration
        encoding = 1
        for i, (key, value) in enumerate(params.items()):
            if isinstance(value, int) and value > 0:
                prime = self._nth_prime(i + 10)  # Start from 10th prime for params
                encoding *= prime ** value
        return encoding
        
    def is_consciousness_opcode(self, opcode: ExtendedOpCode) -> bool:
        """Check if an opcode is a consciousness-related operation."""
        consciousness_ops = {
            ExtendedOpCode.SELF_REFLECT,
            ExtendedOpCode.META_REASON,
            ExtendedOpCode.PATTERN_MATCH,
            ExtendedOpCode.CREATE_ANALOGY,
            ExtendedOpCode.PERSPECTIVE_SHIFT,
            ExtendedOpCode.CREATIVE_SEARCH,
            ExtendedOpCode.CONSCIOUSNESS_TEST,
            ExtendedOpCode.STRANGE_LOOP,
            ExtendedOpCode.ANALYZE_SELF,
            ExtendedOpCode.MODIFY_SELF_MODEL
        }
        return opcode in consciousness_ops
        
    def get_consciousness_impact(self, opcode: ExtendedOpCode) -> float:
        """Get the consciousness impact factor for an opcode."""
        metadata = self.get_metadata(opcode)
        return metadata.consciousness_impact if metadata else 0.0
