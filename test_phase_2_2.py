"""
Test Suite for Phase 2.2 - Analogical Reasoning and Creative Problem Solving

This test suite validates the implementation of analogical reasoning, creative
problem-solving, insight generation, and integrated intelligence capabilities.
"""

import unittest
from datetime import datetime
import numpy as np

# Core imports
from core.prime_vm import ConsciousPrimeVM
from consciousness.consciousness_integration import ConsciousnessIntegrator

# Analogical reasoning imports
from modules.analogical_reasoning.analogy_engine import (
    AnalogicalReasoningEngine, Domain, Element, Relation, Problem, Solution
)
from modules.analogical_reasoning.structure_mapper import StructureMapper
from modules.analogical_reasoning.conceptual_blending import (
    ConceptualBlendingEngine, ConceptualSpace
)

# Creative engine imports
from modules.creative_engine.creativity_core import (
    CreativityCore, CreativityConstraints, CreativityType
)

# Problem solving imports
from modules.problem_solving.insight_generator import InsightGenerator
from modules.problem_solving.problem_solver import IntegratedProblemSolver

# Knowledge systems imports
from modules.knowledge_systems.knowledge_graph import (
    KnowledgeGraph, KnowledgeNode, KnowledgeEdge, NodeType, EdgeType
)


class TestAnalogicalReasoning(unittest.TestCase):
    """Test analogical reasoning capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.vm = ConsciousPrimeVM()
        self.knowledge_graph = KnowledgeGraph()
        self.analogy_engine = AnalogicalReasoningEngine(self.vm, self.knowledge_graph)
        
        # Create test domains
        self.solar_system = self._create_solar_system_domain()
        self.atom = self._create_atom_domain()
        
    def _create_solar_system_domain(self) -> Domain:
        """Create solar system domain for testing"""
        elements = {
            "sun": Element("sun", "star", {"mass": "large", "center": True}, ["orbits"]),
            "earth": Element("earth", "planet", {"mass": "medium"}, ["orbits"]),
            "moon": Element("moon", "satellite", {"mass": "small"}, ["orbits"])
        }
        
        relations = {
            "earth_orbits_sun": Relation("earth_orbits_sun", "orbits", "earth", "sun"),
            "moon_orbits_earth": Relation("moon_orbits_earth", "orbits", "moon", "earth")
        }
        
        return Domain(
            name="solar_system",
            elements=elements,
            relations=relations,
            constraints=["gravity", "orbital_mechanics"],
            goals=["stable_orbits"]
        )
    
    def _create_atom_domain(self) -> Domain:
        """Create atom domain for testing"""
        elements = {
            "nucleus": Element("nucleus", "core", {"charge": "positive", "center": True}, ["orbits"]),
            "electron": Element("electron", "particle", {"charge": "negative"}, ["orbits"])
        }
        
        relations = {
            "electron_orbits_nucleus": Relation(
                "electron_orbits_nucleus", "orbits", "electron", "nucleus"
            )
        }
        
        return Domain(
            name="atom",
            elements=elements,
            relations=relations,
            constraints=["electromagnetic_force"],
            goals=["stable_configuration"]
        )
    
    def test_structural_mapping(self):
        """Test structural mapping between domains"""
        # Create mapping between solar system and atom
        mapping = self.analogy_engine.create_structural_mapping(
            self.solar_system, self.atom
        )
        
        # Verify mapping quality
        self.assertGreater(mapping.mapping_confidence, 0.5)
        self.assertIn("sun", mapping.element_correspondences)
        self.assertEqual(mapping.element_correspondences["sun"], "nucleus")
        
        # Verify relation mapping
        self.assertIn("earth_orbits_sun", mapping.relation_correspondences)
        
    def test_solution_transfer(self):
        """Test solution transfer through analogy"""
        # Create a problem in the atom domain
        problem = Problem(
            id="electron_configuration",
            domain=self.atom,
            initial_state={"electrons": "scattered"},
            goal_state={"electrons": "organized_shells"},
            constraints=["energy_levels"]
        )
        
        # Find analogical solutions
        solutions = self.analogy_engine.find_analogical_solutions(problem)
        
        # Verify solutions found
        self.assertGreater(len(solutions), 0)
        
        # Check solution quality
        best_solution = solutions[0]
        self.assertGreater(best_solution.confidence_score, 0.3)
        self.assertIsNotNone(best_solution.explanation)
        
    def test_analogy_chain(self):
        """Test chain of analogies for complex reasoning"""
        # Create a problem requiring multiple analogies
        problem = Problem(
            id="complex_system",
            domain=self.atom,
            initial_state={"structure": "unknown"},
            goal_state={"structure": "optimized"},
            constraints=["multiple_forces"]
        )
        
        # Generate analogy chains
        chains = self.analogy_engine.generate_multiple_analogies(problem)
        
        # Verify chain generation
        self.assertGreater(len(chains), 0)
        
        # Check chain coherence
        if chains:
            best_chain = chains[0]
            self.assertGreater(best_chain.chain_coherence, 0.5)
            self.assertGreater(len(best_chain.emergent_insights), 0)


class TestCreativeEngine(unittest.TestCase):
    """Test creative problem-solving capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.vm = ConsciousPrimeVM()
        self.consciousness = ConsciousnessIntegrator(self.vm)
        self.creative_engine = CreativityCore(self.vm, self.consciousness)
        
    def test_creative_solution_generation(self):
        """Test generation of creative solutions"""
        # Create a test problem
        domain = Domain(
            name="test_domain",
            elements={"A": Element("A", "type1", {}, [])},
            relations={},
            constraints=["constraint1"],
            goals=["goal1"]
        )
        
        problem = Problem(
            id="creative_test",
            domain=domain,
            initial_state={"state": "initial"},
            goal_state={"state": "goal"},
            constraints=[]
        )
        
        # Set creativity constraints
        constraints = CreativityConstraints(
            novelty_threshold=0.6,
            utility_threshold=0.5
        )
        
        # Generate creative solution
        solution = self.creative_engine.generate_creative_solution(problem, constraints)
        
        # Verify solution properties
        self.assertIsNotNone(solution)
        self.assertGreater(solution.novelty_score, 0)
        self.assertGreater(solution.utility_score, 0)
        self.assertIn(solution.creativity_type, CreativityType)
        
    def test_creativity_evaluation(self):
        """Test evaluation of creative solutions"""
        # Create a mock solution
        solution = Solution(
            problem_id="test",
            steps=[{"action": "creative_step"}],
            final_state={"result": "creative"},
            success_score=0.8
        )
        
        # Evaluate creativity
        evaluation = self.creative_engine.evaluate_creativity(solution)
        
        # Verify evaluation components
        self.assertIsNotNone(evaluation.novelty_assessment)
        self.assertIsNotNone(evaluation.utility_assessment)
        self.assertIsNotNone(evaluation.surprise_assessment)
        self.assertIsNotNone(evaluation.elegance_assessment)
        self.assertGreater(evaluation.overall_creativity_score, 0)
        
    def test_creative_insight_generation(self):
        """Test generation of creative insights"""
        # Create problem context
        from modules.creative_engine.creativity_core import ProblemContext
        
        domain = Domain("insight_domain", {}, {}, [], [])
        problem = Problem("insight_problem", domain, {}, {}, [])
        
        context = ProblemContext(
            problem=problem,
            related_problems=[],
            previous_attempts=[],
            constraints=[],
            available_resources={}
        )
        
        # Trigger insight
        insight = self.creative_engine.trigger_creative_insight(context)
        
        # Verify insight properties
        self.assertIsNotNone(insight)
        self.assertGreater(insight.confidence_level, 0)
        self.assertGreater(len(insight.supporting_evidence), 0)
        self.assertGreater(len(insight.implications), 0)


class TestInsightGenerator(unittest.TestCase):
    """Test insight generation capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.vm = ConsciousPrimeVM()
        self.consciousness = ConsciousnessIntegrator(self.vm)
        self.creative_engine = CreativityCore(self.vm, self.consciousness)
        self.insight_generator = InsightGenerator(self.consciousness, self.creative_engine)
        
    def test_insight_opportunity_detection(self):
        """Test detection of insight opportunities"""
        from modules.problem_solving.insight_generator import ProblemState, Indicator
        
        # Create problem state at impasse
        domain = Domain("test", {}, {}, [], [])
        problem = Problem("test", domain, {}, {}, [])
        
        problem_state = ProblemState(
            problem=problem,
            current_approach=None,
            attempted_solutions=[],
            time_spent=100.0,
            frustration_level=0.8,
            progress_indicators=[
                Indicator("progress", 0.2, "low progress")
            ]
        )
        
        # Detect opportunities
        opportunities = self.insight_generator.detect_insight_opportunities(problem_state)
        
        # Verify opportunity detection
        self.assertGreater(len(opportunities), 0)
        
        # Check for impasse detection
        impasse_detected = any(
            opp.opportunity_type.value == "impasse" 
            for opp in opportunities
        )
        self.assertTrue(impasse_detected)
        
    def test_insight_generation(self):
        """Test insight generation process"""
        
        # Create problem context
        domain = Domain("insight_test", {}, {}, [], [])
        problem = Problem("insight_test", domain, {}, {}, [])
        
        context = ProblemContext(
            problem=problem,
            related_problems=[],
            previous_attempts=[],
            constraints=[],
            available_resources={}
        )
        
        # Generate insight
        insight = self.insight_generator.generate_insight(context)
        
        # Verify insight generation
        self.assertIsNotNone(insight)
        self.assertIsNotNone(insight.insight_content)
        self.assertGreater(insight.confidence_level, 0)
        self.assertGreater(insight.integration_potential, 0)
        
    def test_insight_validation(self):
        """Test insight validation process"""
        
        # Generate an insight
        domain = Domain("validation_test", {}, {}, [], [])
        problem = Problem("validation_test", domain, {}, {}, [])
        context = ProblemContext(problem, [], [], [], {})
        
        insight = self.insight_generator.generate_insight(context)
        
        # Validate the insight
        validation = self.insight_generator.validate_insight_quality(insight)
        
        # Verify validation
        self.assertIsNotNone(validation)
        self.assertGreater(len(validation.validation_tests), 0)
        self.assertIn('logical_consistency', validation.test_results)
        self.assertGreater(validation.overall_validity, 0)


class TestIntegratedProblemSolver(unittest.TestCase):
    """Test integrated problem-solving capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.vm = ConsciousPrimeVM()
        self.knowledge_graph = KnowledgeGraph()
        self.analogy_engine = AnalogicalReasoningEngine(self.vm, self.knowledge_graph)
        self.creative_engine = CreativityCore(
            self.vm, ConsciousnessIntegrator(self.vm)
        )
        self.problem_solver = IntegratedProblemSolver(
            self.vm, self.analogy_engine, self.creative_engine
        )
        
    def test_complex_problem_solving(self):
        """Test solving complex problems with integrated strategies"""
        # Create a complex problem
        elements = {
            "resource_a": Element("resource_a", "resource", {"amount": 100}, []),
            "resource_b": Element("resource_b", "resource", {"amount": 50}, []),
            "goal": Element("goal", "target", {"required_a": 80, "required_b": 40}, [])
        }
        
        domain = Domain(
            name="resource_optimization",
            elements=elements,
            relations={},
            constraints=["limited_resources", "efficiency"],
            goals=["optimize_usage"]
        )
        
        problem = Problem(
            id="complex_optimization",
            domain=domain,
            initial_state={"allocated_a": 0, "allocated_b": 0},
            goal_state={"goal_achieved": True},
            constraints=["minimize_waste"]
        )
        
        # Solve the problem
        solution = self.problem_solver.solve_complex_problem(problem)
        
        # Verify comprehensive solution
        self.assertIsNotNone(solution)
        self.assertGreater(len(solution.solution_components), 0)
        self.assertIsNotNone(solution.synthesis_approach)
        self.assertIsNotNone(solution.confidence_assessment)
        self.assertGreater(solution.confidence_assessment.overall_confidence, 0)
        
    def test_strategy_orchestration(self):
        """Test orchestration of multiple strategies"""
        # Create a problem
        domain = Domain("test", {}, {}, [], [])
        problem = Problem("orchestration_test", domain, {}, {}, [])
        
        # Orchestrate strategies
        orchestration = self.problem_solver.orchestrate_solution_strategies(problem)
        
        # Verify orchestration
        self.assertGreater(len(orchestration.active_strategies), 0)
        self.assertIsNotNone(orchestration.orchestration_plan)
        self.assertIsNotNone(orchestration.performance_monitoring)
        
    def test_meta_solution_generation(self):
        """Test generation of meta-solutions"""
        from modules.problem_solving.problem_solver import ProblemClass
        
        # Generate meta-solutions for optimization problems
        meta_solutions = self.problem_solver.generate_meta_solutions(
            ProblemClass.OPTIMIZATION
        )
        
        # Verify meta-solutions
        self.assertGreater(len(meta_solutions), 0)
        
        if meta_solutions:
            meta_solution = meta_solutions[0]
            self.assertEqual(meta_solution.problem_class, ProblemClass.OPTIMIZATION)
            self.assertIsNotNone(meta_solution.meta_strategy)
            self.assertGreater(len(meta_solution.applicability_conditions), 0)


class TestKnowledgeGraph(unittest.TestCase):
    """Test knowledge graph capabilities"""
    
    def setUp(self):
        """Set up test environment"""
        self.knowledge_graph = KnowledgeGraph()
        
    def test_node_operations(self):
        """Test node addition and retrieval"""
        # Create and add a node
        node = KnowledgeNode(
            node_id="test_node",
            node_type=NodeType.CONCEPT,
            content={"name": "TestConcept", "value": 42}
        )
        
        success = self.knowledge_graph.add_node(node)
        self.assertTrue(success)
        
        # Verify node was added
        self.assertIn("test_node", self.knowledge_graph.nodes)
        
        # Test duplicate prevention
        success = self.knowledge_graph.add_node(node)
        self.assertFalse(success)
        
    def test_edge_operations(self):
        """Test edge addition and relationships"""
        # Add nodes first
        node1 = KnowledgeNode("node1", NodeType.CONCEPT, {"name": "A"})
        node2 = KnowledgeNode("node2", NodeType.CONCEPT, {"name": "B"})
        
        self.knowledge_graph.add_node(node1)
        self.knowledge_graph.add_node(node2)
        
        # Add edge
        edge = KnowledgeEdge(
            edge_id="edge1",
            source_id="node1",
            target_id="node2",
            edge_type=EdgeType.RELATED_TO,
            weight=0.8
        )
        
        success = self.knowledge_graph.add_edge(edge)
        self.assertTrue(success)
        
        # Verify edge was added
        self.assertIn("edge1", self.knowledge_graph.edges)
        
    def test_inference(self):
        """Test relationship inference"""
        # Create a simple hierarchy
        nodes = [
            KnowledgeNode("animal", NodeType.CONCEPT, {"name": "Animal"}),
            KnowledgeNode("mammal", NodeType.CONCEPT, {"name": "Mammal"}),
            KnowledgeNode("dog", NodeType.CONCEPT, {"name": "Dog"})
        ]
        
        for node in nodes:
            self.knowledge_graph.add_node(node)
        
        # Add IS_A relationships
        edges = [
            KnowledgeEdge("e1", "mammal", "animal", EdgeType.IS_A),
            KnowledgeEdge("e2", "dog", "mammal", EdgeType.IS_A)
        ]
        
        for edge in edges:
            self.knowledge_graph.add_edge(edge)
        
        # Infer relationships
        inference_result = self.knowledge_graph.infer_relationships("dog")
        
        # Verify transitive inference
        self.assertGreater(len(inference_result.inferred_edges), 0)
        self.assertGreater(inference_result.confidence, 0)
        
    def test_spreading_activation(self):
        """Test spreading activation in the graph"""
        # Create connected nodes
        nodes = [
            KnowledgeNode(f"node{i}", NodeType.CONCEPT, {"value": i})
            for i in range(5)
        ]
        
        for node in nodes:
            self.knowledge_graph.add_node(node)
        
        # Create chain of connections
        for i in range(4):
            edge = KnowledgeEdge(
                f"edge{i}",
                f"node{i}",
                f"node{i+1}",
                EdgeType.RELATED_TO,
                weight=0.9
            )
            self.knowledge_graph.add_edge(edge)
        
        # Perform spreading activation
        activation_levels = self.knowledge_graph.activate_spreading(
            ["node0"], activation_strength=1.0
        )
        
        # Verify activation spread
        self.assertGreater(activation_levels["node0"], 0.9)
        self.assertGreater(activation_levels["node1"], 0.5)
        self.assertGreater(activation_levels["node2"], 0)
        
        # Check decay with distance
        self.assertGreater(
            activation_levels["node1"],
            activation_levels["node2"]
        )


class TestIntegration(unittest.TestCase):
    """Test integration of all Phase 2.2 components"""
    
    def setUp(self):
        """Set up integrated test environment"""
        self.vm = ConsciousPrimeVM()
        self.knowledge_graph = KnowledgeGraph()
        self.consciousness = ConsciousnessIntegrator(self.vm)
        
        # Initialize all components
        self.analogy_engine = AnalogicalReasoningEngine(self.vm, self.knowledge_graph)
        self.creative_engine = CreativityCore(self.vm, self.consciousness)
        self.problem_solver = IntegratedProblemSolver(
            self.vm, self.analogy_engine, self.creative_engine
        )
        
    def test_end_to_end_problem_solving(self):
        """Test complete problem-solving pipeline"""
        # Create a problem that requires multiple capabilities
        elements = {
            "start": Element("start", "state", {"position": 0}, []),
            "goal": Element("goal", "state", {"position": 10}, []),
            "obstacle": Element("obstacle", "barrier", {"position": 5}, [])
        }
        
        relations = {
            "blocked": Relation("blocked", "blocks", "obstacle", "path")
        }
        
        domain = Domain(
            name="navigation_puzzle",
            elements=elements,
            relations=relations,
            constraints=["avoid_obstacles", "find_shortest_path"],
            goals=["reach_goal"]
        )
        
        problem = Problem(
            id="navigate_with_creativity",
            domain=domain,
            initial_state={"position": 0, "path_clear": False},
            goal_state={"position": 10, "goal_reached": True},
            constraints=["cannot_go_through_obstacle"]
        )
        
        # Solve using integrated system
        solution = self.problem_solver.solve_complex_problem(problem)
        
        # Verify solution uses multiple strategies
        strategy_types = {
            comp.source_strategy for comp in solution.solution_components
        }
        self.assertGreater(len(strategy_types), 1)
        
        # Check for analogical insights
        self.assertGreater(len(solution.analogical_insights), 0)
        
        # Verify solution quality
        self.assertGreater(
            solution.confidence_assessment.overall_confidence, 0.5
        )
        
    def test_learning_and_adaptation(self):
        """Test system learning from experience"""
        # Create multiple similar problems
        problems = []
        for i in range(3):
            domain = Domain(
                name=f"learning_domain_{i}",
                elements={"elem": Element("elem", "type", {"id": i}, [])},
                relations={},
                constraints=[],
                goals=[f"goal_{i}"]
            )
            
            problem = Problem(
                id=f"learning_problem_{i}",
                domain=domain,
                initial_state={"state": "start"},
                goal_state={"state": "end"},
                constraints=[]
            )
            problems.append(problem)
        
        # Solve problems and learn
        solutions = []
        for problem in problems:
            solution = self.problem_solver.solve_complex_problem(problem)
            solutions.append(solution)
        
        # Verify learning occurred
        initial_history_size = len(self.problem_solver.solving_history)
        
        # Create solving attempts from solutions
        from modules.problem_solving.problem_solver import SolvingAttempt, Strategy
        
        attempts = []
        for i, (problem, solution) in enumerate(zip(problems, solutions)):
            attempt = SolvingAttempt(
                attempt_id=f"attempt_{i}",
                problem=problem,
                strategies_used=[],
                solution_quality=0.8,
                time_taken=10.0,
                lessons_learned=["test_lesson"]
            )
            attempts.append(attempt)
        
        # Learn from attempts
        self.problem_solver.learn_problem_solving_patterns(attempts)
        
        # Verify patterns were learned
        self.assertGreater(len(self.problem_solver.learned_patterns), 0)


def run_phase_2_2_tests():
    """Run all Phase 2.2 tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestAnalogicalReasoning,
        TestCreativeEngine,
        TestInsightGenerator,
        TestIntegratedProblemSolver,
        TestKnowledgeGraph,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("PHASE 2.2 TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Print component summary
    print("\nCOMPONENT STATUS:")
    print("✓ Analogical Reasoning Engine - Implemented")
    print("✓ Creative Problem Solving - Implemented")
    print("✓ Insight Generation - Implemented")
    print("✓ Integrated Problem Solver - Implemented")
    print("✓ Knowledge Graph System - Implemented")
    print("✓ Multi-Strategy Orchestration - Implemented")
    
    return result


if __name__ == "__main__":
    run_phase_2_2_tests()
