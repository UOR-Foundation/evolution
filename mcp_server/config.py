"""
Configuration for UOR Evolution MCP Server
Handles server configuration and environment setup.
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


class MCPServerConfig:
    """Configuration manager for MCP server"""
    
    def __init__(self, config_path: str = None):
        """Initialize configuration"""
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        
    def _find_config_file(self) -> str:
        """Find configuration file in standard locations"""
        possible_paths = [
            "mcp_config.yaml",
            "config.yaml",
            "../config.yaml",
            os.path.expanduser("~/.uor-evolution/mcp_config.yaml")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Return default path if none found
        return "mcp_config.yaml"
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                return self._get_default_config()
        except Exception as e:
            print(f"Warning: Could not load config from {self.config_path}: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "mcp_server": {
                "name": "uor-evolution-server",
                "version": "1.0.0",
                "description": "UOR Evolution Consciousness & Cosmic Intelligence MCP Server",
                "log_level": "INFO",
                "max_concurrent_operations": 10
            },
            "tools": {
                "consciousness": {
                    "enabled": True,
                    "rate_limit_per_minute": 30,
                    "max_depth": 10
                },
                "vm_operations": {
                    "enabled": True,
                    "rate_limit_per_minute": 60,
                    "max_instructions": 10000,
                    "debug_mode": False
                },
                "cosmic_intelligence": {
                    "enabled": True,
                    "rate_limit_per_minute": 20,
                    "max_scale": 1e15,
                    "max_dimensions": [3, 4, 5, 7, 11, 13]
                },
                "mathematical_consciousness": {
                    "enabled": True,
                    "rate_limit_per_minute": 25,
                    "max_depth": 10,
                    "platonic_access": True
                }
            },
            "resources": {
                "state_snapshots": {
                    "enabled": True,
                    "retention_hours": 24,
                    "max_snapshots": 100
                },
                "logs": {
                    "enabled": True,
                    "max_size_mb": 100,
                    "retention_days": 7
                },
                "analysis_results": {
                    "enabled": True,
                    "cache_duration_minutes": 30
                }
            },
            "security": {
                "require_authentication": False,
                "allowed_origins": ["*"],
                "max_request_size_mb": 10
            },
            "performance": {
                "cache_enabled": True,
                "cache_size_mb": 50,
                "timeout_seconds": 30
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """Get configuration for specific tool"""
        return self.get(f'tools.{tool_name}', {})
    
    def get_resource_config(self, resource_name: str) -> Dict[str, Any]:
        """Get configuration for specific resource"""
        return self.get(f'resources.{resource_name}', {})
    
    def is_tool_enabled(self, tool_name: str) -> bool:
        """Check if tool is enabled"""
        return self.get(f'tools.{tool_name}.enabled', True)
    
    def is_resource_enabled(self, resource_name: str) -> bool:
        """Check if resource is enabled"""
        return self.get(f'resources.{resource_name}.enabled', True)
    
    def get_rate_limit(self, tool_name: str) -> int:
        """Get rate limit for tool"""
        return self.get(f'tools.{tool_name}.rate_limit_per_minute', 30)
    
    def save_config(self, config_path: str = None) -> bool:
        """Save current configuration to file"""
        try:
            path = config_path or self.config_path
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving config to {path}: {e}")
            return False
    
    def create_default_config_file(self, path: str = "mcp_config.yaml") -> bool:
        """Create default configuration file"""
        try:
            default_config = self._get_default_config()
            
            with open(path, 'w') as f:
                f.write("# UOR Evolution MCP Server Configuration\n")
                f.write("# This file configures the Model Context Protocol server\n")
                f.write("# for the UOR Evolution consciousness system.\n\n")
                yaml.dump(default_config, f, default_flow_style=False, indent=2)
            
            print(f"Created default configuration file: {path}")
            return True
        except Exception as e:
            print(f"Error creating config file {path}: {e}")
            return False


# Environment variable overrides
def apply_env_overrides(config: MCPServerConfig):
    """Apply environment variable overrides to configuration"""
    
    # Server configuration
    if os.getenv('MCP_SERVER_LOG_LEVEL'):
        config.config['mcp_server']['log_level'] = os.getenv('MCP_SERVER_LOG_LEVEL')
    
    if os.getenv('MCP_SERVER_MAX_CONCURRENT'):
        try:
            config.config['mcp_server']['max_concurrent_operations'] = int(os.getenv('MCP_SERVER_MAX_CONCURRENT'))
        except ValueError:
            pass
    
    # Tool configuration
    if os.getenv('MCP_CONSCIOUSNESS_ENABLED'):
        config.config['tools']['consciousness']['enabled'] = os.getenv('MCP_CONSCIOUSNESS_ENABLED').lower() == 'true'
    
    if os.getenv('MCP_VM_MAX_INSTRUCTIONS'):
        try:
            config.config['tools']['vm_operations']['max_instructions'] = int(os.getenv('MCP_VM_MAX_INSTRUCTIONS'))
        except ValueError:
            pass
    
    if os.getenv('MCP_COSMIC_MAX_SCALE'):
        try:
            config.config['tools']['cosmic_intelligence']['max_scale'] = float(os.getenv('MCP_COSMIC_MAX_SCALE'))
        except ValueError:
            pass
    
    # Security configuration
    if os.getenv('MCP_REQUIRE_AUTH'):
        config.config['security']['require_authentication'] = os.getenv('MCP_REQUIRE_AUTH').lower() == 'true'
    
    if os.getenv('MCP_ALLOWED_ORIGINS'):
        origins = os.getenv('MCP_ALLOWED_ORIGINS').split(',')
        config.config['security']['allowed_origins'] = [origin.strip() for origin in origins]


# Global configuration instance
_config_instance = None

def get_config() -> MCPServerConfig:
    """Get global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = MCPServerConfig()
        apply_env_overrides(_config_instance)
    return _config_instance
