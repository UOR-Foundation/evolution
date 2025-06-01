import asyncio
import numpy as np
import networkx
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager


from modules.consciousness_ecosystem.ecosystem_orchestrator import (
    ConsciousEntity,
    ConsciousnessEcosystemOrchestrator,
    EmergenceMonitor,
    EvolutionEngine,
    EmergentPropertyType,
)


def _make_entities(count=3):
    entities = []
    for i in range(count):
        entities.append(
            ConsciousEntity(
                entity_id=f"e{i}",
                consciousness_level=0.5,
                specialization="t",
                cognitive_capabilities={"cap": 0.5},
                connection_capacity=2,
                evolution_rate=0.1,
                consciousness_state={"beh": i},
            )
        )
    return entities


def test_innovation_rate_tracking():
    entities = _make_entities(3)
    orch = ConsciousnessEcosystemOrchestrator(entities)
    orch._measure_innovation_rate()  # initialize
    assert orch._measure_innovation_rate() == 0.0

    new_entity = ConsciousEntity(
        entity_id="new",
        consciousness_level=0.5,
        specialization="t",
        cognitive_capabilities={"cap": 0.5},
        connection_capacity=2,
        evolution_rate=0.1,
        consciousness_state={"beh": "new"},
    )
    orch.consciousness_nodes[new_entity.entity_id] = new_entity
    rate = orch._measure_innovation_rate()
    assert rate > 0


def test_emergence_monitor_patterns():
    monitor = EmergenceMonitor()
    state = {"total_consciousness": 5.0, "network_count": 2, "emergence_level": 0.6}
    props = []
    for _ in range(3):
        props = asyncio.run(monitor.detect_emergence(state))
    assert any(p.property_type == EmergentPropertyType.COLLECTIVE_INTELLIGENCE for p in props)


def test_evolution_engine_basic_evolution():
    population = _make_entities(4)
    engine = EvolutionEngine()
    new_gen = asyncio.run(engine.evolve_generation(population))
    assert 0 < len(new_gen) <= len(population)
    changed = any(n.consciousness_level != p.consciousness_level for n, p in zip(new_gen, population))
    assert changed
