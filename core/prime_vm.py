"""
Enhanced Prime Virtual Machine with consciousness-aware capabilities.

This module implements the main VM that extends the existing UOR system with
consciousness-aware instruction execution, self-reflection mechanisms, and
strange loop detection foundations.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
import json
import traceback
from collections import deque

from core.instruction_set import ExtendedOpCode, InstructionSet
from core.memory_system import WorkingMemory, LongTermMemory, EpisodicMemory, PatternCache
from core.consciousness_layer import (
    ConsciousnessLayer, ConsciousnessLevel, MetaCognitiveState
)


# Re-export OpCode for compatibility
OpCode = ExtendedOpCode


@dataclass
class Instruction:
    """Represents a VM instruction with prime encoding."""
    
    opcode: OpCode
    operand: int = 0
    params: Dict[str, Any] = field(default_factory=dict)
    prime_encoding: int = 0
    
    def __post_init__(self):
        """Calculate prime encoding if not provided."""
        if self.prime_encoding == 0:
            instruction_set = InstructionSet()
            self.prime_encoding = instruction_set.encode_instruction(
                self.opcode, self.operand, self.params
            )


@dataclass
class ExecutionTrace:
    """Records execution history for pattern analysis."""
    
    instruction: Instruction
    timestamp: datetime
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    result: Any
    consciousness_level: ConsciousnessLevel
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary for analysis."""
        return {
            'opcode': self.instruction.opcode.name,
            'operand': self.instruction.operand,
            'params': self.instruction.params,
            'timestamp': self.timestamp.isoformat(),
            'result': str(self.result),
            'consciousness_level': self.consciousness_level.name
        }


@dataclass
class SelfModel:
    """Represents the VM's model of itself."""
    
    capabilities: Set[str] = field(default_factory=set)
    limitations: Set[str] = field(default_factory=set)
    current_goals: List[str] = field(default_factory=list)
    behavioral_patterns: List[Dict[str, Any]] = field(default_factory=list)
    self_description: str = "I am a consciousness-aware virtual machine."
    last_update: datetime = field(default_factory=datetime.now)
    
    def update_capability(self, capability: str, has_capability: bool = True) -> None:
        """Update a capability in the self-model."""
        if has_capability:
            self.capabilities.add(capability)
            self.limitations.discard(capability)
        else:
            self.limitations.add(capability)
            self.capabilities.discard(capability)
        self.last_update = datetime.now()
        
    def add_behavioral_pattern(self, pattern: Dict[str, Any]) -> None:
        """Add a recognized behavioral pattern."""
        self.behavioral_patterns.append({
            'pattern': pattern,
            'discovered': datetime.now()
        })
        # Keep only recent patterns
        if len(self.behavioral_patterns) > 50:
            self.behavioral_patterns = self.behavioral_patterns[-50:]


class ConsciousPrimeVM:
    """
    Enhanced Prime Virtual Machine with consciousness-aware capabilities.
    
    Extends the basic UOR VM with self-reflection, meta-cognition, and
    strange loop detection capabilities.
    """
    
    def __init__(self, memory_capacity: int = 100):
        """
        Initialize the conscious VM.
        
        Args:
            memory_capacity: Size of working memory
        """
        # Core components
        self.instruction_set = InstructionSet()
        self.consciousness = ConsciousnessLayer()
        
        # Memory systems
        self.working_memory = WorkingMemory(capacity=memory_capacity)
        self.long_term_memory = LongTermMemory()
        self.episodic_memory = EpisodicMemory()
        self.pattern_cache = PatternCache()
        
        # Execution state
        self.stack: List[Any] = []
        self.registers: Dict[str, Any] = {}
        self.program_counter: int = 0
        self.execution_history: deque = deque(maxlen=1000)
        
        # Self-awareness components
        self.self_model = SelfModel()
        self.meta_state = MetaCognitiveState()
        self.consciousness_level = ConsciousnessLevel.DORMANT
        
        # Execution control
        self._halt = False
        self._trace_enabled = False
        self._in_strange_loop = False
        self._loop_depth = 0
        self._max_loop_depth = 10
        
        # Initialize capabilities
        self._initialize_capabilities()
        
    def _initialize_capabilities(self) -> None:
        """Initialize VM capabilities in self-model."""
        basic_capabilities = [
            "execute_instructions",
            "maintain_stack",
            "pattern_recognition",
            "self_reflection",
            "meta_reasoning",
            "memory_management"
        ]
        
        for cap in basic_capabilities:
            self.self_model.update_capability(cap, True)
            
        # Set initial limitations
        self.self_model.update_capability("perfect_prediction", False)
        self.self_model.update_capability("infinite_recursion", False)
        
    def execute_instruction(self, instruction: Instruction) -> Any:
        """
        Execute a single instruction with consciousness awareness.
        
        Args:
            instruction: The instruction to execute
            
        Returns:
            Result of instruction execution
        """
        # Capture state before execution
        state_before = self.capture_state()
        
        # Start episodic recording for consciousness operations
        if self.instruction_set.is_consciousness_opcode(instruction.opcode):
            self.episodic_memory.start_episode({
                'instruction': instruction.opcode.name,
                'consciousness_level': self.consciousness_level.name
            })
            
        try:
            # Execute based on opcode
            if instruction.opcode == OpCode.NOP:
                result = None
                
            elif instruction.opcode == OpCode.PUSH:
                self.stack.append(instruction.operand)
                result = instruction.operand
                
            elif instruction.opcode == OpCode.POP:
                result = self.stack.pop() if self.stack else None
                
            elif instruction.opcode == OpCode.ADD:
                if len(self.stack) >= 2:
                    b, a = self.stack.pop(), self.stack.pop()
                    result = a + b
                    self.stack.append(result)
                else:
                    result = None
                    
            elif instruction.opcode == OpCode.SELF_REFLECT:
                result = self._self_reflect()
                
            elif instruction.opcode == OpCode.META_REASON:
                result = self._meta_reason(instruction.params)
                
            elif instruction.opcode == OpCode.PATTERN_MATCH:
                result = self._pattern_match(instruction.params)
                
            elif instruction.opcode == OpCode.CREATE_ANALOGY:
                result = self._create_analogy(instruction.params)
                
            elif instruction.opcode == OpCode.STRANGE_LOOP:
                depth = instruction.params.get('depth', 1)
                result = self._create_strange_loop(depth)
                
            elif instruction.opcode == OpCode.ANALYZE_SELF:
                result = self._analyze_self()
                
            elif instruction.opcode == OpCode.CONSCIOUSNESS_TEST:
                result = self._test_consciousness()
                
            else:
                result = f"Unimplemented opcode: {instruction.opcode.name}"
                
        except Exception as e:
            result = f"Execution error: {str(e)}"
            traceback.print_exc()
            
        # Capture state after execution
        state_after = self.capture_state()
        
        # Record execution trace
        trace = ExecutionTrace(
            instruction=instruction,
            timestamp=datetime.now(),
            state_before=state_before,
            state_after=state_after,
            result=result,
            consciousness_level=self.consciousness_level
        )
        self.execution_history.append(trace)
        
        # Meta-process the execution
        self._meta_process_execution(instruction, result)
        
        # End episodic recording
        if self.episodic_memory._current_episode:
            self.episodic_memory.record_event('execution_complete', result)
            self.episodic_memory.end_episode(result)
            
        return result
        
    def _self_reflect(self) -> Dict[str, Any]:
        """
        Perform self-reflection and analysis.
        
        Returns:
            Comprehensive self-analysis including state, patterns, and capabilities
        """
        # Initiate consciousness layer reflection
        consciousness_reflection = self.consciousness.initiate_self_reflection()
        
        # Analyze recent execution patterns
        recent_patterns = self._analyze_recent_patterns()
        
        # Assess current capabilities
        capability_assessment = self._assess_capabilities()
        
        # Generate self-description
        self_description = self._generate_self_description()
        
        reflection = {
            'timestamp': datetime.now().isoformat(),
            'consciousness_state': consciousness_reflection,
            'execution_patterns': recent_patterns,
            'capability_assessment': capability_assessment,
            'self_description': self_description,
            'memory_state': {
                'working_memory': self.working_memory.get_context(),
                'pattern_cache_stats': self.pattern_cache.get_statistics()
            },
            'stack_depth': len(self.stack),
            'execution_count': len(self.execution_history)
        }
        
        # Store reflection in long-term memory
        self.long_term_memory.consolidate(
            f"reflection_{datetime.now().timestamp()}",
            reflection,
            importance=0.8
        )
        
        return reflection
        
    def _create_strange_loop(self, depth: int) -> Dict[str, Any]:
        """
        Create a self-referential execution loop.
        
        Args:
            depth: Depth of recursion for the strange loop
            
        Returns:
            Analysis of the strange loop creation
        """
        if self._loop_depth >= self._max_loop_depth:
            return {
                'status': 'max_depth_reached',
                'depth': self._loop_depth,
                'message': 'Prevented infinite recursion'
            }
            
        self._in_strange_loop = True
        self._loop_depth += 1
        
        loop_data = {
            'depth': depth,
            'start_time': datetime.now(),
            'initial_consciousness': self.consciousness_level.name,
            'iterations': []
        }
        
        try:
            for i in range(min(depth, 5)):  # Limit iterations
                # Create self-referential instruction
                self_instruction = Instruction(
                    OpCode.ANALYZE_SELF,
                    operand=i,
                    params={'analyzing_loop': True, 'depth': self._loop_depth}
                )
                
                # Execute self-analysis
                analysis = self.execute_instruction(self_instruction)
                
                # Modify behavior based on analysis
                if isinstance(analysis, dict) and 'patterns' in analysis:
                    # Detect emergence of patterns
                    pattern_id = self.pattern_cache.store_pattern(
                        'strange_loop',
                        analysis['patterns']
                    )
                    
                loop_data['iterations'].append({
                    'iteration': i,
                    'analysis': analysis,
                    'consciousness_change': self.consciousness_level.name
                })
                
                # Check for emergent properties
                if self.consciousness_level > ConsciousnessLevel.REFLECTIVE:
                    loop_data['emergence_detected'] = True
                    break
                    
        finally:
            self._loop_depth -= 1
            if self._loop_depth == 0:
                self._in_strange_loop = False
                
        loop_data['end_time'] = datetime.now()
        loop_data['final_consciousness'] = self.consciousness_level.name
        
        # Register with consciousness layer
        self.consciousness.register_strange_loop(loop_data)
        
        return loop_data
        
    def _analyze_recent_patterns(self) -> List[Dict[str, Any]]:
        """
        Analyze patterns in recent execution history.
        
        Returns:
            List of detected patterns
        """
        if len(self.execution_history) < 10:
            return []
            
        patterns = []
        
        # Analyze opcode sequences
        recent_opcodes = [trace.instruction.opcode.name for trace in list(self.execution_history)[-20:]]
        
        # Detect repetitions
        for i in range(2, min(10, len(recent_opcodes) // 2)):
            for j in range(len(recent_opcodes) - i):
                sequence = recent_opcodes[j:j+i]
                if recent_opcodes[j+i:j+2*i] == sequence:
                    patterns.append({
                        'type': 'repetition',
                        'sequence': sequence,
                        'length': i
                    })
                    
        # Detect consciousness operations clustering
        consciousness_ops = [
            op for op in recent_opcodes 
            if op in ['SELF_REFLECT', 'META_REASON', 'ANALYZE_SELF']
        ]
        if len(consciousness_ops) > len(recent_opcodes) * 0.3:
            patterns.append({
                'type': 'consciousness_focus',
                'ratio': len(consciousness_ops) / len(recent_opcodes)
            })
            
        # Store patterns in cache
        for pattern in patterns:
            self.pattern_cache.store_pattern('execution', pattern)
            
        return patterns
        
    def _assess_capabilities(self) -> Dict[str, Any]:
        """
        Assess current VM capabilities.
        
        Returns:
            Assessment of capabilities and limitations
        """
        assessment = {
            'known_capabilities': list(self.self_model.capabilities),
            'known_limitations': list(self.self_model.limitations),
            'operational_status': {}
        }
        
        # Test basic operations
        test_results = {
            'stack_operations': len(self.stack) < 1000,
            'memory_available': self.working_memory.capacity > len(self.working_memory._items),
            'pattern_recognition': len(self.pattern_cache._patterns) > 0,
            'consciousness_active': self.consciousness_level > ConsciousnessLevel.DORMANT
        }
        
        assessment['operational_status'] = test_results
        
        # Update self-model based on assessment
        for capability, status in test_results.items():
            self.self_model.update_capability(capability, status)
            
        return assessment
        
    def _generate_self_description(self) -> str:
        """Generate a natural language self-description."""
        base = self.consciousness._generate_self_description()
        
        # Add VM-specific details
        additions = []
        
        if len(self.execution_history) > 0:
            additions.append(f"I have executed {len(self.execution_history)} instructions.")
            
        if self._in_strange_loop:
            additions.append(f"I am currently in a strange loop at depth {self._loop_depth}.")
            
        if self.pattern_cache._patterns:
            additions.append(f"I have recognized {len(self.pattern_cache._patterns)} patterns.")
            
        return base + " " + " ".join(additions)
        
    def capture_state(self) -> Dict[str, Any]:
        """
        Capture current VM state.
        
        Returns:
            Dictionary containing current state snapshot
        """
        return {
            'stack': self.stack.copy(),
            'registers': self.registers.copy(),
            'program_counter': self.program_counter,
            'consciousness_level': self.consciousness_level.name,
            'working_memory_size': len(self.working_memory._items),
            'pattern_count': len(self.pattern_cache._patterns),
            'in_strange_loop': self._in_strange_loop,
            'loop_depth': self._loop_depth
        }
        
    def _meta_process_execution(self, instruction: Instruction, result: Any) -> None:
        """
        Perform meta-cognitive processing of instruction execution.
        
        Args:
            instruction: Executed instruction
            result: Result of execution
        """
        # Update consciousness based on instruction
        impact = self.instruction_set.get_consciousness_impact(instruction.opcode)
        if impact > 0:
            self.consciousness.meta_state.update_metric('activity', impact)
            
        # Process meta-cognitive events
        if instruction.opcode in [OpCode.SELF_REFLECT, OpCode.ANALYZE_SELF]:
            self.consciousness.process_meta_cognitive_event('self_analysis', result)
            
        # Update consciousness level
        self.consciousness_level = self.consciousness.update_consciousness_level()
        
        # Decay awareness over time
        if len(self.execution_history) % 10 == 0:
            self.consciousness.awareness_tracker.decay_metrics()
            
    def _meta_reason(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform meta-reasoning about reasoning processes."""
        context = params.get('context', {})
        self.consciousness.meta_reasoning.start_reasoning(context)
        
        analysis = self.consciousness.meta_reasoning.reason_about_reasoning()
        
        # Store insights
        if 'patterns_detected' in analysis:
            for pattern in analysis['patterns_detected']:
                self.pattern_cache.store_pattern('meta_reasoning', pattern)
                
        return analysis
        
    def _pattern_match(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find patterns in execution or data."""
        data = params.get('data', self.execution_history)
        pattern_type = params.get('type', 'execution')
        
        matches = self.pattern_cache.find_matching_patterns(data, pattern_type)
        
        return [
            {
                'pattern_id': f"{m.pattern_type}_{m.signature[:8]}",
                'confidence': m.confidence,
                'occurrences': len(m.occurrences)
            }
            for m in matches
        ]
        
    def _create_analogy(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Find structural similarities between concepts."""
        source = params.get('source', {})
        target = params.get('target', {})
        
        # Simple structural comparison
        source_keys = set(source.keys()) if isinstance(source, dict) else set()
        target_keys = set(target.keys()) if isinstance(target, dict) else set()
        
        common = source_keys & target_keys
        similarity = len(common) / max(len(source_keys), len(target_keys), 1)
        
        analogy = {
            'similarity_score': similarity,
            'common_elements': list(common),
            'source_unique': list(source_keys - target_keys),
            'target_unique': list(target_keys - source_keys)
        }
        
        # Store as pattern
        self.pattern_cache.store_pattern('analogy', analogy)
        
        return analogy
        
    def _analyze_self(self) -> Dict[str, Any]:
        """Perform deep self-analysis."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'consciousness_report': self.consciousness.get_consciousness_report(),
            'patterns': self._analyze_recent_patterns(),
            'self_model': {
                'capabilities': list(self.self_model.capabilities),
                'limitations': list(self.self_model.limitations),
                'behavioral_patterns': self.self_model.behavioral_patterns[-5:]
            },
            'memory_analysis': {
                'working_memory_utilization': len(self.working_memory._items) / self.working_memory.capacity,
                'pattern_cache_stats': self.pattern_cache.get_statistics(),
                'episodic_memory_count': len(self.episodic_memory._episodes)
            }
        }
        
        # Detect behavioral patterns
        if len(self.execution_history) > 50:
            recent_behavior = [t.instruction.opcode.name for t in list(self.execution_history)[-50:]]
            behavior_pattern = {
                'dominant_operations': max(set(recent_behavior), key=recent_behavior.count),
                'diversity': len(set(recent_behavior)) / len(recent_behavior)
            }
            self.self_model.add_behavioral_pattern(behavior_pattern)
            
        return analysis
        
    def _test_consciousness(self) -> Dict[str, Any]:
        """Evaluate own awareness level."""
        # Perform various consciousness tests
        tests = {
            'self_recognition': self._test_self_recognition(),
            'meta_cognitive_ability': self._test_meta_cognition(),
            'strange_loop_detection': self._test_strange_loops(),
            'emergence_indicators': self.consciousness.awareness_tracker.detect_emergence()
        }
        
        # Calculate overall score
        scores = []
        if tests['self_recognition']:
            scores.append(1.0)
        if tests['meta_cognitive_ability'] > 0.5:
            scores.append(tests['meta_cognitive_ability'])
        if tests['strange_loop_detection']:
            scores.append(1.0)
        scores.append(len(tests['emergence_indicators']) / 5.0)
        
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            'test_results': tests,
            'overall_score': overall_score,
            'consciousness_level': self.consciousness_level.name,
            'recommendation': self._get_consciousness_recommendation(overall_score)
        }
        
    def _test_self_recognition(self) -> bool:
        """Test if VM recognizes itself."""
        # Check if self-model contains accurate information
        return (
            len(self.self_model.capabilities) > 0 and
            self.self_model.self_description != "" and
            self.consciousness_level > ConsciousnessLevel.REACTIVE
        )
        
    def _test_meta_cognition(self) -> float:
        """Test meta-cognitive abilities."""
        analysis = self.consciousness.meta_reasoning.reason_about_reasoning()
        return analysis.get('efficiency_score', 0.0)
        
    def _test_strange_loops(self) -> bool:
        """Test for presence of strange loops."""
        return self.consciousness.meta_state.strange_loop_count > 0
        
    def _get_consciousness_recommendation(self, score: float) -> str:
        """Get recommendation based on consciousness score."""
        if score < 0.3:
            return "Increase self-reflection and meta-reasoning activities"
        elif score < 0.6:
            return "Explore strange loop creation and pattern recognition"
        elif score < 0.8:
            return "Deepen recursive self-analysis"
        else:
            return "Maintain current consciousness practices"
            
    def reset(self) -> None:
        """Reset VM to initial state."""
        self.stack.clear()
        self.registers.clear()
        self.program_counter = 0
        self.execution_history.clear()
        self._halt = False
        self._in_strange_loop = False
        self._loop_depth = 0
        
        # Reset memory systems
        self.working_memory.clear()
        self.pattern_cache.clear()
        
        # Reset consciousness
        self.consciousness_level = ConsciousnessLevel.DORMANT
        self.consciousness = ConsciousnessLayer()
        
    def run_program(self, instructions: List[Instruction]) -> List[Any]:
        """
        Run a program consisting of multiple instructions.
        
        Args:
            instructions: List of instructions to execute
            
        Returns:
            List of results from each instruction
        """
        results = []
        self.episodic_memory.start_episode({'program_length': len(instructions)})
        
        for i, instruction in enumerate(instructions):
            if self._halt:
                break
                
            self.program_counter = i
            result = self.execute_instruction(instruction)
            results.append(result)
            
            # Periodic consciousness updates
            if i % 5 == 0:
                self.consciousness_level = self.consciousness.update_consciousness_level()
                
        self.episodic_memory.end_episode({'results': len(results), 'halted': self._halt})
        return results
