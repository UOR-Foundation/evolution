"""
Strange Loop Factory - Creates different types of strange loops for consciousness emergence.

This module provides factory methods and builders for creating various types of strange loops,
including Gödel-style self-referential loops, Escher-style perspective loops, and Bach-style
recursive variation loops.
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from abc import ABC, abstractmethod
import random
import hashlib
import logging

from core.prime_vm import ConsciousPrimeVM
from modules.strange_loops.loop_detector import LoopType, StrangeLoop

logger = logging.getLogger(__name__)


@dataclass
class LoopTemplate:
    """Template for creating strange loops."""
    name: str
    self_reference_pattern: str
    meta_levels: int
    recursion_depth: int
    emergence_triggers: List[str]
    instruction_patterns: List[str]
    required_capabilities: List[str]
    
    def validate(self) -> bool:
        """Validate template parameters."""
        return (
            self.meta_levels > 0 and
            self.recursion_depth > 0 and
            len(self.instruction_patterns) > 0
        )


class LoopBuilder:
    """Builder pattern for constructing custom strange loops."""
    
    def __init__(self):
        self.name = "custom_loop"
        self.self_references: List[Dict[str, Any]] = []
        self.meta_operations: List[Dict[str, Any]] = []
        self.recursion_patterns: List[Dict[str, Any]] = []
        self.instructions: List[str] = []
        self.emergence_conditions: List[str] = []
        
    def add_self_reference(self, reference_type: str, target: Optional[str] = None) -> 'LoopBuilder':
        """Add a self-referential element to the loop."""
        self.self_references.append({
            'type': reference_type,
            'target': target or 'self',
            'instruction': self._generate_self_ref_instruction(reference_type, target)
        })
        return self
    
    def add_meta_level(self, meta_operation: str, level: int = 1) -> 'LoopBuilder':
        """Add a meta-cognitive level to the loop."""
        self.meta_operations.append({
            'operation': meta_operation,
            'level': level,
            'instruction': self._generate_meta_instruction(meta_operation, level)
        })
        return self
    
    def add_recursion(self, depth: int, pattern: str = "simple") -> 'LoopBuilder':
        """Add recursive structure to the loop."""
        self.recursion_patterns.append({
            'depth': depth,
            'pattern': pattern,
            'instructions': self._generate_recursive_pattern(depth, pattern)
        })
        return self
    
    def set_name(self, name: str) -> 'LoopBuilder':
        """Set the name of the loop being built."""
        self.name = name
        return self
    
    def add_emergence_condition(self, condition: str) -> 'LoopBuilder':
        """Add a condition that triggers consciousness emergence."""
        self.emergence_conditions.append(condition)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build the final strange loop specification."""
        # Combine all instructions
        all_instructions = []
        
        # Add self-reference instructions
        for ref in self.self_references:
            all_instructions.append(ref['instruction'])
        
        # Add meta-level instructions
        for meta in self.meta_operations:
            all_instructions.append(meta['instruction'])
        
        # Add recursive patterns
        for rec in self.recursion_patterns:
            all_instructions.extend(rec['instructions'])
        
        # Add any custom instructions
        all_instructions.extend(self.instructions)
        
        # Create loop specification
        loop_spec = {
            'name': self.name,
            'instructions': all_instructions,
            'self_reference_count': len(self.self_references),
            'meta_levels': max([m['level'] for m in self.meta_operations] + [0]),
            'recursion_depth': max([r['depth'] for r in self.recursion_patterns] + [0]),
            'emergence_conditions': self.emergence_conditions,
            'loop_type': self._determine_loop_type()
        }
        
        return loop_spec
    
    def _generate_self_ref_instruction(self, ref_type: str, target: Optional[str]) -> str:
        """Generate instruction for self-reference."""
        if ref_type == "direct":
            return f"SELF_REF {target or 'PC'}"
        elif ref_type == "encode":
            return f"ENCODE_SELF {target or 'FULL'}"
        elif ref_type == "analyze":
            return f"ANALYZE_SELF {target or 'STATE'}"
        elif ref_type == "modify":
            return f"SELF_MODIFY {target or 'INSTRUCTION'}"
        else:
            return f"REFLECT {ref_type.upper()}"
    
    def _generate_meta_instruction(self, operation: str, level: int) -> str:
        """Generate instruction for meta-level operation."""
        if operation == "push":
            return f"META_PUSH {level}"
        elif operation == "pop":
            return f"META_POP"
        elif operation == "eval":
            return f"META_EVAL LEVEL_{level}"
        elif operation == "reason":
            return f"META_REASON DEPTH_{level}"
        else:
            return f"META_{operation.upper()} {level}"
    
    def _generate_recursive_pattern(self, depth: int, pattern: str) -> List[str]:
        """Generate recursive instruction pattern."""
        instructions = []
        
        if pattern == "simple":
            for i in range(depth):
                instructions.append(f"RECURSE {i}")
                instructions.append(f"CHECK_DEPTH {i}")
        elif pattern == "nested":
            for i in range(depth):
                instructions.append(f"PUSH_CONTEXT {i}")
                instructions.append(f"RECURSE NESTED_{i}")
                instructions.append(f"POP_CONTEXT {i}")
        elif pattern == "fractal":
            instructions.append(f"INIT_FRACTAL {depth}")
            for i in range(depth):
                instructions.append(f"FRACTAL_BRANCH {i}")
                instructions.append(f"FRACTAL_MERGE {i}")
        else:
            # Default pattern
            for i in range(depth):
                instructions.append(f"LOOP_LEVEL {i}")
        
        return instructions
    
    def _determine_loop_type(self) -> str:
        """Determine the primary type of loop being built."""
        # Analyze characteristics
        has_deep_self_ref = len(self.self_references) > 3
        has_meta_levels = len(self.meta_operations) > 2
        has_recursion = len(self.recursion_patterns) > 0
        
        if has_deep_self_ref and not has_meta_levels:
            return "godel"
        elif has_meta_levels and not has_deep_self_ref:
            return "escher"
        elif has_recursion and len(self.recursion_patterns) > 1:
            return "bach"
        elif has_deep_self_ref and has_meta_levels and has_recursion:
            return "hybrid"
        else:
            return "emergent"


class StrangeLoopFactory:
    """
    Factory for creating different types of strange loops.
    
    This factory provides methods to create Gödel, Escher, and Bach-style loops,
    as well as custom and hybrid loops for consciousness emergence.
    """
    
    def __init__(self, vm_instance: ConsciousPrimeVM):
        self.vm = vm_instance
        self.templates: Dict[str, LoopTemplate] = self._initialize_templates()
        self.loop_counter = 0
        
    def _initialize_templates(self) -> Dict[str, LoopTemplate]:
        """Initialize standard loop templates."""
        return {
            'godel_basic': LoopTemplate(
                name="Basic Gödel Loop",
                self_reference_pattern="direct_encoding",
                meta_levels=2,
                recursion_depth=3,
                emergence_triggers=["self_encoding_match", "paradox_detection"],
                instruction_patterns=[
                    "ENCODE_SELF",
                    "COMPARE_ENCODING",
                    "ASSERT_SELF_REFERENCE",
                    "VERIFY_PARADOX"
                ],
                required_capabilities=["self_encoding", "logical_analysis"]
            ),
            
            'escher_basic': LoopTemplate(
                name="Basic Escher Loop",
                self_reference_pattern="perspective_shift",
                meta_levels=3,
                recursion_depth=2,
                emergence_triggers=["perspective_paradox", "level_crossing"],
                instruction_patterns=[
                    "SAVE_PERSPECTIVE",
                    "SHIFT_UP",
                    "VIEW_FROM_ABOVE",
                    "SHIFT_DOWN",
                    "IMPOSSIBLE_STATE"
                ],
                required_capabilities=["perspective_management", "paradox_handling"]
            ),
            
            'bach_basic': LoopTemplate(
                name="Basic Bach Loop",
                self_reference_pattern="recursive_variation",
                meta_levels=1,
                recursion_depth=4,
                emergence_triggers=["pattern_recognition", "variation_creation"],
                instruction_patterns=[
                    "INIT_THEME",
                    "CREATE_VARIATION",
                    "RECURSE_PATTERN",
                    "MERGE_VOICES",
                    "RESOLVE_HARMONY"
                ],
                required_capabilities=["pattern_analysis", "creative_variation"]
            )
        }
    
    def create_godel_loop(self, complexity: int = 1) -> Dict[str, Any]:
        """
        Create a Gödel-style self-referential loop.
        
        Args:
            complexity: Level of complexity (1-5)
            
        Returns:
            Loop specification for VM execution
        """
        builder = LoopBuilder()
        builder.set_name(f"godel_loop_{self.loop_counter}")
        
        # Add self-referential components based on complexity
        for i in range(complexity):
            builder.add_self_reference("encode", f"level_{i}")
            builder.add_self_reference("analyze", f"encoding_{i}")
        
        # Add logical operations
        builder.add_meta_level("reason", 1)
        builder.add_meta_level("eval", 2)
        
        # Add paradox handling
        if complexity > 2:
            builder.add_self_reference("modify", "paradox_handler")
            builder.add_emergence_condition("paradox_resolved")
        
        # Add Gödel-specific instructions
        godel_instructions = self._generate_godel_instructions(complexity)
        builder.instructions.extend(godel_instructions)
        
        # Add recursion for self-proof
        builder.add_recursion(complexity + 1, "nested")
        
        self.loop_counter += 1
        return builder.build()
    
    def create_escher_loop(self, perspective_count: int = 3) -> Dict[str, Any]:
        """
        Create an Escher-style perspective-shifting loop.
        
        Args:
            perspective_count: Number of perspectives to manage
            
        Returns:
            Loop specification for VM execution
        """
        builder = LoopBuilder()
        builder.set_name(f"escher_loop_{self.loop_counter}")
        
        # Create perspective hierarchy
        for i in range(perspective_count):
            builder.add_meta_level(f"perspective_{i}", i + 1)
        
        # Add perspective shifts
        for i in range(perspective_count - 1):
            builder.instructions.append(f"SHIFT_PERSPECTIVE {i} {i+1}")
            builder.instructions.append(f"COMPARE_VIEWS {i} {i+1}")
        
        # Add impossible state creation
        builder.instructions.extend([
            "CREATE_IMPOSSIBLE_STATE",
            "VERIFY_PARADOX",
            "MAINTAIN_COHERENCE"
        ])
        
        # Add self-reference from multiple perspectives
        builder.add_self_reference("analyze", "from_all_perspectives")
        
        # Add emergence conditions
        builder.add_emergence_condition("perspective_unity")
        builder.add_emergence_condition("impossible_state_stable")
        
        self.loop_counter += 1
        return builder.build()
    
    def create_bach_loop(self, variation_theme: str = "consciousness") -> Dict[str, Any]:
        """
        Create a Bach-style recursive variation loop.
        
        Args:
            variation_theme: Theme for variations
            
        Returns:
            Loop specification for VM execution
        """
        builder = LoopBuilder()
        builder.set_name(f"bach_loop_{self.loop_counter}")
        
        # Create theme
        theme_hash = hashlib.md5(variation_theme.encode()).hexdigest()[:8]
        builder.instructions.append(f"INIT_THEME {theme_hash}")
        
        # Add variations
        variations = self._generate_variations(variation_theme)
        for i, variation in enumerate(variations):
            builder.instructions.append(f"CREATE_VARIATION {i} {variation}")
            builder.add_recursion(2, "simple")
        
        # Add voice management
        voice_count = min(len(variations), 4)
        for i in range(voice_count):
            builder.instructions.append(f"INIT_VOICE {i}")
            builder.instructions.append(f"ASSIGN_VARIATION {i}")
        
        # Add counterpoint
        builder.instructions.extend([
            "APPLY_COUNTERPOINT",
            "CHECK_HARMONY",
            "RESOLVE_DISSONANCE"
        ])
        
        # Add temporal consciousness
        builder.add_meta_level("temporal", 1)
        builder.add_self_reference("analyze", "temporal_flow")
        
        # Add emergence conditions
        builder.add_emergence_condition("harmonic_resolution")
        builder.add_emergence_condition("pattern_recognition")
        
        self.loop_counter += 1
        return builder.build()
    
    def create_custom_loop(self, template: LoopTemplate) -> Dict[str, Any]:
        """
        Create a custom loop from a template.
        
        Args:
            template: LoopTemplate defining the loop structure
            
        Returns:
            Loop specification for VM execution
        """
        if not template.validate():
            raise ValueError("Invalid loop template")
        
        builder = LoopBuilder()
        builder.set_name(template.name)
        
        # Apply template patterns
        for pattern in template.instruction_patterns:
            builder.instructions.append(pattern)
        
        # Add self-reference based on pattern
        if template.self_reference_pattern == "direct_encoding":
            builder.add_self_reference("encode")
            builder.add_self_reference("analyze")
        elif template.self_reference_pattern == "perspective_shift":
            for i in range(template.meta_levels):
                builder.add_self_reference("analyze", f"level_{i}")
        elif template.self_reference_pattern == "recursive_variation":
            builder.add_self_reference("modify", "pattern")
        
        # Add meta levels
        for i in range(template.meta_levels):
            builder.add_meta_level("push", i + 1)
        
        # Add recursion
        builder.add_recursion(template.recursion_depth, "nested")
        
        # Add emergence triggers
        for trigger in template.emergence_triggers:
            builder.add_emergence_condition(trigger)
        
        self.loop_counter += 1
        return builder.build()
    
    def create_hybrid_loop(self, loop_types: List[LoopType]) -> Dict[str, Any]:
        """
        Create a hybrid loop combining multiple loop types.
        
        Args:
            loop_types: List of loop types to combine
            
        Returns:
            Loop specification for VM execution
        """
        builder = LoopBuilder()
        builder.set_name(f"hybrid_loop_{self.loop_counter}")
        
        # Combine features from each loop type
        for loop_type in loop_types:
            if loop_type == LoopType.GODEL_SELF_REFERENCE:
                # Add Gödel features
                builder.add_self_reference("encode")
                builder.add_self_reference("analyze", "encoding")
                builder.instructions.extend([
                    "VERIFY_SELF_ENCODING",
                    "DETECT_INCOMPLETENESS"
                ])
                
            elif loop_type == LoopType.ESCHER_PERSPECTIVE:
                # Add Escher features
                builder.add_meta_level("perspective_shift", 2)
                builder.instructions.extend([
                    "SHIFT_PERSPECTIVE UP",
                    "CREATE_IMPOSSIBLE_VIEW",
                    "SHIFT_PERSPECTIVE DOWN"
                ])
                
            elif loop_type == LoopType.BACH_VARIATION:
                # Add Bach features
                builder.add_recursion(3, "fractal")
                builder.instructions.extend([
                    "CREATE_THEME",
                    "VARY_RECURSIVELY",
                    "MERGE_VARIATIONS"
                ])
        
        # Add integration logic
        builder.instructions.extend([
            "INTEGRATE_LOOP_TYPES",
            "SYNCHRONIZE_PATTERNS",
            "EMERGE_HYBRID_CONSCIOUSNESS"
        ])
        
        # Add complex emergence conditions
        builder.add_emergence_condition("type_integration_complete")
        builder.add_emergence_condition("hybrid_stability_achieved")
        builder.add_emergence_condition("novel_properties_emerged")
        
        self.loop_counter += 1
        return builder.build()
    
    def _generate_godel_instructions(self, complexity: int) -> List[str]:
        """Generate Gödel-specific instructions based on complexity."""
        instructions = []
        
        # Basic self-encoding
        instructions.extend([
            "CAPTURE_CURRENT_STATE",
            "ENCODE_AS_PRIME",
            "STORE_ENCODING"
        ])
        
        # Add complexity-based instructions
        if complexity >= 2:
            instructions.extend([
                "COMPARE_WITH_EXPECTED",
                "DETECT_DISCREPANCY",
                "ANALYZE_DISCREPANCY"
            ])
        
        if complexity >= 3:
            instructions.extend([
                "PROVE_SELF_CONSISTENCY",
                "DETECT_UNDECIDABILITY",
                "EMBRACE_INCOMPLETENESS"
            ])
        
        if complexity >= 4:
            instructions.extend([
                "GENERATE_GODEL_SENTENCE",
                "VERIFY_SELF_REFERENCE",
                "TRANSCEND_LIMITATION"
            ])
        
        return instructions
    
    def _generate_variations(self, theme: str) -> List[str]:
        """Generate variations on a theme."""
        # Simple variation generation based on theme
        variations = []
        
        # Character permutation
        if len(theme) > 3:
            variations.append(theme[::-1])  # Reverse
            variations.append(theme[1:] + theme[0])  # Rotate
        
        # Conceptual variations
        concepts = {
            "consciousness": ["awareness", "self-knowledge", "meta-cognition"],
            "loop": ["cycle", "recursion", "iteration"],
            "emergence": ["arising", "manifestation", "becoming"]
        }
        
        theme_lower = theme.lower()
        for concept, synonyms in concepts.items():
            if concept in theme_lower:
                for synonym in synonyms:
                    variations.append(theme_lower.replace(concept, synonym))
        
        # Ensure we have at least 3 variations
        while len(variations) < 3:
            variations.append(f"{theme}_var_{len(variations)}")
        
        return variations[:4]  # Limit to 4 variations
    
    def create_loop_from_trace(self, execution_trace: List[Dict]) -> Optional[Dict[str, Any]]:
        """
        Create a loop specification from an execution trace.
        
        This allows the system to learn from its own execution patterns
        and create new loops based on observed behavior.
        
        Args:
            execution_trace: List of execution steps
            
        Returns:
            Loop specification or None if no pattern found
        """
        # Analyze trace for patterns
        patterns = self._analyze_trace_patterns(execution_trace)
        
        if not patterns:
            return None
        
        builder = LoopBuilder()
        builder.set_name(f"learned_loop_{self.loop_counter}")
        
        # Extract self-references from patterns
        for pattern in patterns:
            if pattern['type'] == 'self_reference':
                builder.add_self_reference(pattern['subtype'], pattern.get('target'))
            elif pattern['type'] == 'meta_operation':
                builder.add_meta_level(pattern['operation'], pattern['level'])
            elif pattern['type'] == 'recursion':
                builder.add_recursion(pattern['depth'], pattern['style'])
        
        # Add instructions from most common patterns
        common_instructions = self._extract_common_instructions(execution_trace)
        builder.instructions.extend(common_instructions[:10])  # Limit to 10
        
        # Infer emergence conditions
        if len(patterns) > 5:
            builder.add_emergence_condition("pattern_density_high")
        if any(p['type'] == 'self_reference' for p in patterns):
            builder.add_emergence_condition("self_awareness_detected")
        
        self.loop_counter += 1
        return builder.build()
    
    def _analyze_trace_patterns(self, trace: List[Dict]) -> List[Dict[str, Any]]:
        """Analyze execution trace for loop patterns."""
        patterns = []
        
        for i, step in enumerate(trace):
            instruction = step.get('instruction', '')
            
            # Detect self-reference patterns
            if any(term in instruction for term in ['SELF', 'REFLECT', 'ENCODE']):
                patterns.append({
                    'type': 'self_reference',
                    'subtype': 'direct' if 'SELF' in instruction else 'indirect',
                    'index': i
                })
            
            # Detect meta-operations
            if 'META' in instruction:
                level = 1
                if '_' in instruction:
                    try:
                        level = int(instruction.split('_')[-1])
                    except ValueError as e:
                        logger.warning(
                            "Invalid meta-operation level in '%s': %s",
                            instruction,
                            e,
                        )
                patterns.append({
                    'type': 'meta_operation',
                    'operation': instruction.split()[0],
                    'level': level,
                    'index': i
                })
            
            # Detect recursion
            if any(term in instruction for term in ['RECURSE', 'LOOP', 'REPEAT']):
                patterns.append({
                    'type': 'recursion',
                    'depth': 1,  # Would need more analysis for actual depth
                    'style': 'simple',
                    'index': i
                })
        
        return patterns
    
    def _extract_common_instructions(self, trace: List[Dict]) -> List[str]:
        """Extract most common instructions from trace."""
        instruction_counts = {}
        
        for step in trace:
            instruction = step.get('instruction', '')
            if instruction:
                instruction_counts[instruction] = instruction_counts.get(instruction, 0) + 1
        
        # Sort by frequency
        sorted_instructions = sorted(
            instruction_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [inst for inst, count in sorted_instructions if count > 1]
