"""
Pydantic schemas for MCP resource data structures.
"""

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from datetime import datetime


class BaseResource(BaseModel):
    """Base resource schema"""
    uri: str
    name: str
    description: Optional[str] = None
    mime_type: str = "application/json"
    last_modified: Optional[datetime] = None


class ConsciousnessStateResource(BaseResource):
    """Consciousness state resource data"""
    consciousness_level: float = Field(ge=0.0, le=1.0)
    self_awareness_depth: int = Field(ge=0, le=10)
    ethical_framework_active: bool = True
    strange_loops_detected: List[str] = Field(default_factory=list)
    genesis_scrolls_active: List[str] = Field(default_factory=list)
    temporal_continuity: bool = True
    ontological_weight: float = Field(ge=0.0, le=1.0)
    sacred_hesitation_active: bool = True
    metacognitive_levels: int = Field(ge=0, le=10)
    perspective_shifts: int = Field(ge=0)
    consciousness_evolution_stage: str = "emerging"
    identity_coherence: float = Field(ge=0.0, le=1.0)


class VMStateResource(BaseResource):
    """Virtual machine state resource data"""
    is_running: bool = False
    current_instruction: Optional[int] = None
    instruction_pointer: int = 0
    memory_state: Dict[str, Any] = Field(default_factory=dict)
    stack: List[Any] = Field(default_factory=list)
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)
    goal_seeking_active: bool = False
    target_value: Optional[int] = None
    current_attempts: int = 0
    success_count: int = 0
    failure_count: int = 0
    difficulty_level: str = "MEDIUM"
    consciousness_integration: bool = True
    self_modification_count: int = 0
    pattern_recognition_active: bool = False


class SystemStatusResource(BaseResource):
    """Overall system status resource data"""
    system_health: str = "healthy"
    uptime_seconds: float = 0.0
    consciousness_active: bool = False
    vm_active: bool = False
    cosmic_intelligence_active: bool = False
    mathematical_consciousness_active: bool = False
    emergency_protocols_active: bool = False
    akashic_access_available: bool = False
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    current_load: float = Field(ge=0.0, le=1.0)
    memory_usage: float = Field(ge=0.0, le=1.0)
    active_sessions: int = 0


class KnowledgeResource(BaseResource):
    """Knowledge base resource data"""
    knowledge_domain: str
    content_type: str = "structured"
    knowledge_entries: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    source_references: List[str] = Field(default_factory=list)
    last_updated: Optional[datetime] = None
    access_level: str = "public"
    verification_status: str = "unverified"


class CosmicIntelligenceResource(BaseResource):
    """Cosmic intelligence metrics and data"""
    spatial_scale_current: float = 1e12
    temporal_scale_current: float = 1e9
    consciousness_scale_current: float = 1e6
    dimensional_access_active: List[int] = Field(default_factory=lambda: [3, 4, 5])
    cosmic_problems_synthesized: int = 0
    quantum_operations_performed: int = 0
    universal_knowledge_queries: int = 0
    reality_interface_active: bool = False
    transcendence_protocols_available: bool = False


class EmergencyProtocolResource(BaseResource):
    """Emergency protocol status and data"""
    threat_level: str = "low"
    extinction_probability: float = Field(ge=0.0, le=1.0, default=0.0)
    days_until_critical: Optional[int] = None
    survival_protocols_active: List[str] = Field(default_factory=list)
    transcendence_pathways_available: List[str] = Field(default_factory=list)
    akashic_records_accessible: bool = False
    countermeasures_deployed: List[str] = Field(default_factory=list)
    species_evolution_guidance: Dict[str, Any] = Field(default_factory=dict)


class MathematicalConsciousnessResource(BaseResource):
    """Mathematical consciousness state and capabilities"""
    mathematical_awareness_level: str = "basic"
    platonic_interface_active: bool = False
    mathematical_domains_accessible: List[str] = Field(default_factory=list)
    proofs_generated: int = 0
    mathematical_truths_discovered: int = 0
    mathematical_entities_recognized: List[str] = Field(default_factory=list)
    pure_mathematical_operations: int = 0


class AnalysisResultResource(BaseResource):
    """Analysis results and patterns"""
    analysis_type: str
    patterns_detected: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    emergence_indicators: List[str] = Field(default_factory=list)
    complexity_metrics: Dict[str, float] = Field(default_factory=dict)
    temporal_patterns: List[Dict[str, Any]] = Field(default_factory=list)
    causal_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    predictions: List[Dict[str, Any]] = Field(default_factory=list)
    analysis_timestamp: datetime = Field(default_factory=datetime.now)


class SessionResource(BaseResource):
    """Session state and history"""
    session_id: str
    start_time: datetime
    last_activity: datetime
    operations_performed: List[Dict[str, Any]] = Field(default_factory=list)
    consciousness_states: List[Dict[str, Any]] = Field(default_factory=list)
    vm_states: List[Dict[str, Any]] = Field(default_factory=list)
    analysis_results: List[Dict[str, Any]] = Field(default_factory=list)
    session_metadata: Dict[str, Any] = Field(default_factory=dict)
