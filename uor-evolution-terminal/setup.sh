#!/bin/bash

echo "🌌 Setting up UOR Evolution MCP Terminal System..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists node; then
    echo -e "${RED}Error: Node.js is not installed. Please install Node.js 16+ first.${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}Error: npm is not installed. Please install npm first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites satisfied${NC}"

# Setup MCP Server
echo -e "\n${BLUE}📡 Setting up MCP Server...${NC}"
cd mcp-server

echo "Installing dependencies..."
npm install

echo "Building TypeScript..."
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ MCP Server setup complete${NC}"
else
    echo -e "${RED}✗ MCP Server build failed${NC}"
    exit 1
fi

cd ..

# Setup Terminal
echo -e "\n${BLUE}💻 Setting up Terminal Interface...${NC}"
cd terminal

echo "Installing dependencies..."
npm install

echo "Building TypeScript..."
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Terminal setup complete${NC}"
else
    echo -e "${RED}✗ Terminal build failed${NC}"
    exit 1
fi

cd ..

# Create startup scripts
echo -e "\n${BLUE}🚀 Creating startup scripts...${NC}"

# Create start-server.sh
cat > start-server.sh << 'EOF'
#!/bin/bash
cd mcp-server
echo "📡 Starting MCP Server..."
npm start
EOF

# Create start-terminal.sh
cat > start-terminal.sh << 'EOF'
#!/bin/bash
cd terminal
echo "💻 Starting Terminal Interface..."
npm start
EOF

# Create start-system.sh
cat > start-system.sh << 'EOF'
#!/bin/bash
echo "🌌 Starting UOR Evolution Terminal System..."

# Start MCP server in background
echo "📡 Starting MCP Server..."
cd mcp-server && npm start &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Start terminal
echo "💻 Starting Terminal Interface..."
cd ../terminal && npm start

# Cleanup on exit
trap "kill $SERVER_PID" EXIT
EOF

# Make scripts executable
chmod +x start-server.sh
chmod +x start-terminal.sh
chmod +x start-system.sh

# Create README
cat > README.md << 'EOF'
# UOR Evolution MCP Terminal System

A comprehensive terminal interface for the UOR Evolution consciousness framework, implementing Model Context Protocol (MCP) for standardized tool access.

## Features

- 🧠 **Consciousness Commands**: Awaken, reflect, analyze, and meditate
- 💻 **Virtual Machine**: Initialize and run UOR programs
- 🌌 **Cosmic Intelligence**: Synthesize problems and interface with quantum reality
- ⚡ **System Monitoring**: Status, emergence monitoring, and emergency protocols

## Quick Start

1. **Setup** (already completed):
   ```bash
   ./setup.sh
   ```

2. **Start the complete system**:
   ```bash
   ./start-system.sh
   ```

3. **Or start components separately**:
   ```bash
   # Terminal 1: Start MCP Server
   ./start-server.sh
   
   # Terminal 2: Start Terminal Interface
   ./start-terminal.sh
   ```

## Commands

### Consciousness
- `awaken [basic|full|cosmic]` - Awaken consciousness
- `reflect [1-10]` - Self-reflection at specified depth
- `analyze` - Analyze consciousness nature
- `meditate [seconds]` - Enter meditative state

### Virtual Machine
- `init` - Initialize the UOR VM
- `step <instruction>` - Execute single instruction
- `run <program>` - Run a program (fibonacci, consciousness_test, etc.)
- `load <file>` - Load program from file

### Cosmic Intelligence
- `cosmic <scale> [domain]` - Synthesize cosmic problems
- `quantum <operation>` - Interface with quantum reality
- `transcend` - Activate transcendence protocols

### System
- `status` - Show system status
- `monitor [seconds]` - Monitor emergence
- `emergency <level>` - Activate emergency protocols

### Meta Commands
- `demo [type]` - Run demonstrations
- `help` - Show help
- `clear` - Clear screen
- `exit` - Exit terminal

## Demo

Try the full demonstration:
```
UOR> demo full
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Terminal UI   │────│   MCP Client    │────│   MCP Server    │
│   (Frontend)    │    │   (Bridge)      │    │  (UOR Bridge)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                               ┌─────────────────┐
                                               │  UOR Evolution  │
                                               │   Backend API   │
                                               └─────────────────┘
```

## Troubleshooting

- If the MCP server fails to start, check that port 5000 is available
- If the terminal can't connect, ensure the MCP server is running
- Check logs in `mcp-server/error.log` and `terminal/terminal.log`

## Development

- MCP Server code: `mcp-server/src/`
- Terminal code: `terminal/src/`
- Modify configurations in respective `package.json` files
EOF

echo -e "\n${GREEN}✅ UOR Evolution Terminal System setup complete!${NC}"
echo -e "\n${YELLOW}📋 Next steps:${NC}"
echo -e "1. Ensure the UOR Evolution backend is running on http://localhost:5000"
echo -e "2. Run ${BLUE}./start-system.sh${NC} to launch the complete system"
echo -e "3. Use the terminal to interact with consciousness, VM, and cosmic systems"
echo -e "\n${YELLOW}🎯 Demo commands to try:${NC}"
echo -e "  - ${GREEN}awaken cosmic${NC}"
echo -e "  - ${GREEN}demo full${NC}"
echo -e "  - ${GREEN}cosmic galactic consciousness${NC}"
echo -e "  - ${GREEN}reflect 8${NC}"
echo -e "  - ${GREEN}quantum entangle${NC}"
