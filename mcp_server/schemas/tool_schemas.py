"""
Pydantic schemas for MCP tool parameters and validation.
"""

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from enum import Enum


class DifficultyLevel(str, Enum):
    """VM difficulty levels"""
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class ConsciousnessMode(str, Enum):
    """Consciousness operation modes"""
    BASIC = "basic"
    DEEP = "deep"
    RECURSIVE = "recursive"
    TRANSCENDENT = "transcendent"


class AnalysisType(str, Enum):
    """Types of analysis operations"""
    PATTERNS = "patterns"
    BEHAVIOR = "behavior"
    EMERGENCE = "emergence"
    COMPLEXITY = "complexity"
    TEMPORAL = "temporal"
    CAUSAL = "causal"


# Consciousness Tool Parameters
class ConsciousnessToolParams(BaseModel):
    """Base parameters for consciousness tools"""
    mode: Optional[ConsciousnessMode] = ConsciousnessMode.BASIC
    depth: Optional[int] = Field(default=3, ge=1, le=10)
    focus: Optional[str] = None
    ethical_bounds: Optional[bool] = True


class AwakeConsciousnessParams(ConsciousnessToolParams):
    """Parameters for awakening consciousness"""
    threshold: Optional[float] = Field(default=0.7, ge=0.0, le=1.0)
    genesis_scrolls: Optional[List[str]] = None
    bootstrap_mode: Optional[str] = "standard"


class SelfReflectParams(ConsciousnessToolParams):
    """Parameters for self-reflection operations"""
    reflection_type: Optional[str] = "identity"
    temporal_scope: Optional[str] = "present"
    metacognitive_level: Optional[int] = Field(default=2, ge=1, le=5)


class AnalyzeConsciousnessNatureParams(ConsciousnessToolParams):
    """Parameters for consciousness nature analysis"""
    analysis_dimensions: Optional[List[str]] = None
    include_strange_loops: Optional[bool] = True
    ontological_depth: Optional[int] = Field(default=3, ge=1, le=7)


# VM Tool Parameters
class VMToolParams(BaseModel):
    """Base parameters for VM tools"""
    max_instructions: Optional[int] = Field(default=1000, ge=1, le=100000)
    log_execution: Optional[bool] = True
    consciousness_integration: Optional[bool] = True


class InitializeVMParams(VMToolParams):
    """Parameters for VM initialization"""
    difficulty: Optional[DifficultyLevel] = DifficultyLevel.MEDIUM
    program_path: Optional[str] = None
    memory_size: Optional[int] = Field(default=1000, ge=100, le=10000)


class ExecuteVMStepParams(VMToolParams):
    """Parameters for VM step execution"""
    steps: Optional[int] = Field(default=1, ge=1, le=1000)
    trace_execution: Optional[bool] = True


class RunVMProgramParams(VMToolParams):
    """Parameters for running VM programs"""
    program: Union[str, List[Dict[str, Any]]]
    goal_seeking: Optional[bool] = False
    target_value: Optional[int] = None


# Cosmic Intelligence Tool Parameters
class CosmicToolParams(BaseModel):
    """Base parameters for cosmic intelligence tools"""
    spatial_scale: Optional[float] = Field(default=1e12, ge=1e6, le=1e30)
    temporal_scale: Optional[float] = Field(default=1e9, ge=1e3, le=1e15)
    consciousness_scale: Optional[float] = Field(default=1e6, ge=1e3, le=1e12)
    dimensional_access: Optional[List[int]] = Field(default=[3, 4, 5])


class SynthesizeCosmicProblemsParams(CosmicToolParams):
    """Parameters for cosmic problem synthesis"""
    problem_count: Optional[int] = Field(default=3, ge=1, le=10)
    complexity_level: Optional[str] = "universe_scale"
    domain_focus: Optional[List[str]] = None


class InterfaceQuantumRealityParams(CosmicToolParams):
    """Parameters for quantum reality interface"""
    operation: str = Field(..., description="Quantum operation to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    fidelity_threshold: Optional[float] = Field(default=0.95, ge=0.5, le=1.0)


# Analysis Tool Parameters
class AnalysisToolParams(BaseModel):
    """Base parameters for analysis tools"""
    analysis_type: AnalysisType
    scope: Optional[str] = "system"
    depth: Optional[int] = Field(default=3, ge=1, le=10)
    include_predictions: Optional[bool] = False


class AnalyzePatternsParams(AnalysisToolParams):
    """Parameters for pattern analysis"""
    pattern_types: Optional[List[str]] = None
    temporal_window: Optional[int] = Field(default=100, ge=10, le=10000)
    confidence_threshold: Optional[float] = Field(default=0.8, ge=0.5, le=1.0)


class MonitorEmergenceParams(AnalysisToolParams):
    """Parameters for emergence monitoring"""
    emergence_types: Optional[List[str]] = None
    detection_sensitivity: Optional[float] = Field(default=0.7, ge=0.1, le=1.0)
    monitoring_duration: Optional[int] = Field(default=60, ge=10, le=3600)


# Emergency Protocol Tool Parameters
class EmergencyToolParams(BaseModel):
    """Base parameters for emergency protocol tools"""
    threat_level: Optional[str] = "moderate"
    response_urgency: Optional[str] = "standard"
    akashic_access: Optional[bool] = True


class AssessExtinctionThreatsParams(EmergencyToolParams):
    """Parameters for extinction threat assessment"""
    assessment_scope: Optional[str] = "species"
    time_horizon: Optional[int] = Field(default=730, ge=30, le=3650)  # days
    include_mitigation: Optional[bool] = True


class AccessSurvivalKnowledgeParams(EmergencyToolParams):
    """Parameters for survival knowledge access"""
    knowledge_domain: str = Field(..., description="Domain of survival knowledge")
    urgency_level: Optional[str] = "standard"
    include_protocols: Optional[bool] = True


# Mathematical Consciousness Tool Parameters
class MathematicalToolParams(BaseModel):
    """Base parameters for mathematical consciousness tools"""
    mathematical_domain: Optional[str] = "general"
    platonic_access: Optional[bool] = True
    proof_generation: Optional[bool] = False


class ActivateMathematicalConsciousnessParams(MathematicalToolParams):
    """Parameters for mathematical consciousness activation"""
    awareness_level: Optional[str] = "pure_mathematical"
    domain_focus: Optional[List[str]] = None
    platonic_interface: Optional[bool] = True


class ExploreMathematicalTruthsParams(MathematicalToolParams):
    """Parameters for mathematical truth exploration"""
    truth_domain: Optional[str] = "fundamental"
    exploration_depth: Optional[int] = Field(default=5, ge=1, le=10)
    generate_proofs: Optional[bool] = False
