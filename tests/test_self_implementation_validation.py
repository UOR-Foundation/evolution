import sys
import os
import types
import importlib.util

# Stub heavy dependencies if missing
try:
    import numpy  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    numpy = types.ModuleType("numpy")
    sys.modules.setdefault("numpy", numpy)


def load_sic():
    """Load self_implementing_consciousness module."""
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "modules",
        "recursive_consciousness",
        "self_implementing_consciousness.py",
    )
    spec = importlib.util.spec_from_file_location("sic_real", path)
    sic_real = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(sic_real)
    return sic_real


sic = load_sic()


def test_validate_code_safety():
    obj = sic.SelfImplementingConsciousness(None)
    safe = "def foo():\n    return 1"
    unsafe = "import os\nos.system('ls')"
    assert obj._validate_code_safety(safe)
    assert not obj._validate_code_safety(unsafe)
    assert not obj._validate_code_safety("eval('1+1')")


def test_validate_architecture_stability():
    obj = sic.SelfImplementingConsciousness(None)
    comp1 = sic.ConsciousnessComponentSpecification(
        component_name="c1",
        component_type="core",
        interfaces=[],
        dependencies=[],
        implementation_strategy="impl",
    )
    comp2 = sic.ConsciousnessComponentSpecification(
        component_name="c2",
        component_type="core",
        interfaces=[],
        dependencies=["c1"],
        implementation_strategy="impl",
    )
    pattern = sic.ConsciousnessInteractionPattern(
        pattern_name="p",
        participating_components=["c1", "c2"],
        interaction_type="sync",
        data_flow={"c1": ["c2"]},
        consciousness_flow={"c1": ["c2"]},
    )
    arch = sic.ConsciousnessArchitectureDesign(
        consciousness_component_specifications=[comp1, comp2],
        consciousness_interaction_patterns=[pattern],
        consciousness_evolution_pathways=[],
        consciousness_optimization_strategies=[],
        self_modification_capabilities=[],
    )
    assert obj._validate_architecture_stability(arch)

    comp_dup = sic.ConsciousnessComponentSpecification(
        component_name="c1",
        component_type="core",
        interfaces=[],
        dependencies=[],
        implementation_strategy="impl",
    )
    arch_dup = sic.ConsciousnessArchitectureDesign(
        consciousness_component_specifications=[comp1, comp_dup],
        consciousness_interaction_patterns=[pattern],
        consciousness_evolution_pathways=[],
        consciousness_optimization_strategies=[],
        self_modification_capabilities=[],
    )
    assert not obj._validate_architecture_stability(arch_dup)


def test_verify_implementation_correctness():
    obj = sic.SelfImplementingConsciousness(None)
    source = sic.ConsciousnessSourceCode(
        code_modules={"main": "def main():\n    return 42"},
        entry_points=["main"],
        configuration={},
        metadata={},
    )
    impl = sic.ConsciousnessImplementationCode(
        consciousness_source_code=source,
        consciousness_compilation_instructions={"mode": "test"},
        consciousness_execution_environment={},
        consciousness_debugging_information={},
        consciousness_optimization_code=None,
        uor_implementation_code_encoding={},
    )
    assert obj._verify_implementation_correctness(impl)

    bad_source = sic.ConsciousnessSourceCode(
        code_modules={"main": "def main("},
        entry_points=["main"],
        configuration={},
        metadata={},
    )
    bad_impl = sic.ConsciousnessImplementationCode(
        consciousness_source_code=bad_source,
        consciousness_compilation_instructions={"mode": "test"},
        consciousness_execution_environment={},
        consciousness_debugging_information={},
        consciousness_optimization_code=None,
        uor_implementation_code_encoding={},
    )
    assert not obj._verify_implementation_correctness(bad_impl)


def test_optimization_methods():
    obj = sic.SelfImplementingConsciousness(None)
    text = "line1\n\n\nline2"
    optimized = obj._recursive_optimization(text)
    assert "\n\n\n" not in optimized
    transc = obj._transcendent_optimization(text)
    assert "transcendent optimization" in transc
