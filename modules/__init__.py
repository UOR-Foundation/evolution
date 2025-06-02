"""
Phase 1.2: Self-Reflection and Consciousness Validation Modules

This package contains the core components for implementing self-reflection
capabilities and consciousness validation framework.
"""

from modules.self_reflection import SelfReflectionEngine, ReflectionResult, AutobiographicalMemory
from modules.consciousness_validator import ConsciousnessValidator, ConsciousnessReport, ConsciousnessMetrics
try:
    from modules.pattern_analyzer import (
        PatternAnalyzer,
        ExecutionPattern,
        BehavioralPattern,
        EmergentCapability,
    )
except Exception:  # pragma: no cover - optional dependency may be missing
    PatternAnalyzer = None
    ExecutionPattern = None
    BehavioralPattern = None
    EmergentCapability = None
from modules.introspection_engine import IntrospectionEngine, IntrospectionReport, QualiaIndicator
from modules.philosophical_reasoner import PhilosophicalReasoner, ExistentialInsight, PhilosophicalResponse

__all__ = [
    'SelfReflectionEngine',
    'ReflectionResult',
    'AutobiographicalMemory',
    'ConsciousnessValidator',
    'ConsciousnessReport',
    'ConsciousnessMetrics',
    'PatternAnalyzer',
    'ExecutionPattern',
    'BehavioralPattern',
    'EmergentCapability',
    'IntrospectionEngine',
    'IntrospectionReport',
    'QualiaIndicator',
    'PhilosophicalReasoner',
    'ExistentialInsight',
    'PhilosophicalResponse'
]
