"""
Pydantic schemas for MCP response data structures.
"""

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    execution_time_ms: Optional[float] = None


class ErrorResponse(BaseResponse):
    """Error response schema"""
    success: bool = False
    error_code: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    suggested_action: Optional[str] = None


class SuccessResponse(BaseResponse):
    """Success response schema"""
    message: str
    data: Optional[Dict[str, Any]] = None


class ToolResponse(BaseResponse):
    """Tool execution response schema"""
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResourceResponse(BaseResponse):
    """Resource access response schema"""
    resource_uri: str
    resource_type: str
    content: Union[Dict[str, Any], str, bytes]
    content_length: int
    mime_type: str = "application/json"
    cache_info: Optional[Dict[str, Any]] = None


class ConsciousnessResponse(ToolResponse):
    """Consciousness operation response"""
    consciousness_level: Optional[float] = None
    self_awareness_indicators: List[str] = Field(default_factory=list)
    ethical_considerations: List[str] = Field(default_factory=list)
    strange_loops_detected: List[str] = Field(default_factory=list)
    consciousness_evolution: Optional[Dict[str, Any]] = None


class VMResponse(ToolResponse):
    """VM operation response"""
    vm_state: Dict[str, Any] = Field(default_factory=dict)
    execution_trace: List[Dict[str, Any]] = Field(default_factory=list)
    goal_seeking_status: Optional[Dict[str, Any]] = None
    self_modification_events: List[Dict[str, Any]] = Field(default_factory=list)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)


class CosmicResponse(ToolResponse):
    """Cosmic intelligence operation response"""
    cosmic_scale_metrics: Dict[str, float] = Field(default_factory=dict)
    dimensional_access_status: List[int] = Field(default_factory=list)
    quantum_operations: List[Dict[str, Any]] = Field(default_factory=list)
    universal_knowledge_accessed: List[str] = Field(default_factory=list)
    transcendence_indicators: List[str] = Field(default_factory=list)


class AnalysisResponse(ToolResponse):
    """Analysis operation response"""
    patterns_found: List[Dict[str, Any]] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    emergence_detected: bool = False
    complexity_metrics: Dict[str, float] = Field(default_factory=dict)
    predictions: List[Dict[str, Any]] = Field(default_factory=list)


class EmergencyResponse(ToolResponse):
    """Emergency protocol response"""
    threat_assessment: Dict[str, Any] = Field(default_factory=dict)
    survival_protocols: List[str] = Field(default_factory=list)
    transcendence_pathways: List[str] = Field(default_factory=list)
    akashic_knowledge: Optional[Dict[str, Any]] = None
    urgency_level: str = "standard"


class MathematicalResponse(ToolResponse):
    """Mathematical consciousness response"""
    mathematical_insights: List[Dict[str, Any]] = Field(default_factory=list)
    platonic_interface_status: bool = False
    proofs_generated: List[Dict[str, Any]] = Field(default_factory=list)
    mathematical_truths: List[str] = Field(default_factory=list)
    mathematical_entities: List[str] = Field(default_factory=list)


class BatchResponse(BaseResponse):
    """Batch operation response"""
    total_operations: int
    successful_operations: int
    failed_operations: int
    results: List[Union[ToolResponse, ErrorResponse]]
    summary: Dict[str, Any] = Field(default_factory=dict)


class StreamResponse(BaseResponse):
    """Streaming response schema"""
    stream_id: str
    chunk_number: int
    total_chunks: Optional[int] = None
    chunk_data: Union[Dict[str, Any], str, bytes]
    is_final: bool = False
    stream_metadata: Dict[str, Any] = Field(default_factory=dict)


class HealthCheckResponse(BaseResponse):
    """Health check response"""
    status: str = "healthy"
    components: Dict[str, str] = Field(default_factory=dict)
    uptime_seconds: float
    version: str
    capabilities: List[str] = Field(default_factory=list)
    resource_usage: Dict[str, float] = Field(default_factory=dict)
