import asyncio
from core.instruction_set import PrimeInstruction
from consciousness.state_transition_manager import StateTransitionManager

from modules.unified_consciousness.consciousness_orchestrator import ConsciousnessState
from modules.unified_consciousness.identity_integration import (
    IdentityIntegrator,
    UnifiedIdentity,
    PersonalityTrait,
    PersonalityCoherence,
)

from unittest.mock import Mock, AsyncMock
import pytest
import numpy as np

class DummyOrchestrator:
    def __init__(self, state):
        self.current_state = state

@pytest.mark.asyncio
async def test_state_personality_adjustments():
    integrator = IdentityIntegrator(DummyOrchestrator(ConsciousnessState.CREATIVE))
    adjustments = integrator._get_state_personality_adjustments()
    assert adjustments[PersonalityTrait.CREATIVITY] > 0
    assert PersonalityTrait.OPENNESS in adjustments


def test_belief_coherence_calculation():
    integrator = IdentityIntegrator(DummyOrchestrator(ConsciousnessState.ACTIVE))
    balanced = {
        'about_self': ['A', 'B'],
        'about_world': ['C', 'D'],
        'about_others': ['E', 'F'],
        'derived': ['G', 'H'],
    }
    high = integrator._calculate_belief_coherence(balanced)
    imbalanced = {
        'about_self': ['A'] * 5,
        'about_world': [],
        'about_others': ['E'],
        'derived': [],
    }
    low = integrator._calculate_belief_coherence(imbalanced)
    assert high > low
    assert high <= 1.0 and low >= 0.5


@pytest.mark.asyncio
async def test_assess_authenticity_computation():
    orch = DummyOrchestrator(ConsciousnessState.ACTIVE)
    integrator = IdentityIntegrator(orch)
    integrator.personality_coherence = PersonalityCoherence(
        coherence_score=0.8,
        consistent_traits=[],
        contextual_variations={},
        integration_quality=0.75,
        stability_over_time=1.0,
    )
    integrator.unified_identity = UnifiedIdentity(
        identity_id='id',
        core_essence={},
        personality_profile={},
        value_system=[],
        belief_structure={},
        self_narrative='',
        identity_coherence=0.8,
        authenticity_score=0.8,
        evolution_stage='init',
    )
    integrator._assess_value_behavior_alignment = AsyncMock(return_value=0.9)
    score = await integrator._assess_authenticity()
    expected = np.mean([0.8, 0.9, min(1.0, 0.6 + 0.4 * 0.75)])
    assert score == pytest.approx(expected)


@pytest.mark.asyncio
async def test_evolve_beliefs_updates_structure():
    integrator = IdentityIntegrator(DummyOrchestrator(ConsciousnessState.ACTIVE))
    beliefs = await integrator._extract_beliefs()
    integrator.unified_identity = UnifiedIdentity(
        identity_id='id',
        core_essence={},
        personality_profile={},
        value_system=[],
        belief_structure=beliefs,
        self_narrative='',
        identity_coherence=0.8,
        authenticity_score=0.8,
        evolution_stage='init',
    )
    result = await integrator._evolve_beliefs('moderate_evolution')
    assert 'growth' in integrator.unified_identity.belief_structure['about_world'][-1]
    assert result['aspect'] == 'beliefs'


@pytest.mark.asyncio
async def test_evolve_capabilities_increases_levels():
    integrator = IdentityIntegrator(DummyOrchestrator(ConsciousnessState.ACTIVE))
    result = await integrator._evolve_capabilities('minor_evolution')
    for change in result['changes'].values():
        assert change['new'] >= change['old']
