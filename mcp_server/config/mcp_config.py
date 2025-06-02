"""
MCP server configuration management.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from pathlib import Path


class SecurityConfig(BaseModel):
    """Security configuration"""
    authentication: bool = True
    rate_limiting: bool = True
    max_requests_per_minute: int = 100
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])
    api_key_required: bool = False
    session_timeout_minutes: int = 60


class ToolsConfig(BaseModel):
    """Tools configuration"""
    consciousness: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 5,
        "timeout": 30
    })
    vm: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 10,
        "timeout": 15
    })
    cosmic: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 3,
        "timeout": 60
    })
    analysis: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 8,
        "timeout": 45
    })
    emergency: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 2,
        "timeout": 120
    })
    mathematical: Dict[str, Any] = Field(default_factory=lambda: {
        "enabled": True,
        "max_concurrent": 4,
        "timeout": 90
    })


class ResourcesConfig(BaseModel):
    """Resources configuration"""
    consciousness: Dict[str, Any] = Field(default_factory=lambda: {
        "cache_ttl": 300,
        "max_size": "100MB"
    })
    vm: Dict[str, Any] = Field(default_factory=lambda: {
        "cache_ttl": 60,
        "max_size": "50MB"
    })
    system: Dict[str, Any] = Field(default_factory=lambda: {
        "cache_ttl": 30,
        "max_size": "25MB"
    })
    knowledge: Dict[str, Any] = Field(default_factory=lambda: {
        "cache_ttl": 3600,
        "max_size": "500MB"
    })


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    file_path: Optional[str] = None
    json_format: bool = False
    console_output: bool = True
    max_file_size: str = "100MB"
    backup_count: int = 5


class PerformanceConfig(BaseModel):
    """Performance configuration"""
    max_memory_usage: str = "1GB"
    max_cpu_usage: float = 0.8
    connection_pool_size: int = 10
    request_timeout: int = 300
    keepalive_timeout: int = 60


class MCPConfig(BaseModel):
    """Main MCP server configuration"""
    name: str = "uor-consciousness"
    version: str = "1.0.0"
    description: str = "MCP Server for UOR Evolution Consciousness System"
    
    # Server settings
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    
    # Capabilities
    capabilities: Dict[str, bool] = Field(default_factory=lambda: {
        "tools": True,
        "resources": True,
        "prompts": True,
        "logging": True
    })
    
    # Component configurations
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    tools: ToolsConfig = Field(default_factory=ToolsConfig)
    resources: ResourcesConfig = Field(default_factory=ResourcesConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    
    # UOR system integration
    uor_config_path: str = "config.yaml"
    uor_session_dir: str = "sessions"
    uor_results_dir: str = "results"
    
    # Custom settings
    custom_settings: Dict[str, Any] = Field(default_factory=dict)


def load_mcp_config(config_path: Optional[str] = None) -> MCPConfig:
    """
    Load MCP configuration from file or environment variables.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        MCPConfig instance
    """
    config_data = {}
    
    # Load from file if provided
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config_data = yaml.safe_load(f)
            else:
                import json
                config_data = json.load(f)
    
    # Override with environment variables
    env_overrides = _get_env_overrides()
    config_data.update(env_overrides)
    
    return MCPConfig(**config_data)


def _get_env_overrides() -> Dict[str, Any]:
    """Get configuration overrides from environment variables"""
    overrides = {}
    
    # Server settings
    if os.getenv('MCP_HOST'):
        overrides['host'] = os.getenv('MCP_HOST')
    if os.getenv('MCP_PORT'):
        overrides['port'] = int(os.getenv('MCP_PORT'))
    if os.getenv('MCP_DEBUG'):
        overrides['debug'] = os.getenv('MCP_DEBUG').lower() == 'true'
    
    # Logging
    if os.getenv('MCP_LOG_LEVEL'):
        overrides.setdefault('logging', {})['level'] = os.getenv('MCP_LOG_LEVEL')
    if os.getenv('MCP_LOG_FILE'):
        overrides.setdefault('logging', {})['file_path'] = os.getenv('MCP_LOG_FILE')
    if os.getenv('MCP_LOG_JSON'):
        overrides.setdefault('logging', {})['json_format'] = os.getenv('MCP_LOG_JSON').lower() == 'true'
    
    # Security
    if os.getenv('MCP_AUTH_REQUIRED'):
        overrides.setdefault('security', {})['authentication'] = os.getenv('MCP_AUTH_REQUIRED').lower() == 'true'
    if os.getenv('MCP_RATE_LIMIT'):
        overrides.setdefault('security', {})['rate_limiting'] = os.getenv('MCP_RATE_LIMIT').lower() == 'true'
    if os.getenv('MCP_MAX_REQUESTS'):
        overrides.setdefault('security', {})['max_requests_per_minute'] = int(os.getenv('MCP_MAX_REQUESTS'))
    
    # UOR integration
    if os.getenv('UOR_CONFIG_PATH'):
        overrides['uor_config_path'] = os.getenv('UOR_CONFIG_PATH')
    if os.getenv('UOR_SESSION_DIR'):
        overrides['uor_session_dir'] = os.getenv('UOR_SESSION_DIR')
    if os.getenv('UOR_RESULTS_DIR'):
        overrides['uor_results_dir'] = os.getenv('UOR_RESULTS_DIR')
    
    return overrides


def create_default_config_file(output_path: str = "mcp_config.yaml") -> None:
    """
    Create a default configuration file.
    
    Args:
        output_path: Path where to save the configuration file
    """
    default_config = MCPConfig()
    config_dict = default_config.model_dump()
    
    with open(output_path, 'w') as f:
        yaml.dump(config_dict, f, default_flow_style=False, indent=2)
    
    print(f"Default MCP configuration saved to: {output_path}")


def validate_config(config: MCPConfig) -> List[str]:
    """
    Validate configuration and return list of issues.
    
    Args:
        config: Configuration to validate
        
    Returns:
        List of validation issues (empty if valid)
    """
    issues = []
    
    # Validate port range
    if not (1 <= config.port <= 65535):
        issues.append(f"Invalid port number: {config.port}")
    
    # Validate log level
    valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if config.logging.level.upper() not in valid_log_levels:
        issues.append(f"Invalid log level: {config.logging.level}")
    
    # Validate file paths
    if config.logging.file_path:
        log_dir = os.path.dirname(config.logging.file_path)
        if log_dir and not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create log directory: {e}")
    
    # Validate UOR config path
    if not os.path.exists(config.uor_config_path):
        issues.append(f"UOR config file not found: {config.uor_config_path}")
    
    # Validate timeout values
    for tool_category, tool_config in config.tools.model_dump().items():
        if isinstance(tool_config, dict) and 'timeout' in tool_config:
            if tool_config['timeout'] <= 0:
                issues.append(f"Invalid timeout for {tool_category}: {tool_config['timeout']}")
    
    # Validate concurrent limits
    for tool_category, tool_config in config.tools.model_dump().items():
        if isinstance(tool_config, dict) and 'max_concurrent' in tool_config:
            if tool_config['max_concurrent'] <= 0:
                issues.append(f"Invalid max_concurrent for {tool_category}: {tool_config['max_concurrent']}")
    
    return issues


def get_config_summary(config: MCPConfig) -> Dict[str, Any]:
    """
    Get a summary of the configuration for logging/debugging.
    
    Args:
        config: Configuration to summarize
        
    Returns:
        Configuration summary
    """
    return {
        "server": {
            "name": config.name,
            "version": config.version,
            "host": config.host,
            "port": config.port,
            "debug": config.debug
        },
        "capabilities": config.capabilities,
        "tools_enabled": {
            category: tool_config.get("enabled", False) 
            for category, tool_config in config.tools.model_dump().items()
            if isinstance(tool_config, dict)
        },
        "security": {
            "authentication": config.security.authentication,
            "rate_limiting": config.security.rate_limiting,
            "max_requests_per_minute": config.security.max_requests_per_minute
        },
        "logging": {
            "level": config.logging.level,
            "file_enabled": config.logging.file_path is not None,
            "json_format": config.logging.json_format
        },
        "uor_integration": {
            "config_path": config.uor_config_path,
            "session_dir": config.uor_session_dir,
            "results_dir": config.uor_results_dir
        }
    }


if __name__ == "__main__":
    # Create default config file when run directly
    create_default_config_file()
