"""
Structure Mapper

This module handles the mapping of structural elements between domains,
including partial mappings, conflict resolution, and multi-level mappings.
"""

from typing import List, Dict, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import defaultdict

from modules.analogical_reasoning.analogy_engine import Element, Relation, Domain, StructuralMapping


class ConflictType(Enum):
    """Types of mapping conflicts"""
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    CIRCULAR = "circular"
    TYPE_MISMATCH = "type_mismatch"
    CONSTRAINT_VIOLATION = "constraint_violation"


class MappingLevel(Enum):
    """Levels of structural mapping"""
    SURFACE = "surface"
    STRUCTURAL = "structural"
    SYSTEM = "system"
    PRAGMATIC = "pragmatic"


@dataclass
class MappingStep:
    """A single step in the mapping optimization process"""
    action: str
    element_mapped: Optional[str]
    relation_mapped: Optional[str]
    score_delta: float
    timestamp: float


@dataclass
class Resolution:
    """Resolution for a mapping conflict"""
    conflict_id: str
    resolution_type: str
    chosen_mapping: Dict[str, str]
    confidence: float
    rationale: str


@dataclass
class PartialMapping:
    """A partial mapping between structures"""
    mapped_elements: Dict[str, str]
    mapped_relations: Dict[str, str]
    unmapped_source: Set[str]
    unmapped_target: Set[str]
    coverage: float
    confidence: float


@dataclass
class OptimalMapping:
    """An optimized structural mapping"""
    element_mappings: Dict[str, str]
    relation_mappings: Dict[str, str]
    mapping_score: float
    optimization_path: List[MappingStep]
    confidence_intervals: Dict[str, Tuple[float, float]]


@dataclass
class MappingConflict:
    """A conflict in the mapping process"""
    conflict_type: ConflictType
    conflicting_elements: List[str]
    possible_resolutions: List[Resolution]
    severity: float


@dataclass
class SurfaceMapping:
    """Surface-level mapping based on labels and properties"""
    label_mappings: Dict[str, str]
    property_mappings: Dict[str, str]
    similarity_scores: Dict[str, float]


@dataclass
class SystemMapping:
    """System-level mapping of higher-order patterns"""
    pattern_mappings: Dict[str, str]
    goal_mappings: Dict[str, str]
    constraint_mappings: Dict[str, str]


@dataclass
class MultiLevelMapping:
    """Multi-level structural mapping"""
    surface_level: SurfaceMapping
    structural_level: StructuralMapping
    system_level: SystemMapping
    cross_level_constraints: List[Dict[str, Any]]


class StructureMapper:
    """
    Maps structural elements between domains, handling partial mappings,
    conflicts, and multi-level correspondences.
    """
    
    def __init__(self, similarity_detector: Optional[Any] = None):
        self.similarity_detector = similarity_detector
        self.mapping_history: List[OptimalMapping] = []
        self.conflict_resolutions: List[Resolution] = []
        
    def create_optimal_mapping(self, source: Domain, target: Domain) -> OptimalMapping:
        """Create an optimal mapping between source and target structures"""
        # Initialize with greedy mapping
        initial_mapping = self._create_greedy_mapping(source, target)
        
        # Optimize through iterative refinement
        optimized = self._optimize_mapping(initial_mapping, source, target)
        
        # Calculate confidence intervals
        confidence_intervals = self._calculate_confidence_intervals(
            optimized, source, target
        )
        
        optimal = OptimalMapping(
            element_mappings=optimized['elements'],
            relation_mappings=optimized['relations'],
            mapping_score=optimized['score'],
            optimization_path=optimized['path'],
            confidence_intervals=confidence_intervals
        )
        
        # Store in history
        self.mapping_history.append(optimal)
        
        return optimal
    
    def resolve_mapping_conflicts(self, conflicts: List[MappingConflict]) -> List[Resolution]:
        """Resolve conflicts in the mapping process"""
        resolutions = []
        
        # Sort conflicts by severity
        sorted_conflicts = sorted(conflicts, key=lambda c: c.severity, reverse=True)
        
        for conflict in sorted_conflicts:
            resolution = self._resolve_single_conflict(conflict)
            resolutions.append(resolution)
            
            # Update other conflicts based on this resolution
            self._propagate_resolution(resolution, conflicts)
        
        # Store resolutions
        self.conflict_resolutions.extend(resolutions)
        
        return resolutions
    
    def generate_partial_mappings(self, source: Domain, target: Domain) -> List[PartialMapping]:
        """Generate multiple partial mappings between structures"""
        partial_mappings = []
        
        # Try different mapping strategies
        strategies = [
            self._type_based_partial_mapping,
            self._relation_based_partial_mapping,
            self._goal_oriented_partial_mapping,
            self._constraint_preserving_partial_mapping
        ]
        
        for strategy in strategies:
            mapping = strategy(source, target)
            if mapping and mapping.coverage > 0.3:  # Minimum coverage threshold
                partial_mappings.append(mapping)
        
        # Combine complementary partial mappings
        combined = self._combine_partial_mappings(partial_mappings)
        partial_mappings.extend(combined)
        
        # Sort by coverage and confidence
        partial_mappings.sort(
            key=lambda m: m.coverage * m.confidence, 
            reverse=True
        )
        
        return partial_mappings
    
    def optimize_mapping_through_search(self, initial_mapping: StructuralMapping) -> OptimalMapping:
        """Optimize a mapping through search algorithms"""
        # Convert to search state
        current_state = self._mapping_to_state(initial_mapping)
        best_state = current_state.copy()
        best_score = self._evaluate_state(current_state)
        
        # Search parameters
        max_iterations = 1000
        temperature = 1.0
        cooling_rate = 0.995
        
        optimization_path = []
        
        # Simulated annealing search
        for iteration in range(max_iterations):
            # Generate neighbor state
            neighbor = self._generate_neighbor(current_state)
            neighbor_score = self._evaluate_state(neighbor)
            
            # Calculate acceptance probability
            delta = neighbor_score - self._evaluate_state(current_state)
            if delta > 0 or np.random.random() < np.exp(delta / temperature):
                # Accept the neighbor
                step = MappingStep(
                    action="accept_neighbor",
                    element_mapped=neighbor.get('last_mapped_element'),
                    relation_mapped=neighbor.get('last_mapped_relation'),
                    score_delta=delta,
                    timestamp=iteration
                )
                optimization_path.append(step)
                
                current_state = neighbor
                
                # Update best if necessary
                if neighbor_score > best_score:
                    best_state = neighbor
                    best_score = neighbor_score
            
            # Cool down
            temperature *= cooling_rate
            
            # Early stopping if converged
            if temperature < 0.01:
                break
        
        # Convert best state back to mapping
        optimal = OptimalMapping(
            element_mappings=best_state['element_mappings'],
            relation_mappings=best_state['relation_mappings'],
            mapping_score=best_score,
            optimization_path=optimization_path,
            confidence_intervals={}
        )
        
        return optimal
    
    def create_multi_level_mapping(self, structures: List[Domain]) -> MultiLevelMapping:
        """Create a multi-level mapping across multiple structures"""
        if len(structures) < 2:
            raise ValueError("Need at least 2 structures for multi-level mapping")
        
        # Create pairwise mappings at each level
        surface_mappings = []
        structural_mappings = []
        system_mappings = []
        
        for i in range(len(structures) - 1):
            source = structures[i]
            target = structures[i + 1]
            
            # Surface level
            surface = self._create_surface_mapping(source, target)
            surface_mappings.append(surface)
            
            # Structural level
            structural = self._create_structural_mapping(source, target)
            structural_mappings.append(structural)
            
            # System level
            system = self._create_system_mapping(source, target)
            system_mappings.append(system)
        
        # Merge mappings across all structures
        merged_surface = self._merge_surface_mappings(surface_mappings)
        merged_structural = self._merge_structural_mappings(structural_mappings)
        merged_system = self._merge_system_mappings(system_mappings)
        
        # Identify cross-level constraints
        cross_level_constraints = self._identify_cross_level_constraints(
            merged_surface, merged_structural, merged_system
        )
        
        return MultiLevelMapping(
            surface_level=merged_surface,
            structural_level=merged_structural,
            system_level=merged_system,
            cross_level_constraints=cross_level_constraints
        )
    
    def _create_greedy_mapping(self, source: Domain, target: Domain) -> Dict[str, Any]:
        """Create an initial greedy mapping"""
        element_mappings = {}
        relation_mappings = {}
        
        # Map elements greedily by similarity
        for source_elem_id, source_elem in source.elements.items():
            best_target = None
            best_score = 0.0
            
            for target_elem_id, target_elem in target.elements.items():
                if target_elem_id not in element_mappings.values():
                    score = self._calculate_element_similarity(source_elem, target_elem)
                    if score > best_score:
                        best_score = score
                        best_target = target_elem_id
            
            if best_target and best_score > 0.5:
                element_mappings[source_elem_id] = best_target
        
        # Map relations based on element mappings
        for source_rel_id, source_rel in source.relations.items():
            if (source_rel.source in element_mappings and 
                source_rel.target in element_mappings):
                # Look for corresponding relation in target
                for target_rel_id, target_rel in target.relations.items():
                    if (target_rel.source == element_mappings[source_rel.source] and
                        target_rel.target == element_mappings[source_rel.target] and
                        target_rel.type == source_rel.type):
                        relation_mappings[source_rel_id] = target_rel_id
                        break
        
        score = self._calculate_mapping_score(
            element_mappings, relation_mappings, source, target
        )
        
        return {
            'elements': element_mappings,
            'relations': relation_mappings,
            'score': score,
            'path': []
        }
    
    def _optimize_mapping(self, initial: Dict[str, Any], 
                         source: Domain, target: Domain) -> Dict[str, Any]:
        """Optimize a mapping through iterative refinement"""
        current = initial.copy()
        improved = True
        path = []
        
        while improved:
            improved = False
            
            # Try swapping element mappings
            for source_elem1 in list(current['elements'].keys()):
                for source_elem2 in list(current['elements'].keys()):
                    if source_elem1 != source_elem2:
                        # Try swapping
                        new_mapping = current['elements'].copy()
                        new_mapping[source_elem1], new_mapping[source_elem2] = \
                            new_mapping.get(source_elem2), new_mapping.get(source_elem1)
                        
                        # Recalculate relation mappings
                        new_relations = self._recalculate_relation_mappings(
                            new_mapping, source, target
                        )
                        
                        # Evaluate new score
                        new_score = self._calculate_mapping_score(
                            new_mapping, new_relations, source, target
                        )
                        
                        if new_score > current['score']:
                            step = MappingStep(
                                action="swap_elements",
                                element_mapped=f"{source_elem1}<->{source_elem2}",
                                relation_mapped=None,
                                score_delta=new_score - current['score'],
                                timestamp=len(path)
                            )
                            path.append(step)
                            
                            current['elements'] = new_mapping
                            current['relations'] = new_relations
                            current['score'] = new_score
                            improved = True
                            break
                
                if improved:
                    break
        
        current['path'] = path
        return current
    
    def _resolve_single_conflict(self, conflict: MappingConflict) -> Resolution:
        """Resolve a single mapping conflict"""
        if conflict.conflict_type == ConflictType.ONE_TO_MANY:
            # Choose the mapping with highest confidence
            best_mapping = max(
                conflict.possible_resolutions,
                key=lambda r: r.confidence
            )
            return best_mapping
            
        elif conflict.conflict_type == ConflictType.TYPE_MISMATCH:
            # Prefer mappings that preserve type hierarchy
            for resolution in conflict.possible_resolutions:
                if self._preserves_type_hierarchy(resolution):
                    return resolution
            
            # Fall back to highest confidence
            return max(conflict.possible_resolutions, key=lambda r: r.confidence)
            
        elif conflict.conflict_type == ConflictType.CONSTRAINT_VIOLATION:
            # Try to find a resolution that satisfies constraints
            for resolution in conflict.possible_resolutions:
                if self._satisfies_constraints(resolution):
                    return resolution
            
            # Create a new resolution that modifies constraints
            return self._create_constraint_relaxing_resolution(conflict)
        
        else:
            # Default: highest confidence
            return max(conflict.possible_resolutions, key=lambda r: r.confidence)
    
    def _calculate_element_similarity(self, elem1: Element, elem2: Element) -> float:
        """Calculate similarity between two elements"""
        # Type similarity
        type_sim = 1.0 if elem1.type == elem2.type else 0.5
        
        # Property similarity
        common_props = set(elem1.properties.keys()) & set(elem2.properties.keys())
        if common_props:
            prop_sim = len(common_props) / len(
                set(elem1.properties.keys()) | set(elem2.properties.keys())
            )
        else:
            prop_sim = 0.0
        
        # Relation similarity (number of relations)
        rel_diff = abs(len(elem1.relations) - len(elem2.relations))
        rel_sim = 1.0 / (1.0 + rel_diff)
        
        # Combine similarities
        return type_sim * 0.4 + prop_sim * 0.4 + rel_sim * 0.2
    
    def _calculate_mapping_score(self, element_mappings: Dict[str, str],
                               relation_mappings: Dict[str, str],
                               source: Domain, target: Domain) -> float:
        """Calculate overall mapping score"""
        # Coverage score
        elem_coverage = len(element_mappings) / len(source.elements)
        rel_coverage = len(relation_mappings) / len(source.relations) if source.relations else 1.0
        
        # Consistency score
        consistency = self._calculate_consistency_score(
            element_mappings, relation_mappings, source, target
        )
        
        # Systematicity score
        systematicity = self._calculate_systematicity_score(
            element_mappings, relation_mappings, source, target
        )
        
        # Combine scores
        return (elem_coverage * 0.3 + 
                rel_coverage * 0.3 + 
                consistency * 0.2 + 
                systematicity * 0.2)
    
    def _calculate_consistency_score(self, element_mappings: Dict[str, str],
                                   relation_mappings: Dict[str, str],
                                   source: Domain, target: Domain) -> float:
        """Calculate consistency of the mapping"""
        consistent_relations = 0
        total_mapped_relations = 0
        
        for source_rel_id, target_rel_id in relation_mappings.items():
            source_rel = source.relations[source_rel_id]
            target_rel = target.relations[target_rel_id]
            
            # Check if element mappings are consistent with relation mapping
            if (source_rel.source in element_mappings and
                source_rel.target in element_mappings):
                if (element_mappings[source_rel.source] == target_rel.source and
                    element_mappings[source_rel.target] == target_rel.target):
                    consistent_relations += 1
            
            total_mapped_relations += 1
        
        return consistent_relations / total_mapped_relations if total_mapped_relations > 0 else 1.0
    
    def _calculate_systematicity_score(self, element_mappings: Dict[str, str],
                                     relation_mappings: Dict[str, str],
                                     source: Domain, target: Domain) -> float:
        """Calculate systematicity (preference for coherent systems of relations)"""
        # Find connected components in source
        source_components = self._find_connected_components(source)
        
        # Check how well components map together
        component_scores = []
        for component in source_components:
            mapped_together = sum(
                1 for elem in component 
                if elem in element_mappings
            )
            score = mapped_together / len(component) if component else 0
            component_scores.append(score)
        
        return np.mean(component_scores) if component_scores else 0.0
    
    def _find_connected_components(self, domain: Domain) -> List[Set[str]]:
        """Find connected components in the domain graph"""
        visited = set()
        components = []
        
        def dfs(elem_id: str, component: Set[str]):
            if elem_id in visited:
                return
            visited.add(elem_id)
            component.add(elem_id)
            
            # Find neighbors through relations
            for rel in domain.relations.values():
                if rel.source == elem_id and rel.target not in visited:
                    dfs(rel.target, component)
                elif rel.target == elem_id and rel.source not in visited:
                    dfs(rel.source, component)
        
        for elem_id in domain.elements:
            if elem_id not in visited:
                component = set()
                dfs(elem_id, component)
                components.append(component)
        
        return components
