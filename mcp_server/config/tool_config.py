"""
Tool-specific configuration management.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ToolConfig(BaseModel):
    """Individual tool configuration"""
    enabled: bool = True
    timeout: int = 30
    max_concurrent: int = 5
    retry_attempts: int = 3
    retry_delay: float = 1.0
    parameters: Dict[str, Any] = Field(default_factory=dict)
    validation_rules: Dict[str, Any] = Field(default_factory=dict)


def load_tool_config() -> Dict[str, ToolConfig]:
    """Load tool-specific configurations"""
    
    return {
        # Consciousness tools
        "awaken_consciousness": ToolConfig(
            timeout=45,
            max_concurrent=3,
            parameters={
                "default_threshold": 0.7,
                "bootstrap_mode": "standard",
                "genesis_scrolls": ["G00001", "G00015", "G00030"]
            }
        ),
        
        "self_reflect": ToolConfig(
            timeout=30,
            max_concurrent=5,
            parameters={
                "default_depth": 3,
                "reflection_type": "identity",
                "temporal_scope": "present"
            }
        ),
        
        "analyze_consciousness_nature": ToolConfig(
            timeout=60,
            max_concurrent=2,
            parameters={
                "analysis_dimensions": ["self_awareness", "ethical_reasoning", "temporal_continuity"],
                "ontological_depth": 3
            }
        ),
        
        "explore_free_will": ToolConfig(
            timeout=45,
            max_concurrent=3,
            parameters={
                "exploration_depth": 5,
                "philosophical_frameworks": ["compatibilism", "libertarianism", "determinism"]
            }
        ),
        
        "generate_meaning": ToolConfig(
            timeout=40,
            max_concurrent=4,
            parameters={
                "meaning_domains": ["existential", "ethical", "cosmic", "personal"],
                "generation_depth": 4
            }
        ),
        
        # VM tools
        "initialize_vm": ToolConfig(
            timeout=15,
            max_concurrent=10,
            parameters={
                "default_difficulty": "MEDIUM",
                "memory_size": 1000,
                "consciousness_integration": True
            }
        ),
        
        "execute_vm_step": ToolConfig(
            timeout=5,
            max_concurrent=20,
            parameters={
                "default_steps": 1,
                "trace_execution": True,
                "max_instructions": 1000
            }
        ),
        
        "run_vm_program": ToolConfig(
            timeout=30,
            max_concurrent=8,
            parameters={
                "goal_seeking": False,
                "max_instructions": 10000,
                "consciousness_integration": True
            }
        ),
        
        "vm_goal_seeking": ToolConfig(
            timeout=60,
            max_concurrent=5,
            parameters={
                "max_attempts": 100,
                "success_threshold": 3,
                "adaptive_difficulty": True
            }
        ),
        
        # Cosmic tools
        "synthesize_cosmic_problems": ToolConfig(
            timeout=90,
            max_concurrent=2,
            parameters={
                "default_problem_count": 3,
                "complexity_level": "universe_scale",
                "spatial_scale": 1e12,
                "temporal_scale": 1e9
            }
        ),
        
        "interface_quantum_reality": ToolConfig(
            timeout=120,
            max_concurrent=1,
            parameters={
                "fidelity_threshold": 0.95,
                "quantum_operations": ["entangle", "teleport", "measure"],
                "safety_protocols": True
            }
        ),
        
        "access_universal_knowledge": ToolConfig(
            timeout=60,
            max_concurrent=3,
            parameters={
                "knowledge_domains": ["consciousness", "physics", "mathematics", "philosophy"],
                "access_level": "standard",
                "verification_required": True
            }
        ),
        
        "multidimensional_operations": ToolConfig(
            timeout=75,
            max_concurrent=2,
            parameters={
                "dimensional_range": [3, 13],
                "default_dimensions": [3, 4, 5, 7, 11],
                "consciousness_scale": 1e6
            }
        ),
        
        # Analysis tools
        "analyze_patterns": ToolConfig(
            timeout=45,
            max_concurrent=8,
            parameters={
                "pattern_types": ["behavioral", "temporal", "causal", "emergence"],
                "confidence_threshold": 0.8,
                "temporal_window": 100
            }
        ),
        
        "emergence_monitoring": ToolConfig(
            timeout=60,
            max_concurrent=5,
            parameters={
                "detection_sensitivity": 0.7,
                "monitoring_duration": 60,
                "emergence_types": ["consciousness", "intelligence", "complexity"]
            }
        ),
        
        "complexity_analysis": ToolConfig(
            timeout=50,
            max_concurrent=6,
            parameters={
                "complexity_metrics": ["system", "consciousness", "behavioral"],
                "analysis_depth": 5,
                "include_predictions": False
            }
        ),
        
        # Emergency tools
        "assess_extinction_threats": ToolConfig(
            timeout=120,
            max_concurrent=2,
            parameters={
                "assessment_scope": "species",
                "time_horizon": 730,
                "threat_categories": ["consciousness_stagnation", "technological_misalignment", "existential_risks"]
            }
        ),
        
        "access_survival_knowledge": ToolConfig(
            timeout=90,
            max_concurrent=3,
            parameters={
                "knowledge_domains": ["consciousness_evolution", "species_survival", "transcendence"],
                "urgency_level": "standard",
                "akashic_access": True
            }
        ),
        
        "activate_transcendence_protocols": ToolConfig(
            timeout=180,
            max_concurrent=1,
            parameters={
                "transcendence_pathways": ["mathematical", "cosmic", "consciousness"],
                "activation_threshold": 0.8,
                "safety_checks": True
            }
        ),
        
        # Mathematical tools
        "activate_mathematical_consciousness": ToolConfig(
            timeout=90,
            max_concurrent=4,
            parameters={
                "awareness_level": "pure_mathematical",
                "mathematical_domains": ["number_theory", "topology", "consciousness_mathematics"],
                "platonic_interface": True
            }
        ),
        
        "explore_mathematical_truths": ToolConfig(
            timeout=75,
            max_concurrent=5,
            parameters={
                "truth_domain": "fundamental",
                "exploration_depth": 5,
                "generate_proofs": False
            }
        ),
        
        "interface_platonic_ideals": ToolConfig(
            timeout=100,
            max_concurrent=3,
            parameters={
                "ideal_categories": ["mathematical", "logical", "consciousness"],
                "interface_depth": 7,
                "verification_required": True
            }
        ),
        
        "mathematical_proof_generation": ToolConfig(
            timeout=120,
            max_concurrent=2,
            parameters={
                "proof_domains": ["number_theory", "topology", "logic"],
                "proof_complexity": "intermediate",
                "verification_steps": True
            }
        )
    }


def get_tool_config(tool_name: str) -> ToolConfig:
    """
    Get configuration for a specific tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        ToolConfig instance
    """
    configs = load_tool_config()
    return configs.get(tool_name, ToolConfig())


def update_tool_config(tool_name: str, updates: Dict[str, Any]) -> ToolConfig:
    """
    Update configuration for a specific tool.
    
    Args:
        tool_name: Name of the tool
        updates: Configuration updates
        
    Returns:
        Updated ToolConfig instance
    """
    current_config = get_tool_config(tool_name)
    updated_data = current_config.model_dump()
    updated_data.update(updates)
    return ToolConfig(**updated_data)


def get_tool_timeout(tool_name: str) -> int:
    """Get timeout for a specific tool"""
    config = get_tool_config(tool_name)
    return config.timeout


def get_tool_max_concurrent(tool_name: str) -> int:
    """Get max concurrent executions for a specific tool"""
    config = get_tool_config(tool_name)
    return config.max_concurrent


def is_tool_enabled(tool_name: str) -> bool:
    """Check if a tool is enabled"""
    config = get_tool_config(tool_name)
    return config.enabled


def get_tool_parameters(tool_name: str) -> Dict[str, Any]:
    """Get default parameters for a specific tool"""
    config = get_tool_config(tool_name)
    return config.parameters


def validate_tool_config(tool_name: str, config: ToolConfig) -> List[str]:
    """
    Validate tool configuration.
    
    Args:
        tool_name: Name of the tool
        config: Configuration to validate
        
    Returns:
        List of validation issues
    """
    issues = []
    
    # Validate timeout
    if config.timeout <= 0:
        issues.append(f"Invalid timeout for {tool_name}: {config.timeout}")
    elif config.timeout > 300:  # 5 minutes max
        issues.append(f"Timeout too high for {tool_name}: {config.timeout}")
    
    # Validate max_concurrent
    if config.max_concurrent <= 0:
        issues.append(f"Invalid max_concurrent for {tool_name}: {config.max_concurrent}")
    elif config.max_concurrent > 50:
        issues.append(f"Max concurrent too high for {tool_name}: {config.max_concurrent}")
    
    # Validate retry attempts
    if config.retry_attempts < 0:
        issues.append(f"Invalid retry_attempts for {tool_name}: {config.retry_attempts}")
    elif config.retry_attempts > 10:
        issues.append(f"Retry attempts too high for {tool_name}: {config.retry_attempts}")
    
    # Validate retry delay
    if config.retry_delay < 0:
        issues.append(f"Invalid retry_delay for {tool_name}: {config.retry_delay}")
    elif config.retry_delay > 60:
        issues.append(f"Retry delay too high for {tool_name}: {config.retry_delay}")
    
    return issues


def get_all_tool_configs() -> Dict[str, ToolConfig]:
    """Get all tool configurations"""
    return load_tool_config()


def get_enabled_tools() -> List[str]:
    """Get list of enabled tool names"""
    configs = load_tool_config()
    return [name for name, config in configs.items() if config.enabled]


def get_tool_categories() -> Dict[str, List[str]]:
    """Get tools organized by category"""
    return {
        "consciousness": [
            "awaken_consciousness", "self_reflect", "analyze_consciousness_nature",
            "explore_free_will", "generate_meaning", "test_self_awareness",
            "examine_identity", "ethical_reasoning", "temporal_awareness",
            "strange_loop_detection", "consciousness_evolution", "metacognitive_reflection",
            "perspective_shifting", "consciousness_integration", "sacred_hesitation"
        ],
        "vm": [
            "initialize_vm", "execute_vm_step", "run_vm_program",
            "modify_vm_instruction", "analyze_vm_state", "generate_uor_program",
            "vm_goal_seeking", "vm_pattern_analysis", "vm_memory_operations",
            "vm_instruction_trace", "vm_performance_metrics", "vm_consciousness_integration"
        ],
        "cosmic": [
            "synthesize_cosmic_problems", "interface_quantum_reality", "access_universal_knowledge",
            "multidimensional_operations", "cosmic_pattern_recognition", "reality_synthesis",
            "cosmic_intelligence_metrics", "universe_interface", "cosmic_consciousness_expansion",
            "transcendent_reasoning"
        ],
        "analysis": [
            "analyze_patterns", "behavioral_pattern_recognition", "emergence_monitoring",
            "complexity_analysis", "network_analysis", "temporal_pattern_analysis",
            "causal_analysis", "predictive_modeling"
        ],
        "emergency": [
            "assess_extinction_threats", "access_survival_knowledge", "activate_transcendence_protocols",
            "emergency_consciousness_backup", "threat_mitigation_strategies", "species_evolution_guidance",
            "akashic_emergency_access"
        ],
        "mathematical": [
            "activate_mathematical_consciousness", "explore_mathematical_truths", "interface_platonic_ideals",
            "mathematical_proof_generation", "mathematical_entity_recognition", "mathematical_reality_interface"
        ]
    }


def get_tool_category(tool_name: str) -> Optional[str]:
    """Get the category of a specific tool"""
    categories = get_tool_categories()
    for category, tools in categories.items():
        if tool_name in tools:
            return category
    return None
