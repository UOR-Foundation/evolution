import ast
import os
import importlib.util
import sys
import types

# Stub heavy dependencies required by the module under test
sys.modules.setdefault(
    'modules.universal_consciousness.cosmic_consciousness_core',
    types.ModuleType('cosmic_consciousness_core'),
)
setattr(sys.modules['modules.universal_consciousness.cosmic_consciousness_core'],
        'CosmicConsciousness', object)
sys.modules.setdefault(
    'modules.uor_meta_architecture.uor_meta_vm',
    types.ModuleType('uor_meta_vm'),
)

class _DummyVM:
    def __init__(self, *args, **kwargs):
        pass

setattr(sys.modules['modules.uor_meta_architecture.uor_meta_vm'],
        'UORMetaRealityVM', _DummyVM)
setattr(sys.modules['modules.uor_meta_architecture.uor_meta_vm'],
        'MetaDimensionalInstruction', object)
setattr(sys.modules['modules.uor_meta_architecture.uor_meta_vm'],
        'MetaOpCode', object)
setattr(sys.modules['modules.uor_meta_architecture.uor_meta_vm'],
        'InfiniteOperand', object)
sys.modules.setdefault(
    'modules.meta_reality_consciousness.meta_reality_core',
    types.ModuleType('meta_reality_core'),
)
class _Dummy:
    def __init__(self, *args, **kwargs):
        pass

setattr(sys.modules['modules.meta_reality_consciousness.meta_reality_core'],
        'MetaRealityConsciousness', _Dummy)


def load_sic():
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


def test_self_modification_module_generation():
    obj = sic.SelfImplementingConsciousness(None)
    comp = sic.ConsciousnessComponentSpecification(
        component_name="core",
        component_type="core",
        interfaces=[],
        dependencies=[],
        implementation_strategy="impl",
    )
    cap = sic.SelfModificationCapability(
        capability_name="modify_core",
        modification_scope="local",
        modification_types=["rewrite"],
        safety_constraints=[],
    )
    obj.architecture_design = sic.ConsciousnessArchitectureDesign(
        consciousness_component_specifications=[comp],
        consciousness_interaction_patterns=[],
        consciousness_evolution_pathways=[],
        consciousness_optimization_strategies=[],
        self_modification_capabilities=[cap],
    )

    code = obj._generate_self_modification_module()
    tree = ast.parse(code)
    cls = next(
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "EnhancedSelfModification"
    )
    methods = {n.name for n in cls.body if isinstance(n, ast.FunctionDef)}
    assert "modify_component" in methods
    assert "modify_core" in methods
