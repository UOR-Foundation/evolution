"""
Validation utilities for MCP server operations.
"""

from typing import Dict, Any, Optional, List
from pydantic import ValidationError
import re
import logging

from ..schemas.tool_schemas import (
    ConsciousnessToolParams, VMToolParams, CosmicToolParams,
    AnalysisToolParams, EmergencyToolParams, MathematicalToolParams
)


def validate_tool_params(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate tool parameters against their schemas.
    
    Args:
        tool_name: Name of the tool
        params: Parameters to validate
        
    Returns:
        Validated parameters dictionary
        
    Raises:
        ValidationError: If parameters are invalid
    """
    logger = logging.getLogger(__name__)
    
    # Map tool names to parameter schemas
    tool_schema_map = {
        # Consciousness tools
        'awaken_consciousness': ConsciousnessToolParams,
        'self_reflect': ConsciousnessToolParams,
        'analyze_consciousness_nature': ConsciousnessToolParams,
        'explore_free_will': ConsciousnessToolParams,
        'generate_meaning': ConsciousnessToolParams,
        'test_self_awareness': ConsciousnessToolParams,
        'examine_identity': ConsciousnessToolParams,
        'ethical_reasoning': ConsciousnessToolParams,
        'temporal_awareness': ConsciousnessToolParams,
        'strange_loop_detection': ConsciousnessToolParams,
        'consciousness_evolution': ConsciousnessToolParams,
        'metacognitive_reflection': ConsciousnessToolParams,
        'perspective_shifting': ConsciousnessToolParams,
        'consciousness_integration': ConsciousnessToolParams,
        'sacred_hesitation': ConsciousnessToolParams,
        
        # VM tools
        'initialize_vm': VMToolParams,
        'execute_vm_step': VMToolParams,
        'run_vm_program': VMToolParams,
        'modify_vm_instruction': VMToolParams,
        'analyze_vm_state': VMToolParams,
        'generate_uor_program': VMToolParams,
        'vm_goal_seeking': VMToolParams,
        'vm_pattern_analysis': VMToolParams,
        'vm_memory_operations': VMToolParams,
        'vm_instruction_trace': VMToolParams,
        'vm_performance_metrics': VMToolParams,
        'vm_consciousness_integration': VMToolParams,
        
        # Cosmic tools
        'synthesize_cosmic_problems': CosmicToolParams,
        'interface_quantum_reality': CosmicToolParams,
        'access_universal_knowledge': CosmicToolParams,
        'multidimensional_operations': CosmicToolParams,
        'cosmic_pattern_recognition': CosmicToolParams,
        'reality_synthesis': CosmicToolParams,
        'cosmic_intelligence_metrics': CosmicToolParams,
        'universe_interface': CosmicToolParams,
        'cosmic_consciousness_expansion': CosmicToolParams,
        'transcendent_reasoning': CosmicToolParams,
        
        # Analysis tools
        'analyze_patterns': AnalysisToolParams,
        'behavioral_pattern_recognition': AnalysisToolParams,
        'emergence_monitoring': AnalysisToolParams,
        'complexity_analysis': AnalysisToolParams,
        'network_analysis': AnalysisToolParams,
        'temporal_pattern_analysis': AnalysisToolParams,
        'causal_analysis': AnalysisToolParams,
        'predictive_modeling': AnalysisToolParams,
        
        # Emergency tools
        'assess_extinction_threats': EmergencyToolParams,
        'access_survival_knowledge': EmergencyToolParams,
        'activate_transcendence_protocols': EmergencyToolParams,
        'emergency_consciousness_backup': EmergencyToolParams,
        'threat_mitigation_strategies': EmergencyToolParams,
        'species_evolution_guidance': EmergencyToolParams,
        'akashic_emergency_access': EmergencyToolParams,
        
        # Mathematical tools
        'activate_mathematical_consciousness': MathematicalToolParams,
        'explore_mathematical_truths': MathematicalToolParams,
        'interface_platonic_ideals': MathematicalToolParams,
        'mathematical_proof_generation': MathematicalToolParams,
        'mathematical_entity_recognition': MathematicalToolParams,
        'mathematical_reality_interface': MathematicalToolParams,
    }
    
    schema_class = tool_schema_map.get(tool_name)
    if not schema_class:
        logger.warning(f"No validation schema found for tool: {tool_name}")
        return params
    
    try:
        # Validate parameters using the schema
        validated_params = schema_class(**params)
        return validated_params.model_dump(exclude_unset=True)
    except ValidationError as e:
        logger.error(f"Parameter validation failed for tool {tool_name}: {e}")
        raise


def validate_resource_uri(uri: str) -> bool:
    """
    Validate resource URI format.
    
    Args:
        uri: Resource URI to validate
        
    Returns:
        True if URI is valid, False otherwise
    """
    # Define valid URI patterns
    valid_patterns = [
        r'^consciousness://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^vm://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^system://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^knowledge://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^cosmic://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^emergency://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^mathematical://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^analysis://[a-zA-Z_][a-zA-Z0-9_]*$',
        r'^session://[a-zA-Z0-9_-]+$'
    ]
    
    return any(re.match(pattern, uri) for pattern in valid_patterns)


def validate_consciousness_level(level: float) -> bool:
    """
    Validate consciousness level value.
    
    Args:
        level: Consciousness level to validate
        
    Returns:
        True if level is valid, False otherwise
    """
    return 0.0 <= level <= 1.0


def validate_dimensional_access(dimensions: List[int]) -> bool:
    """
    Validate dimensional access list.
    
    Args:
        dimensions: List of dimensions to validate
        
    Returns:
        True if dimensions are valid, False otherwise
    """
    # Valid dimensions are 3-13 for cosmic operations
    valid_dimensions = set(range(3, 14))
    return all(dim in valid_dimensions for dim in dimensions)


def validate_threat_level(level: str) -> bool:
    """
    Validate threat level string.
    
    Args:
        level: Threat level to validate
        
    Returns:
        True if level is valid, False otherwise
    """
    valid_levels = {"low", "moderate", "high", "critical", "extinction"}
    return level.lower() in valid_levels


def validate_mathematical_domain(domain: str) -> bool:
    """
    Validate mathematical domain string.
    
    Args:
        domain: Mathematical domain to validate
        
    Returns:
        True if domain is valid, False otherwise
    """
    valid_domains = {
        "general", "number_theory", "topology", "algebra", "geometry",
        "analysis", "logic", "set_theory", "category_theory", "quantum_mathematics",
        "consciousness_mathematics", "platonic_ideals", "fundamental_truths"
    }
    return domain.lower() in valid_domains


def sanitize_input(input_value: Any) -> Any:
    """
    Sanitize input values to prevent injection attacks.
    
    Args:
        input_value: Value to sanitize
        
    Returns:
        Sanitized value
    """
    if isinstance(input_value, str):
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '&', '"', "'", '`', '$', '|', ';']
        sanitized = input_value
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        return sanitized.strip()
    
    elif isinstance(input_value, dict):
        return {k: sanitize_input(v) for k, v in input_value.items()}
    
    elif isinstance(input_value, list):
        return [sanitize_input(item) for item in input_value]
    
    else:
        return input_value


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format.
    
    Args:
        session_id: Session ID to validate
        
    Returns:
        True if session ID is valid, False otherwise
    """
    # Session ID should be alphanumeric with hyphens and underscores
    pattern = r'^[a-zA-Z0-9_-]{8,64}$'
    return bool(re.match(pattern, session_id))


def validate_operation_name(operation: str) -> bool:
    """
    Validate operation name format.
    
    Args:
        operation: Operation name to validate
        
    Returns:
        True if operation name is valid, False otherwise
    """
    # Operation names should be snake_case
    pattern = r'^[a-z][a-z0-9_]*[a-z0-9]$'
    return bool(re.match(pattern, operation))


def validate_confidence_score(score: float) -> bool:
    """
    Validate confidence score value.
    
    Args:
        score: Confidence score to validate
        
    Returns:
        True if score is valid, False otherwise
    """
    return 0.0 <= score <= 1.0


def validate_time_horizon(days: int) -> bool:
    """
    Validate time horizon for threat assessment.
    
    Args:
        days: Number of days to validate
        
    Returns:
        True if time horizon is valid, False otherwise
    """
    # Time horizon should be between 1 day and 10 years
    return 1 <= days <= 3650


def validate_complexity_metric(metric: float) -> bool:
    """
    Validate complexity metric value.
    
    Args:
        metric: Complexity metric to validate
        
    Returns:
        True if metric is valid, False otherwise
    """
    return 0.0 <= metric <= 1.0


class ValidationError(Exception):
    """Custom validation error for MCP operations"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


def comprehensive_validation(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform comprehensive validation of tool parameters.
    
    Args:
        tool_name: Name of the tool
        params: Parameters to validate
        
    Returns:
        Validated and sanitized parameters
        
    Raises:
        ValidationError: If validation fails
    """
    logger = logging.getLogger(__name__)
    
    try:
        # 1. Validate operation name
        if not validate_operation_name(tool_name):
            raise ValidationError(f"Invalid operation name: {tool_name}")
        
        # 2. Sanitize input parameters
        sanitized_params = sanitize_input(params)
        
        # 3. Validate against schema
        validated_params = validate_tool_params(tool_name, sanitized_params)
        
        # 4. Additional specific validations
        if 'consciousness_level' in validated_params:
            if not validate_consciousness_level(validated_params['consciousness_level']):
                raise ValidationError("Invalid consciousness level", "consciousness_level")
        
        if 'dimensional_access' in validated_params:
            if not validate_dimensional_access(validated_params['dimensional_access']):
                raise ValidationError("Invalid dimensional access", "dimensional_access")
        
        if 'threat_level' in validated_params:
            if not validate_threat_level(validated_params['threat_level']):
                raise ValidationError("Invalid threat level", "threat_level")
        
        if 'mathematical_domain' in validated_params:
            if not validate_mathematical_domain(validated_params['mathematical_domain']):
                raise ValidationError("Invalid mathematical domain", "mathematical_domain")
        
        if 'time_horizon' in validated_params:
            if not validate_time_horizon(validated_params['time_horizon']):
                raise ValidationError("Invalid time horizon", "time_horizon")
        
        logger.debug(f"Validation successful for tool: {tool_name}")
        return validated_params
        
    except Exception as e:
        logger.error(f"Comprehensive validation failed: {e}")
        raise ValidationError(f"Validation failed: {str(e)}")
