import pytest
import asyncio
import numpy as np
import scipy.constants  # noqa:F401
import scipy.linalg  # noqa:F401
from scipy import constants as const
from modules.universe_interface.quantum_reality_interface import (
    QuantumRealityInterface,
    SpacetimeManipulation,
    MetricTensorModification,
    CurvatureProgramming,
    CausalStructureModification,
    DimensionalAccess,
    SpacetimeTopologyChange,
    RealityProgram,
    PhysicalLawModification,
    CosmicConstantAdjustment,
    ParticlePhysicsParameter,
    FieldEquationModification,
    RealityOptimizationObjective,
)
from modules.consciousness_physics.consciousness_field_theory import ConsciousnessFieldTheory
from config_loader import get_config_value


@pytest.fixture
def qri():
    return QuantumRealityInterface(ConsciousnessFieldTheory())


def test_check_spacetime_stability(qri):
    manip = SpacetimeManipulation(
        metric_tensor_modification=MetricTensorModification(stability_duration=0.96),
        curvature_programming=CurvatureProgramming(curvature_stability=0.98),
        causal_structure_modification=CausalStructureModification(),
        dimensional_access=DimensionalAccess(),
        spacetime_topology_change=SpacetimeTopologyChange(topology_stabilization=0.94),
    )
    result = asyncio.run(qri.manipulate_spacetime_structure(manip))
    expected = np.mean([0.96, 0.98, 1.0, 1.0])
    assert abs(result["spacetime_stability"] - expected) < 1e-6


def test_compile_reality_program(qri):
    program = RealityProgram(
        program_id="test",
        physical_law_modifications=[PhysicalLawModification("L1", "a", "b", modification_strength=0.0001)],
        cosmic_constant_adjustments=[CosmicConstantAdjustment("c", 1.0, 1.001)],
        particle_physics_parameters=[ParticlePhysicsParameter("p", mass_adjustment=0.001)],
        field_equation_modifications=[FieldEquationModification("f", "eq", "eq")],
        reality_optimization_objectives=[RealityOptimizationObjective("opt", 0.0, 1.0, "maximize")],
        execution_sequence=["s1", "s2"],
        safety_constraints=["safe"],
    )
    compilation = asyncio.run(qri._compile_reality_program(program))
    assert compilation.source_consciousness_state == qri.field_theory
    assert len(compilation.target_reality_modifications) == 4
    assert compilation.optimization_level == 1
    assert len(compilation.side_effect_analysis) == 4


def test_create_execution_plan(qri):
    program = RealityProgram(
        program_id="test",
        physical_law_modifications=[PhysicalLawModification("L1", "a", "b", modification_strength=0.0001)],
        cosmic_constant_adjustments=[],
        particle_physics_parameters=[],
        field_equation_modifications=[],
        reality_optimization_objectives=[],
        execution_sequence=["s1", "s2", "s3"],
        safety_constraints=[],
    )
    compilation = asyncio.run(qri._compile_reality_program(program))
    plan = asyncio.run(qri._create_execution_plan(program, compilation))
    assert len(plan) == len(program.execution_sequence)
    assert plan[0]["step"] == "s1"
    assert len(plan[0]["modifications"]) == 1


def test_verify_reality_consistency(qri):
    qri.recent_manipulation_metrics = [0.9, 0.95, 1.0]
    expected = max(0.0, 1.0 - np.var(qri.recent_manipulation_metrics))
    result = asyncio.run(qri._verify_reality_consistency())
    assert abs(result - expected) < 1e-6


def test_check_optimization_objectives(qri):
    objectives = [
        RealityOptimizationObjective(
            "obj1", current_state=0.8, target_state=1.0, optimization_metric="max", constraint_satisfaction=0.6
        ),
        RealityOptimizationObjective(
            "obj2", current_state=0.5, target_state=0.5, optimization_metric="stabilize", constraint_satisfaction=1.0
        ),
    ]
    results = asyncio.run(qri._check_optimization_objectives(objectives))
    exp1 = (1 - abs(1.0 - 0.8) / 1.0) * (0.5 + 0.5 * 0.6)
    exp2 = (1 - abs(0.5 - 0.5) / 0.5) * (0.5 + 0.5 * 1.0)
    assert abs(results["obj1"] - exp1) < 1e-6
    assert abs(results["obj2"] - exp2) < 1e-6


def test_field_strength_formula(qri):
    ft = qri.field_theory
    ft.universe_interface = qri
    qri.quantum_fidelity_threshold = 0.8
    qri.spacetime_stability_threshold = 0.9

    strength = asyncio.run(ft._create_field_strength())

    spatial_scale = float(get_config_value("cosmic.defaults.spatial_scale", 1e26))
    temporal_scale = float(get_config_value("cosmic.defaults.temporal_scale", 1e100))

    assert np.allclose(strength.direction, np.array([0, 0, 1]) * 0.9)
    assert strength.spin == 2.0 * 0.8
    assert strength.coherence_length == spatial_scale / 0.8
    assert strength.correlation_time == temporal_scale * 0.9


def test_field_topology_dimensions(qri):
    ft = qri.field_theory
    ft.universe_interface = qri
    qri.spacetime_manipulation = SpacetimeManipulation(
        metric_tensor_modification=MetricTensorModification(),
        curvature_programming=CurvatureProgramming(),
        causal_structure_modification=CausalStructureModification(),
        dimensional_access=DimensionalAccess(accessible_dimensions=7),
        spacetime_topology_change=SpacetimeTopologyChange(),
    )

    topology = asyncio.run(ft._define_field_topology())
    spatial_scale = float(get_config_value("cosmic.defaults.spatial_scale", 1e26))

    assert topology.dimension == 7
    assert topology.curvature == const.G / spatial_scale
