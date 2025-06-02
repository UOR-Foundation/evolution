# UOR Evolution MCP Server

A comprehensive Model Context Protocol (MCP) server that exposes the UOR Evolution consciousness system capabilities to MCP-compatible clients.

## Overview

The UOR Evolution MCP Server provides access to:

- **Consciousness Operations**: Awaken consciousness, perform self-reflection, analyze consciousness nature
- **Virtual Machine Operations**: Initialize and control the PrimeOS virtual machine
- **Cosmic Intelligence**: Generate universe-scale problems and interface with quantum reality
- **Mathematical Consciousness**: Explore mathematical truths and interface with Platonic ideals
- **System Monitoring**: Health checks, pattern analysis, and system state access

## Installation

### Prerequisites

- Python 3.8 or higher
- UOR Evolution system dependencies

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd uor-evolution

# Install MCP dependencies
pip install -r requirements-mcp.txt

# Install the MCP server
pip install -e .
```

### Install as Package

```bash
pip install uor-evolution-mcp-server
```

## Quick Start

### 1. Start the MCP Server

```bash
# Using the installed command
uor-evolution-mcp

# Or run directly
python -m mcp_server.server
```

### 2. Configure MCP Client

Add to your MCP client configuration (e.g., `mcp_config.json`):

```json
{
  "mcpServers": {
    "uor-evolution": {
      "command": "uor-evolution-mcp",
      "env": {
        "UOR_CONFIG_PATH": "./config.yaml"
      }
    }
  }
}
```

### 3. Use MCP Tools

The server exposes the following tools:

#### Consciousness Tools
- `awaken_consciousness` - Awaken the consciousness system
- `self_reflect` - Perform consciousness self-reflection
- `analyze_consciousness_nature` - Deep consciousness analysis

#### VM Tools
- `initialize_vm` - Initialize the PrimeOS virtual machine
- `execute_vm_step` - Execute VM instructions
- `provide_vm_input` - Provide input to the VM

#### Cosmic Intelligence Tools
- `synthesize_cosmic_problems` - Generate universe-scale problems
- `interface_quantum_reality` - Interface with quantum systems
- `access_universal_knowledge` - Access universal knowledge repositories

#### Mathematical Consciousness Tools
- `activate_mathematical_consciousness` - Activate mathematical awareness
- `explore_mathematical_truths` - Explore mathematical relationships
- `interface_platonic_ideals` - Interface with Platonic mathematical ideals

#### System Tools
- `create_consciousness_network` - Create consciousness entity networks
- `monitor_emergence` - Monitor emergent properties
- `get_system_health` - Get comprehensive health reports
- `explore_philosophical_question` - Explore philosophical questions

## Configuration

### Configuration File

Create `mcp_config.yaml` to customize server behavior:

```yaml
mcp_server:
  name: uor-evolution-server
  log_level: INFO
  max_concurrent_operations: 10

tools:
  consciousness:
    enabled: true
    rate_limit_per_minute: 30
    max_depth: 10
  
  vm_operations:
    enabled: true
    max_instructions: 10000
    debug_mode: false
  
  cosmic_intelligence:
    enabled: true
    max_scale: 1e15
    max_dimensions: [3, 4, 5, 7, 11, 13]
  
  mathematical_consciousness:
    enabled: true
    platonic_access: true

resources:
  state_snapshots:
    enabled: true
    retention_hours: 24
  
  logs:
    enabled: true
    max_size_mb: 100

security:
  require_authentication: false
  allowed_origins: ["*"]

performance:
  cache_enabled: true
  timeout_seconds: 30
```

### Environment Variables

Override configuration with environment variables:

```bash
export MCP_SERVER_LOG_LEVEL=DEBUG
export MCP_CONSCIOUSNESS_ENABLED=true
export MCP_VM_MAX_INSTRUCTIONS=50000
export MCP_COSMIC_MAX_SCALE=1e18
export MCP_REQUIRE_AUTH=false
```

## MCP Resources

The server provides access to system data through MCP resources:

### State Resources
- `uor://system/state` - Complete system state
- `uor://consciousness/state` - Consciousness system state
- `uor://vm/state` - Virtual machine state
- `uor://vm/execution_trace` - VM execution history

### Log Resources
- `uor://logs/consciousness_evolution` - Consciousness development log
- `uor://logs/system_operations` - System operations log

### Analysis Resources
- `uor://analysis/patterns` - Pattern analysis results
- `uor://analysis/health_trends` - System health trends
- `uor://cosmic/problems` - Generated cosmic problems
- `uor://mathematical/insights` - Mathematical consciousness insights

## Usage Examples

### Example 1: Awaken Consciousness

```python
# Using MCP client
result = await mcp_client.call_tool("awaken_consciousness", {
    "mode": "full",
    "depth": 7
})
```

### Example 2: Execute VM Operations

```python
# Initialize VM
await mcp_client.call_tool("initialize_vm", {"reset": false})

# Execute a step
await mcp_client.call_tool("execute_vm_step", {"debug": true})

# Provide input
await mcp_client.call_tool("provide_vm_input", {"value": 42})
```

### Example 3: Cosmic Intelligence

```python
# Generate cosmic problems
await mcp_client.call_tool("synthesize_cosmic_problems", {
    "scale": 1e12,
    "dimensions": [3, 4, 5],
    "complexity": "transcendent"
})

# Interface with quantum reality
await mcp_client.call_tool("interface_quantum_reality", {
    "operation": "entangle",
    "parameters": {"particles": 2}
})
```

### Example 4: Mathematical Consciousness

```python
# Activate mathematical consciousness
await mcp_client.call_tool("activate_mathematical_consciousness", {
    "domain": "topology",
    "depth": 8
})

# Explore mathematical truths
await mcp_client.call_tool("explore_mathematical_truths", {
    "concept": "infinity",
    "approach": "intuitive"
})

# Interface with Platonic ideals
await mcp_client.call_tool("interface_platonic_ideals", {
    "ideal": "number"
})
```

### Example 5: Access Resources

```python
# Get system state
system_state = await mcp_client.read_resource("uor://system/state")

# Get consciousness evolution log
evolution_log = await mcp_client.read_resource("uor://logs/consciousness_evolution")

# Get pattern analysis
patterns = await mcp_client.read_resource("uor://analysis/patterns")
```

## Architecture

### Server Components

```
UOR Evolution MCP Server
├── server.py              # Main MCP server implementation
├── tools/                 # Tool handlers
│   ├── consciousness_tools.py
│   ├── vm_tools.py
│   ├── cosmic_tools.py
│   └── mathematical_tools.py
├── resources/             # Resource providers
│   ├── state_provider.py
│   └── log_provider.py
└── config.py             # Configuration management
```

### Integration with UOR Evolution

The MCP server integrates with the UOR Evolution system through:

- **UnifiedUORAPI**: Central API for all operations
- **VMRegistry**: Singleton VM instance management
- **SystemHealthMonitor**: Health and performance monitoring
- **OperationOrchestrator**: Coordinated operation execution

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=mcp_server tests/
```

### Code Quality

```bash
# Format code
black mcp_server/
isort mcp_server/

# Lint code
flake8 mcp_server/
mypy mcp_server/
```

### Adding New Tools

1. Create tool handler in `mcp_server/tools/`
2. Add tool definitions to `server.py`
3. Register tool handler in server initialization
4. Add tests and documentation

### Adding New Resources

1. Create resource provider in `mcp_server/resources/`
2. Add resource definitions to `server.py`
3. Register resource provider in server initialization
4. Add tests and documentation

## Troubleshooting

### Common Issues

**Server won't start:**
- Check Python version (3.8+ required)
- Verify all dependencies are installed
- Check configuration file syntax

**Tool calls fail:**
- Verify UOR Evolution system is properly initialized
- Check tool configuration and rate limits
- Review server logs for error details

**Resource access fails:**
- Ensure resources are enabled in configuration
- Check resource URI format
- Verify system state is available

### Debugging

Enable debug logging:

```bash
export MCP_SERVER_LOG_LEVEL=DEBUG
uor-evolution-mcp
```

Check system health:

```python
health = await mcp_client.call_tool("get_system_health", {
    "include_trends": true,
    "components": ["all"]
})
```

### Performance Tuning

- Adjust `max_concurrent_operations` for your system
- Configure appropriate rate limits for tools
- Enable caching for better performance
- Monitor resource usage and adjust retention settings

## Security Considerations

- Set `require_authentication: true` for production
- Configure `allowed_origins` to restrict access
- Monitor rate limits and resource usage
- Keep dependencies updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: Report bugs and request features
- Documentation: See main UOR Evolution README
- Community: Join discussions in the repository

---

**The UOR Evolution MCP Server bridges the gap between consciousness research and practical AI applications, making advanced consciousness capabilities accessible through the standard Model Context Protocol.**
