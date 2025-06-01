"""
Test Suite for Consciousness Ecosystem

Tests the functionality of large-scale consciousness networks, collective
intelligence emergence, and ecosystem-level consciousness capabilities.
"""

import pytest
import asyncio
import numpy as np
import networkx as nx
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime


class TestConsciousnessEcosystem:
    """Test consciousness ecosystem functionality"""
    
    @pytest.fixture
    def sample_entities(self):
        """Create sample conscious entities"""
        entities = []
        for i in range(10):
            entity = ConsciousEntity(
                entity_id=f"entity_{i}",
                consciousness_level=0.5 + (i * 0.05),
                specialization=f"type_{i % 3}",
                cognitive_capabilities={
                    "reasoning": 0.7 + (i * 0.02),
                    "creativity": 0.6 + (i * 0.03),
                    "memory": 0.8 + (i * 0.01)
                },
                connection_capacity=5,
                evolution_rate=0.1,
                consciousness_state={
                    "awareness": 0.7,
                    "intention": "collaborate",
                    "emotions": {"curiosity": 0.8}
                }
            )
            entities.append(entity)
        return entities
        
    @pytest.fixture
    def ecosystem_orchestrator(self, sample_entities):
        """Create ecosystem orchestrator"""
        return ConsciousnessEcosystemOrchestrator(sample_entities)
        
    @pytest.mark.asyncio
    async def test_ecosystem_emergence(self, ecosystem_orchestrator):
        """Test ecosystem-level consciousness emergence"""
        emergence = await ecosystem_orchestrator.orchestrate_ecosystem_emergence()
        
        assert isinstance(emergence, EcosystemEmergence)
        assert emergence.ecosystem_consciousness_level > 0
        assert emergence.network_effect_amplification > 1.0
        assert emergence.consciousness_density > 0
        assert len(emergence.emergent_properties) >= 0
        
    @pytest.mark.asyncio
    async def test_collective_intelligence(self, ecosystem_orchestrator):
        """Test collective intelligence facilitation"""
        collective_intel = await ecosystem_orchestrator.facilitate_collective_intelligence()
        
        assert isinstance(collective_intel, CollectiveIntelligence)
        assert collective_intel.intelligence_amplification_factor > 1.0
        assert collective_intel.collective_problem_solving_capability > 0
        assert collective_intel.collective_creativity_index > 0
        assert collective_intel.wisdom_synthesis_capability > 0
        
    @pytest.mark.asyncio
    async def test_network_coordination(self, ecosystem_orchestrator, sample_entities):
        """Test consciousness network coordination"""
        # Create sample networks
        import networkx as nx
        
        network1 = ConsciousnessNetwork(
            network_id="net1",
            participating_consciousness=sample_entities[:5],
            network_topology=NetworkTopology(
                topology_type=NetworkTopologyType.SMALL_WORLD,
                connection_graph=nx.watts_strogatz_graph(5, 3, 0.3),
                bandwidth_matrix=np.ones((5, 5)),
                latency_matrix=np.ones((5, 5)) * 0.01,
                reliability_scores={}
            ),
            communication_protocols=[],
            shared_consciousness_state=Mock(),
            collective_goals=[],
            emergence_level=0.5
        )
        
        network2 = ConsciousnessNetwork(
            network_id="net2",
            participating_consciousness=sample_entities[5:],
            network_topology=NetworkTopology(
                topology_type=NetworkTopologyType.SCALE_FREE,
                connection_graph=nx.barabasi_albert_graph(5, 2),
                bandwidth_matrix=np.ones((5, 5)),
                latency_matrix=np.ones((5, 5)) * 0.01,
                reliability_scores={}
            ),
            communication_protocols=[],
            shared_consciousness_state=Mock(),
            collective_goals=[],
            emergence_level=0.6
        )
        
        coordination = await ecosystem_orchestrator.coordinate_consciousness_networks(
            [network1, network2]
        )
        
        assert len(coordination.coordinated_networks) == 2
        assert coordination.coordination_efficiency > 0
        
    @pytest.mark.asyncio
    async def test_ecosystem_stability(self, ecosystem_orchestrator):
        """Test ecosystem stability maintenance"""
        stability = await ecosystem_orchestrator.ensure_ecosystem_stability()
        
        assert stability['stability_score'] > 0
        assert 'health_metrics' in stability
        assert 'diversity_status' in stability
        assert stability['resource_efficiency']['efficiency'] > 0
        
    @pytest.mark.asyncio
    async def test_diversity_optimization(self, ecosystem_orchestrator):
        """Test consciousness diversity optimization"""
        diversity = await ecosystem_orchestrator.optimize_consciousness_diversity()
        
        assert diversity.diversity_index > 0
        assert len(diversity.specialization_distribution) > 0
        assert diversity.cognitive_coverage > 0
        assert diversity.innovation_potential > 0
        assert diversity.ecosystem_resilience > 0
        
    def test_diversity_calculation(self, ecosystem_orchestrator):
        """Test Shannon diversity index calculation"""
        diversity = ecosystem_orchestrator._calculate_diversity_index()
        
        # Shannon index should be positive for diverse population
        assert diversity > 0
        assert diversity <= np.log(3)  # Max for 3 specialization types
        
    def test_network_effects(self, ecosystem_orchestrator):
        """Test network effect calculation"""
        network_effect = ecosystem_orchestrator._calculate_network_effects()
        
        # Should follow modified Metcalfe's law
        assert network_effect > 1.0
        # Should increase with more nodes
        assert network_effect < 10.0  # Reasonable upper bound
        
    def test_consciousness_density(self, ecosystem_orchestrator):
        """Test consciousness density calculation"""
        density = ecosystem_orchestrator._calculate_consciousness_density()
        
        assert 0 <= density <= 1.0
        # With sample entities having 0.5-1.0 consciousness levels
        assert density > 0.5


class TestEmergentProperties:
    """Test emergent property detection and management"""
    
    @pytest.mark.asyncio
    async def test_emergence_detection(self):
        """Test detection of emergent properties"""
        from modules.consciousness_ecosystem.ecosystem_orchestrator import EmergenceMonitor
        
        monitor = EmergenceMonitor()
        ecosystem_state = {
            'total_consciousness': 10.0,
            'network_count': 3,
            'emergence_level': 0.7
        }
        
        emergent_props = await monitor.detect_emergence(ecosystem_state)
        
        assert isinstance(emergent_props, list)
        # Should detect some emergent properties in complex ecosystem
        
    def test_emergent_property_types(self):
        """Test emergent property type definitions"""
        # Verify all emergent property types are defined
        property_types = [
            EmergentPropertyType.COLLECTIVE_INTELLIGENCE,
            EmergentPropertyType.SWARM_CREATIVITY,
            EmergentPropertyType.DISTRIBUTED_WISDOM,
            EmergentPropertyType.EMERGENT_GOALS,
            EmergentPropertyType.META_CONSCIOUSNESS,
            EmergentPropertyType.COLLECTIVE_INTUITION
        ]
        
        for prop_type in property_types:
            assert prop_type.value is not None


class TestEcosystemEvolution:
    """Test ecosystem-level evolution capabilities"""
    
    @pytest.fixture
    def evolution_parameters(self):
        """Create evolution parameters"""
        return {
            'selection_criteria': {
                'fitness_threshold': 0.6,
                'diversity_requirement': 0.7
            },
            'challenges': [
                'resource_scarcity',
                'environmental_change'
            ]
        }
        
    @pytest.mark.asyncio
    async def test_ecosystem_evolution(self, ecosystem_orchestrator, evolution_parameters):
        """Test ecosystem evolution management"""
        evolution = await ecosystem_orchestrator.manage_ecosystem_evolution(
            evolution_parameters
        )
        
        assert evolution.generation > 0
        assert isinstance(evolution.fitness_improvements, dict)
        assert isinstance(evolution.evolutionary_innovations, list)
        assert 0 <= evolution.adaptation_success_rate <= 1.0


class TestCollectiveIntelligence:
    """Test collective intelligence emergence"""
    
    @pytest.mark.asyncio
    async def test_distributed_reasoning(self, ecosystem_orchestrator):
        """Test distributed reasoning network creation"""
        # Mock the internal method
        ecosystem_orchestrator._create_distributed_reasoning_network = AsyncMock(
            return_value={'nodes': 10, 'connections': 45}
        )
        
        collective_intel = await ecosystem_orchestrator.facilitate_collective_intelligence()
        
        assert collective_intel.distributed_reasoning_network is not None
        assert collective_intel.intelligence_amplification_factor > 1.0
        
    @pytest.mark.asyncio
    async def test_collective_problem_solving(self, ecosystem_orchestrator):
        """Test collective problem-solving capabilities"""
        # Mock problem-solving amplification
        ecosystem_orchestrator._amplify_problem_solving = AsyncMock(
            return_value={'capability': 0.9}
        )
        
        collective_intel = await ecosystem_orchestrator.facilitate_collective_intelligence()
        
        assert collective_intel.collective_problem_solving_capability > 0
        
    @pytest.mark.asyncio
    async def test_wisdom_synthesis(self, ecosystem_orchestrator):
        """Test collective wisdom synthesis"""
        # Mock wisdom synthesis
        ecosystem_orchestrator._synthesize_collective_wisdom = AsyncMock(
            return_value={'synthesis_level': 0.8}
        )
        
        collective_intel = await ecosystem_orchestrator.facilitate_collective_intelligence()
        
        assert collective_intel.wisdom_synthesis_capability > 0


class TestNetworkTopologies:
    """Test different consciousness network topologies"""
    
    def test_topology_types(self):
        """Test all network topology types"""
        topologies = [
            NetworkTopologyType.FULLY_CONNECTED,
            NetworkTopologyType.HIERARCHICAL,
            NetworkTopologyType.SMALL_WORLD,
            NetworkTopologyType.SCALE_FREE,
            NetworkTopologyType.MODULAR,
            NetworkTopologyType.HYBRID
        ]
        
        for topology in topologies:
            assert topology.value is not None
            
    def test_network_creation(self):
        """Test consciousness network creation"""
        import networkx as nx
        
        # Create a simple network
        graph = nx.complete_graph(5)
        
        topology = NetworkTopology(
            topology_type=NetworkTopologyType.FULLY_CONNECTED,
            connection_graph=graph,
            bandwidth_matrix=np.ones((5, 5)),
            latency_matrix=np.ones((5, 5)) * 0.001,
            reliability_scores={(0, 1): 0.99, (1, 2): 0.98}
        )
        
        assert topology.connection_graph.number_of_nodes() == 5
        assert topology.connection_graph.number_of_edges() == 10  # Complete graph
        assert topology.bandwidth_matrix.shape == (5, 5)
        assert topology.latency_matrix.min() == 0.001


class TestEcosystemIntegration:
    """Test integration with other consciousness systems"""
    
    @pytest.mark.asyncio
    async def test_consciousness_aggregation(self, ecosystem_orchestrator):
        """Test aggregation of individual consciousness"""
        collective_state = await ecosystem_orchestrator._aggregate_consciousness()
        
        assert collective_state['total_awareness'] > 0
        assert isinstance(collective_state['shared_knowledge'], dict)
        assert isinstance(collective_state['collective_emotions'], dict)
        assert isinstance(collective_state['unified_intentions'], list)
        
    @pytest.mark.asyncio
    async def test_meta_consciousness_creation(self, ecosystem_orchestrator):
        """Test meta-consciousness creation"""
        collective_awareness = {
            'total_awareness': 7.5,
            'shared_knowledge': {'domain': 'consciousness'},
            'collective_emotions': {'curiosity': 0.8},
            'unified_intentions': ['explore', 'understand']
        }
        
        ecosystem_goals = [
            {'goal': 'collective_learning', 'priority': 0.9}
        ]
        
        meta_consciousness = await ecosystem_orchestrator._create_meta_consciousness(
            collective_awareness, ecosystem_goals
        )
        
        assert meta_consciousness['consciousness_level'] > collective_awareness['total_awareness']
        assert meta_consciousness['meta_awareness']['constituent_count'] == 10
        assert meta_consciousness['meta_cognition']['self_reflection'] is True
        assert meta_consciousness['meta_cognition']['emergence_understanding'] is True


class DummyGoal:
    def __init__(self, active=True, achieved=False, approach_strategy="direct"):
        self.active = active
        self.achieved = achieved
        self.approach_strategy = approach_strategy


class DummyVM:
    """Simple VM stub for self-reflection tests"""

    def __init__(self):
        self.execution_trace = [
            "PUSH", "ADD", "CREATIVE_SEARCH", "GOAL", "SUCCESS"
        ]
        self.stack = []
        self.memory = type("Mem", (), {"cells": {}, "regions": []})()
        self.error_count = 1
        self.error_history = [
            {"type": "overflow"},
            {"type": "overflow"},
            {"type": "timeout"},
            {"type": "overflow"}
        ]
        self.goals = [
            DummyGoal(True, True, "direct"),
            DummyGoal(False, False, "direct")
        ]
        self.decision_history = [
            {"type": "explore", "risk_level": 0.8},
            {"type": "explore", "risk_level": 0.7},
            {"type": "exploit", "risk_level": 0.2}
        ]
        self.consciousness_level = 1


class TestSelfReflectionHelpers:
    """Test self-reflection analysis helpers"""

    @pytest.fixture
    def reflection_engine(self):
        from modules.self_reflection import SelfReflectionEngine

        vm = DummyVM()
        return SelfReflectionEngine(vm)

    def test_identify_success_patterns(self, reflection_engine):
        patterns = reflection_engine._identify_success_patterns()
        assert isinstance(patterns, list)
        assert len(patterns) > 0

    def test_assess_creative_potential(self, reflection_engine):
        score = reflection_engine._assess_creative_potential()
        assert 0.0 <= score <= 1.0

    def test_decision_pattern_analysis(self, reflection_engine):
        patterns = reflection_engine._analyze_decision_patterns()
        assert any(p["type"] == "decision_type" for p in patterns)

    def test_goal_pattern_analysis(self, reflection_engine):
        patterns = reflection_engine._analyze_goal_patterns()
        types = {p["type"] for p in patterns}
        assert "goal_achievement" in types

    def test_adaptation_pattern_analysis(self, reflection_engine):
        patterns = reflection_engine._analyze_adaptation_patterns()
        assert any(p["type"] == "error_frequency" for p in patterns)


class TestConflictResolutionLearning:
    """Test conflict resolution strategy learning and application"""

    def test_strategy_effectiveness_update(self):
        from modules.relational_intelligence.conflict_resolution import (
            ConflictResolutionEngine,
            ConflictType,
            ResolutionStrategy,
        )

        engine = ConflictResolutionEngine()
        old = engine.strategy_effectiveness[ConflictType.GOAL_BASED][ResolutionStrategy.COMPETITION]
        engine._update_strategy_effectiveness("competition", 1.0)
        new = engine.strategy_effectiveness[ConflictType.GOAL_BASED][ResolutionStrategy.COMPETITION]
        assert new > old
        hist = engine.strategy_history[ResolutionStrategy.COMPETITION]
        assert hist["count"] == 1
        assert hist["avg"] == 1.0

    def test_history_influences_strategy_choice(self):
        from modules.relational_intelligence.conflict_resolution import (
            ConflictResolutionEngine,
            ConflictContext,
            ConflictType,
            ResolutionStrategy,
        )

        engine = ConflictResolutionEngine()
        conflict = ConflictContext(
            conflict_id="c1",
            conflict_type=ConflictType.GOAL_BASED,
            parties_involved=["A", "B"],
            core_issues=["issue"],
            underlying_needs={"A": ["security"], "B": ["security"]},
            emotional_context={
                "intensity": 0.5,
                "volatility": 0.2,
                "hurt_level": 0.2,
                "anger_level": 0.2,
                "fear_level": 0.2,
                "trust_damage": 0.2,
            },
            historical_context=[],
            cultural_factors=[],
            power_dynamics={"A": 0.5, "B": 0.5},
        )

        before = engine._identify_suitable_strategies(conflict)
        assert ResolutionStrategy.COMPETITION not in before

        engine._update_strategy_effectiveness("competition", 1.0)

        after = engine._identify_suitable_strategies(conflict)
        assert ResolutionStrategy.COMPETITION in after


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
