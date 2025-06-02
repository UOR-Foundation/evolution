"""
Abstract Reasoning Module

This module provides abstract reasoning capabilities including logical reasoning,
temporal reasoning, modal reasoning, and paradox resolution.
"""

from modules.abstract_reasoning.logical_reasoning import LogicalReasoner
from modules.abstract_reasoning.temporal_reasoning import TemporalReasoner
from modules.abstract_reasoning.modal_reasoning import ModalReasoner
from modules.abstract_reasoning.paradox_resolver import ParadoxResolver
from modules.abstract_reasoning.concept_abstraction import ConceptAbstractor

__all__ = [
    'LogicalReasoner',
    'TemporalReasoner', 
    'ModalReasoner',
    'ParadoxResolver',
    'ConceptAbstractor'
]
