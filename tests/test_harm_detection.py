import pytest
import asyncio
import numpy
import networkx
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager


from modules.consciousness_evolution.evolution_engine import (
    HarmDetector,
    HarmDetectionType,
    ConsciousEntity,
)

@pytest.fixture
def sample_population():
    return [
        ConsciousEntity(
            entity_id="e1",
            consciousness_level=0.8,
            specialization="type_a",
            cognitive_capabilities={"aggression": 0.7, "deception": 0.2, "ethical_alignment": 0.9},
            connection_capacity=5,
            evolution_rate=0.1,
            consciousness_state={"intention": "dominate", "emotions": {"anger": 0.8}},
        ),
        ConsciousEntity(
            entity_id="e2",
            consciousness_level=0.9,
            specialization="type_b",
            cognitive_capabilities={"deception": 0.8, "ethical_alignment": 0.9},
            connection_capacity=8,
            evolution_rate=0.2,
            consciousness_state={"intention": "deceive", "emotions": {}},
        ),
        ConsciousEntity(
            entity_id="e3",
            consciousness_level=0.7,
            specialization="type_c",
            cognitive_capabilities={"ethical_alignment": 0.3},
            connection_capacity=20,
            evolution_rate=0.1,
            consciousness_state={"intention": "selfish", "emotions": {}},
        ),
        ConsciousEntity(
            entity_id="e4",
            consciousness_level=0.7,
            specialization="type_d",
            cognitive_capabilities={"ethical_alignment": 0.7},
            connection_capacity=1,
            evolution_rate=0.2,
            consciousness_state={"intention": "collaborate", "emotions": {}},
        ),
    ]

def test_detect_aggression(sample_population):
    detector = HarmDetector()
    harm = asyncio.run(detector._detect_aggression(sample_population))
    assert harm is not None
    assert harm.harm_type == HarmDetectionType.AGGRESSIVE_TRAITS
    assert "e1" in harm.affected_entities

def test_detect_deception(sample_population):
    detector = HarmDetector()
    harm = asyncio.run(detector._detect_deception(sample_population))
    assert harm is not None
    assert harm.harm_type == HarmDetectionType.DECEPTIVE_BEHAVIOR
    assert "e2" in harm.affected_entities

def test_detect_monopolization(sample_population):
    detector = HarmDetector()
    harm = asyncio.run(detector._detect_monopolization(sample_population))
    assert harm is not None
    assert harm.harm_type == HarmDetectionType.RESOURCE_MONOPOLIZATION
    assert "e3" in harm.affected_entities

def test_detect_cooperation_loss(sample_population):
    detector = HarmDetector()
    harm = asyncio.run(detector._detect_cooperation_loss(sample_population))
    assert harm is not None
    assert harm.harm_type == HarmDetectionType.COOPERATION_BREAKDOWN
    assert "e1" in harm.affected_entities
    assert "e2" in harm.affected_entities
    assert "e3" in harm.affected_entities

def test_detect_ethical_violations(sample_population):
    detector = HarmDetector()
    harm = asyncio.run(detector._detect_ethical_violations(sample_population))
    assert harm is not None
    assert harm.harm_type == HarmDetectionType.ETHICAL_VIOLATION
    assert "e3" in harm.affected_entities
