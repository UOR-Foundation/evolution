"""
Knowledge Systems Module

This module provides dynamic knowledge representation, conceptual networks,
and self-modifying knowledge structures that support analogical reasoning
and creative problem-solving.
"""

from modules.knowledge_systems.knowledge_graph import (
    KnowledgeGraph,
    KnowledgeNode,
    KnowledgeEdge,
    GraphQuery,
    GraphUpdate
)
from modules.knowledge_systems.concept_network import (
    ConceptNetwork,
    Concept,
    ConceptualRelation,
    ActivationPattern,
    SpreadingActivation
)
from modules.knowledge_systems.semantic_memory import (
    SemanticMemory,
    SemanticNode,
    PrimeEncoding,
    MemoryTrace,
    RetrievalCue
)
from modules.knowledge_systems.episodic_integration import (
    EpisodicIntegrator,
    Episode,
    ContextualMemory,
    TemporalLink,
    AutobiographicalMemory
)
from modules.knowledge_systems.knowledge_evolution import (
    KnowledgeEvolution,
    EvolutionMechanism,
    KnowledgeConflict,
    ResolutionStrategy,
    AdaptiveStructure
)

__all__ = [
    'KnowledgeGraph',
    'KnowledgeNode',
    'KnowledgeEdge',
    'GraphQuery',
    'GraphUpdate',
    'ConceptNetwork',
    'Concept',
    'ConceptualRelation',
    'ActivationPattern',
    'SpreadingActivation',
    'SemanticMemory',
    'SemanticNode',
    'PrimeEncoding',
    'MemoryTrace',
    'RetrievalCue',
    'EpisodicIntegrator',
    'Episode',
    'ContextualMemory',
    'TemporalLink',
    'AutobiographicalMemory',
    'KnowledgeEvolution',
    'EvolutionMechanism',
    'KnowledgeConflict',
    'ResolutionStrategy',
    'AdaptiveStructure'
]
