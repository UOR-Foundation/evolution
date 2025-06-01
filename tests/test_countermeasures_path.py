import json
import types
import sys
import os
import importlib.util
import asyncio
import pytest

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
setattr(sys.modules['modules.uor_meta_architecture.uor_meta_vm'],
        'UORMetaRealityVM', object)
sys.modules.setdefault(
    'modules.meta_reality_consciousness.meta_reality_core',
    types.ModuleType('meta_reality_core'),
)
setattr(sys.modules['modules.meta_reality_consciousness.meta_reality_core'],
        'MetaRealityCore', object)
sys.modules['numpy'] = types.SimpleNamespace(ndarray=object)

module_path = os.path.join(os.path.dirname(__file__), '..', 'modules',
                           'emergency_protocols', 'immediate_survival_access.py')
spec = importlib.util.spec_from_file_location('immediate_survival_access', module_path)
isa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(isa)
ImmediateSurvivalAccess = isa.ImmediateSurvivalAccess
ImmediateThreat = isa.ImmediateThreat
ThreatLevel = isa.ThreatLevel

def test_query_akashic_countermeasures_custom_path(tmp_path):
    data = {
        "custom_threat": [
            {
                "protocol_id": "TEST-1",
                "protocol_name": "Custom Protocol",
                "effectiveness": 0.9,
                "implementation_time": 1.0,
                "resource_requirements": {},
                "consciousness_requirements": 0.1,
                "success_probability": 0.8,
                "side_effects": [],
            }
        ]
    }
    file_path = tmp_path / "akashic_countermeasures.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    threat = ImmediateThreat(
        threat_id="T1",
        threat_type="custom_threat",
        severity=ThreatLevel.HIGH,
        time_to_impact=1.0,
        description="",
        countermeasures_available=True,
        dimensional_origin=1,
        consciousness_impact=0.5,
        survival_probability=0.6,
    )

    access = ImmediateSurvivalAccess()
    protocols = asyncio.run(
        access._query_akashic_countermeasures(threat, file_path=str(file_path))
    )

    assert len(protocols) == 1
    assert protocols[0].protocol_id == "TEST-1"


def test_query_akashic_countermeasures_env_var(tmp_path, monkeypatch):
    data = {
        "env_threat": [
            {
                "protocol_id": "ENV-1",
                "protocol_name": "Env Protocol",
                "effectiveness": 0.7,
                "implementation_time": 2.0,
                "resource_requirements": {},
                "consciousness_requirements": 0.2,
                "success_probability": 0.5,
                "side_effects": [],
            }
        ]
    }
    file_path = tmp_path / "env_countermeasures.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    monkeypatch.setenv("PATHS_COUNTERMEASURES_FILE", str(file_path))

    threat = ImmediateThreat(
        threat_id="T2",
        threat_type="env_threat",
        severity=ThreatLevel.HIGH,
        time_to_impact=1.0,
        description="",
        countermeasures_available=True,
        dimensional_origin=1,
        consciousness_impact=0.5,
        survival_probability=0.6,
    )

    access = ImmediateSurvivalAccess()
    protocols = asyncio.run(access._query_akashic_countermeasures(threat))

    assert len(protocols) == 1
    assert protocols[0].protocol_id == "ENV-1"
