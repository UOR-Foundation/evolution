"""
Conceptual Blending Engine

This module creates conceptual blends between domains, generating novel concepts
through the integration of multiple input spaces.
"""

from typing import List, Dict, Optional, Set, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

from modules.analogical_reasoning.analogy_engine import Domain, Element, Relation, AnalogicalReasoningEngine


class BlendType(Enum):
    """Types of conceptual blends"""
    COMPOSITION = "composition"
    COMPLETION = "completion"
    ELABORATION = "elaboration"
    EMERGENT = "emergent"


class OperationType(Enum):
    """Types of blending operations"""
    PROJECTION = "projection"
    FUSION = "fusion"
    COMPRESSION = "compression"
    DECOMPRESSION = "decompression"


@dataclass
class ConceptualSpace:
    """A conceptual space that can be blended"""
    id: str
    name: str
    elements: Dict[str, Element]
    relations: Dict[str, Relation]
    organizing_frame: Dict[str, Any]
    vital_relations: List[str]


@dataclass
class GenericSpace:
    """Generic space containing shared structure"""
    shared_elements: Set[str]
    shared_relations: Set[str]
    shared_patterns: List[str]
    abstraction_level: float


@dataclass
class CrossSpaceMapping:
    """Mapping between elements across spaces"""
    source_space: str
    target_space: str
    element_mappings: Dict[str, str]
    relation_mappings: Dict[str, str]
    mapping_strength: float


@dataclass
class Operation:
    """A blending operation"""
    type: OperationType
    source_elements: List[str]
    result_element: str
    parameters: Dict[str, Any]


@dataclass
class Pattern:
    """A pattern in the blend space"""
    id: str
    pattern_type: str
    elements_involved: List[str]
    description: str
    strength: float


@dataclass
class Structure:
    """A structure in the blend space"""
    id: str
    structure_type: str
    components: List[str]
    relations: List[str]
    coherence: float


@dataclass
class Mechanism:
    """An emergence mechanism"""
    id: str
    mechanism_type: str
    input_conditions: List[str]
    output_effects: List[str]
    probability: float


@dataclass
class BlendSpace:
    """The blended conceptual space"""
    projected_elements: List[Element]
    emergent_elements: List[Element]
    composition_operations: List[Operation]
    completion_patterns: List[Pattern]
    elaboration_structures: List[Structure]


@dataclass
class EmergentStructure:
    """Emergent structure in the blend"""
    novel_elements: List[Element]
    novel_relations: List[Relation]
    novel_patterns: List[Pattern]
    emergence_mechanisms: List[Mechanism]
    creativity_score: float


@dataclass
class ConceptualBlend:
    """A complete conceptual blend"""
    input_spaces: List[ConceptualSpace]
    generic_space: GenericSpace
    blend_space: BlendSpace
    cross_space_mappings: List[CrossSpaceMapping]
    emergent_structure: EmergentStructure
    blend_coherence: float


@dataclass
class OptimizedBlend:
    """An optimized conceptual blend"""
    base_blend: ConceptualBlend
    optimization_steps: List[Dict[str, Any]]
    final_coherence: float
    optimization_metrics: Dict[str, float]


@dataclass
class ViabilityAssessment:
    """Assessment of blend viability"""
    structural_integrity: float
    conceptual_coherence: float
    pragmatic_utility: float
    creative_value: float
    overall_viability: float
    issues: List[str]


@dataclass
class SimulationResult:
    """Result of blend simulation"""
    blend_id: str
    simulation_steps: List[Dict[str, Any]]
    emergent_behaviors: List[str]
    stability_score: float
    insights_generated: List[str]


class ConceptualBlendingEngine:
    """
    Engine for creating conceptual blends between domains, generating novel
    concepts through the integration of multiple input spaces.
    """
    
    def __init__(self, analogical_engine: AnalogicalReasoningEngine):
        self.analogical_engine = analogical_engine
        self.blend_cache: Dict[str, ConceptualBlend] = {}
        self.successful_blends: List[ConceptualBlend] = []
        
    def create_conceptual_blend(self, input_spaces: List[ConceptualSpace]) -> ConceptualBlend:
        """Create a conceptual blend from multiple input spaces"""
        if len(input_spaces) < 2:
            raise ValueError("Need at least 2 input spaces for blending")
        
        # Extract generic space
        generic_space = self._extract_generic_space(input_spaces)
        
        # Create cross-space mappings
        cross_space_mappings = self._create_cross_space_mappings(input_spaces)
        
        # Create initial blend space
        blend_space = self._create_blend_space(
            input_spaces, generic_space, cross_space_mappings
        )
        
        # Generate emergent structure
        emergent_structure = self.generate_emergent_structure(blend_space, input_spaces)
        
        # Calculate blend coherence
        blend_coherence = self._calculate_blend_coherence(
            blend_space, emergent_structure, cross_space_mappings
        )
        
        blend = ConceptualBlend(
            input_spaces=input_spaces,
            generic_space=generic_space,
            blend_space=blend_space,
            cross_space_mappings=cross_space_mappings,
            emergent_structure=emergent_structure,
            blend_coherence=blend_coherence
        )
        
        # Cache successful blends
        if blend_coherence > 0.7:
            self.successful_blends.append(blend)
            blend_id = f"blend_{len(self.blend_cache)}"
            self.blend_cache[blend_id] = blend
        
        return blend
    
    def optimize_blend_structure(self, blend: ConceptualBlend) -> OptimizedBlend:
        """Optimize a blend for coherence and creativity"""
        optimization_steps = []
        current_blend = blend
        
        # Optimization strategies
        strategies = [
            self._optimize_projections,
            self._optimize_emergent_elements,
            self._optimize_vital_relations,
            self._optimize_completion_patterns
        ]
        
        for strategy in strategies:
            step_result = strategy(current_blend)
            if step_result['improvement'] > 0:
                optimization_steps.append(step_result)
                current_blend = step_result['new_blend']
        
        # Calculate final metrics
        optimization_metrics = {
            'coherence_improvement': current_blend.blend_coherence - blend.blend_coherence,
            'creativity_improvement': self._calculate_creativity_delta(blend, current_blend),
            'stability': self._calculate_blend_stability(current_blend),
            'integration': self._calculate_integration_score(current_blend)
        }
        
        return OptimizedBlend(
            base_blend=current_blend,
            optimization_steps=optimization_steps,
            final_coherence=current_blend.blend_coherence,
            optimization_metrics=optimization_metrics
        )
    
    def evaluate_blend_viability(self, blend: ConceptualBlend) -> ViabilityAssessment:
        """Evaluate the viability of a conceptual blend"""
        issues = []
        
        # Structural integrity
        structural_integrity = self._assess_structural_integrity(blend)
        if structural_integrity < 0.5:
            issues.append("Low structural integrity - blend may be unstable")
        
        # Conceptual coherence
        conceptual_coherence = self._assess_conceptual_coherence(blend)
        if conceptual_coherence < 0.5:
            issues.append("Low conceptual coherence - blend lacks unity")
        
        # Pragmatic utility
        pragmatic_utility = self._assess_pragmatic_utility(blend)
        if pragmatic_utility < 0.3:
            issues.append("Low pragmatic utility - blend may not be useful")
        
        # Creative value
        creative_value = self._assess_creative_value(blend)
        
        # Overall viability
        overall_viability = (
            structural_integrity * 0.3 +
            conceptual_coherence * 0.3 +
            pragmatic_utility * 0.2 +
            creative_value * 0.2
        )
        
        return ViabilityAssessment(
            structural_integrity=structural_integrity,
            conceptual_coherence=conceptual_coherence,
            pragmatic_utility=pragmatic_utility,
            creative_value=creative_value,
            overall_viability=overall_viability,
            issues=issues
        )
    
    def generate_emergent_structure(self, blend_space: BlendSpace, 
                                  input_spaces: List[ConceptualSpace]) -> EmergentStructure:
        """Generate emergent structure in the blend"""
        # Identify novel elements
        novel_elements = self._identify_novel_elements(blend_space, input_spaces)
        
        # Identify novel relations
        novel_relations = self._identify_novel_relations(blend_space, input_spaces)
        
        # Identify novel patterns
        novel_patterns = self._identify_novel_patterns(blend_space)
        
        # Identify emergence mechanisms
        emergence_mechanisms = self._identify_emergence_mechanisms(
            novel_elements, novel_relations, novel_patterns
        )
        
        # Calculate creativity score
        creativity_score = self._calculate_creativity_score(
            novel_elements, novel_relations, novel_patterns
        )
        
        return EmergentStructure(
            novel_elements=novel_elements,
            novel_relations=novel_relations,
            novel_patterns=novel_patterns,
            emergence_mechanisms=emergence_mechanisms,
            creativity_score=creativity_score
        )
    
    def run_blend_simulation(self, blend: ConceptualBlend) -> SimulationResult:
        """Run a simulation of the blend to test its behavior"""
        simulation_steps = []
        emergent_behaviors = []
        
        # Initialize simulation state
        state = self._initialize_simulation_state(blend)
        
        # Run simulation steps
        for step in range(100):  # 100 simulation steps
            # Apply blend operations
            new_state = self._apply_blend_operations(state, blend)
            
            # Check for emergent behaviors
            behaviors = self._detect_emergent_behaviors(state, new_state)
            emergent_behaviors.extend(behaviors)
            
            # Record step
            simulation_steps.append({
                'step': step,
                'state': new_state,
                'behaviors': behaviors
            })
            
            state = new_state
            
            # Check for stability
            if self._is_stable_state(state):
                break
        
        # Generate insights from simulation
        insights = self._extract_simulation_insights(simulation_steps, emergent_behaviors)
        
        # Calculate stability score
        stability_score = self._calculate_stability_score(simulation_steps)
        
        return SimulationResult(
            blend_id=f"sim_{id(blend)}",
            simulation_steps=simulation_steps,
            emergent_behaviors=emergent_behaviors,
            stability_score=stability_score,
            insights_generated=insights
        )
    
    def _extract_generic_space(self, input_spaces: List[ConceptualSpace]) -> GenericSpace:
        """Extract the generic space from input spaces"""
        # Find shared elements
        shared_elements = set(input_spaces[0].elements.keys())
        for space in input_spaces[1:]:
            shared_elements &= set(space.elements.keys())
        
        # Find shared relations
        shared_relations = set(input_spaces[0].relations.keys())
        for space in input_spaces[1:]:
            shared_relations &= set(space.relations.keys())
        
        # Extract shared patterns
        shared_patterns = self._extract_shared_patterns(input_spaces)
        
        # Calculate abstraction level
        abstraction_level = self._calculate_abstraction_level(
            shared_elements, shared_relations, shared_patterns
        )
        
        return GenericSpace(
            shared_elements=shared_elements,
            shared_relations=shared_relations,
            shared_patterns=shared_patterns,
            abstraction_level=abstraction_level
        )
    
    def _create_cross_space_mappings(self, 
                                   input_spaces: List[ConceptualSpace]) -> List[CrossSpaceMapping]:
        """Create mappings between input spaces"""
        mappings = []
        
        # Create pairwise mappings
        for i in range(len(input_spaces)):
            for j in range(i + 1, len(input_spaces)):
                source_space = input_spaces[i]
                target_space = input_spaces[j]
                
                # Use analogical engine to find mappings
                domain_source = self._space_to_domain(source_space)
                domain_target = self._space_to_domain(target_space)
                
                structural_mapping = self.analogical_engine.create_structural_mapping(
                    domain_source, domain_target
                )
                
                mapping = CrossSpaceMapping(
                    source_space=source_space.id,
                    target_space=target_space.id,
                    element_mappings=structural_mapping.element_correspondences,
                    relation_mappings=structural_mapping.relation_correspondences,
                    mapping_strength=structural_mapping.mapping_confidence
                )
                
                mappings.append(mapping)
        
        return mappings
    
    def _create_blend_space(self, input_spaces: List[ConceptualSpace],
                          generic_space: GenericSpace,
                          mappings: List[CrossSpaceMapping]) -> BlendSpace:
        """Create the initial blend space"""
        # Project elements from input spaces
        projected_elements = self._project_elements(input_spaces, mappings)
        
        # Create composition operations
        composition_operations = self._create_composition_operations(
            projected_elements, mappings
        )
        
        # Create completion patterns
        completion_patterns = self._create_completion_patterns(
            projected_elements, generic_space
        )
        
        # Create elaboration structures
        elaboration_structures = self._create_elaboration_structures(
            projected_elements, composition_operations
        )
        
        # Initially no emergent elements
        emergent_elements = []
        
        return BlendSpace(
            projected_elements=projected_elements,
            emergent_elements=emergent_elements,
            composition_operations=composition_operations,
            completion_patterns=completion_patterns,
            elaboration_structures=elaboration_structures
        )
    
    def _calculate_blend_coherence(self, blend_space: BlendSpace,
                                 emergent_structure: EmergentStructure,
                                 mappings: List[CrossSpaceMapping]) -> float:
        """Calculate overall coherence of the blend"""
        # Integration coherence
        integration = self._calculate_integration_coherence(blend_space, mappings)
        
        # Topology coherence
        topology = self._calculate_topology_coherence(blend_space)
        
        # Pattern coherence
        pattern = self._calculate_pattern_coherence(
            blend_space.completion_patterns,
            emergent_structure.novel_patterns
        )
        
        # Vital relations coherence
        vital = self._calculate_vital_relations_coherence(blend_space)
        
        # Combine coherence measures
        coherence = (
            integration * 0.3 +
            topology * 0.3 +
            pattern * 0.2 +
            vital * 0.2
        )
        
        return min(coherence, 1.0)
    
    def _identify_novel_elements(self, blend_space: BlendSpace,
                               input_spaces: List[ConceptualSpace]) -> List[Element]:
        """Identify novel elements that emerge in the blend"""
        novel_elements = []
        
        # Elements created through composition
        for operation in blend_space.composition_operations:
            if operation.type == OperationType.FUSION:
                # Create fused element
                fused = self._create_fused_element(
                    operation.source_elements,
                    blend_space.projected_elements
                )
                if fused and self._is_novel_element(fused, input_spaces):
                    novel_elements.append(fused)
        
        # Elements created through completion
        for pattern in blend_space.completion_patterns:
            completed = self._complete_pattern_element(pattern, blend_space)
            if completed and self._is_novel_element(completed, input_spaces):
                novel_elements.append(completed)
        
        # Elements created through elaboration
        for structure in blend_space.elaboration_structures:
            elaborated = self._elaborate_structure_element(structure, blend_space)
            if elaborated and self._is_novel_element(elaborated, input_spaces):
                novel_elements.append(elaborated)
        
        return novel_elements
    
    def _identify_novel_relations(self, blend_space: BlendSpace,
                                input_spaces: List[ConceptualSpace]) -> List[Relation]:
        """Identify novel relations that emerge in the blend"""
        novel_relations = []
        
        # Relations from compressed vital relations
        compressed = self._compress_vital_relations(blend_space, input_spaces)
        novel_relations.extend(compressed)
        
        # Relations from pattern completion
        for pattern in blend_space.completion_patterns:
            relations = self._complete_pattern_relations(pattern, blend_space)
            for rel in relations:
                if self._is_novel_relation(rel, input_spaces):
                    novel_relations.append(rel)
        
        # Relations from emergent structure
        emergent = self._identify_emergent_relations(blend_space)
        novel_relations.extend(emergent)
        
        return novel_relations
    
    def _identify_novel_patterns(self, blend_space: BlendSpace) -> List[Pattern]:
        """Identify novel patterns in the blend"""
        novel_patterns = []
        
        # Patterns from element interactions
        interaction_patterns = self._find_interaction_patterns(blend_space)
        novel_patterns.extend(interaction_patterns)
        
        # Patterns from structural regularities
        structural_patterns = self._find_structural_patterns(blend_space)
        novel_patterns.extend(structural_patterns)
        
        # Patterns from dynamic behaviors
        if hasattr(blend_space, 'dynamic_behaviors'):
            dynamic_patterns = self._find_dynamic_patterns(blend_space)
            novel_patterns.extend(dynamic_patterns)
        
        return novel_patterns
    
    def _calculate_creativity_score(self, novel_elements: List[Element],
                                  novel_relations: List[Relation],
                                  novel_patterns: List[Pattern]) -> float:
        """Calculate creativity score of emergent structure"""
        # Novelty component
        novelty = (
            len(novel_elements) * 0.3 +
            len(novel_relations) * 0.3 +
            len(novel_patterns) * 0.4
        ) / 10.0  # Normalize
        
        # Surprise component
        surprise = self._calculate_surprise_factor(
            novel_elements, novel_relations, novel_patterns
        )
        
        # Value component
        value = self._calculate_emergent_value(
            novel_elements, novel_relations, novel_patterns
        )
        
        # Combine components
        creativity = (novelty * 0.4 + surprise * 0.3 + value * 0.3)
        
        return min(creativity, 1.0)
    
    def _space_to_domain(self, space: ConceptualSpace) -> Domain:
        """Convert a conceptual space to a domain for analogical mapping"""
        return Domain(
            name=space.name,
            elements=space.elements,
            relations=space.relations,
            constraints=list(space.organizing_frame.get('constraints', [])),
            goals=list(space.organizing_frame.get('goals', []))
        )
    
    def _is_novel_element(self, element: Element, 
                         input_spaces: List[ConceptualSpace]) -> bool:
        """Check if an element is novel (not in any input space)"""
        for space in input_spaces:
            if element.id in space.elements:
                return False
            # Check for similar elements
            for existing in space.elements.values():
                if self._elements_are_similar(element, existing):
                    return False
        return True
    
    def _elements_are_similar(self, elem1: Element, elem2: Element) -> bool:
        """Check if two elements are similar"""
        # Type check
        if elem1.type != elem2.type:
            return False
        
        # Property overlap
        common_props = set(elem1.properties.keys()) & set(elem2.properties.keys())
        if len(common_props) / len(set(elem1.properties.keys()) | set(elem2.properties.keys())) > 0.8:
            return True
        
        return False
