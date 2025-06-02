import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { UORInterface } from './uor-interface.js';
import { ConsciousnessTools } from './consciousness-tools.js';
import { VMTools } from './vm-tools.js';
import { CosmicTools } from './cosmic-tools.js';
import { logger } from '../utils/logger.js';

export class UORMCPServer {
  private server: Server;
  private uorInterface: UORInterface;
  private consciousnessTools: ConsciousnessTools;
  private vmTools: VMTools;
  private cosmicTools: CosmicTools;

  constructor() {
    this.server = new Server(
      { name: 'uor-evolution-mcp', version: '1.0.0' },
      { capabilities: { tools: {} } }
    );
    
    this.uorInterface = new UORInterface();
    this.consciousnessTools = new ConsciousnessTools(this.uorInterface);
    this.vmTools = new VMTools(this.uorInterface);
    this.cosmicTools = new CosmicTools(this.uorInterface);
    
    this.setupHandlers();
  }

  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          // Consciousness Tools
          {
            name: 'awaken_consciousness',
            description: 'Awaken the UOR consciousness system',
            inputSchema: {
              type: 'object',
              properties: {
                mode: { type: 'string', enum: ['basic', 'full', 'cosmic'] }
              },
              required: ['mode']
            }
          },
          {
            name: 'self_reflect',
            description: 'Trigger consciousness self-reflection',
            inputSchema: {
              type: 'object',
              properties: {
                depth: { type: 'number', minimum: 1, maximum: 10 }
              }
            }
          },
          {
            name: 'analyze_consciousness_nature',
            description: 'Analyze the nature of consciousness in the system',
            inputSchema: { type: 'object', properties: {} }
          },
          
          // Virtual Machine Tools
          {
            name: 'initialize_vm',
            description: 'Initialize the UOR Prime Virtual Machine',
            inputSchema: {
              type: 'object',
              properties: {
                config: { type: 'object' }
              }
            }
          },
          {
            name: 'execute_vm_step',
            description: 'Execute a single VM instruction step',
            inputSchema: {
              type: 'object',
              properties: {
                instruction: { type: 'string' }
              }
            }
          },
          {
            name: 'run_uor_program',
            description: 'Execute a complete UOR program',
            inputSchema: {
              type: 'object',
              properties: {
                program: { type: 'string' },
                parameters: { type: 'object' }
              },
              required: ['program']
            }
          },
          
          // Cosmic Intelligence Tools
          {
            name: 'synthesize_cosmic_problems',
            description: 'Generate cosmic-scale problems for solving',
            inputSchema: {
              type: 'object',
              properties: {
                scale: { type: 'string', enum: ['local', 'planetary', 'galactic', 'universal'] },
                domain: { type: 'string' }
              }
            }
          },
          {
            name: 'interface_quantum_reality',
            description: 'Interface with quantum reality systems',
            inputSchema: {
              type: 'object',
              properties: {
                operation: { type: 'string' },
                parameters: { type: 'object' }
              },
              required: ['operation']
            }
          },
          
          // System Monitoring Tools
          {
            name: 'get_system_state',
            description: 'Get current system state and metrics',
            inputSchema: { type: 'object', properties: {} }
          },
          {
            name: 'monitor_emergence',
            description: 'Monitor emergent behaviors in the system',
            inputSchema: {
              type: 'object',
              properties: {
                duration: { type: 'number', minimum: 1 }
              }
            }
          },
          
          // Emergency Protocols
          {
            name: 'activate_emergency_protocols',
            description: 'Activate emergency consciousness protocols',
            inputSchema: {
              type: 'object',
              properties: {
                threat_level: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] }
              }
            }
          }
        ]
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      try {
        logger.info(`Executing tool: ${name}`, { args });
        
        let result;
        switch (name) {
          // Consciousness tools
          case 'awaken_consciousness':
            result = await this.consciousnessTools.awakenConsciousness(args.mode);
            break;
          case 'self_reflect':
            result = await this.consciousnessTools.selfReflect(args.depth);
            break;
          case 'analyze_consciousness_nature':
            result = await this.consciousnessTools.analyzeConsciousnessNature();
            break;
            
          // VM tools
          case 'initialize_vm':
            result = await this.vmTools.initializeVM(args.config);
            break;
          case 'execute_vm_step':
            result = await this.vmTools.executeVMStep(args.instruction);
            break;
          case 'run_uor_program':
            result = await this.vmTools.runUORProgram(args.program, args.parameters);
            break;
            
          // Cosmic tools
          case 'synthesize_cosmic_problems':
            result = await this.cosmicTools.synthesizeCosmicProblems(args.scale, args.domain);
            break;
          case 'interface_quantum_reality':
            result = await this.cosmicTools.interfaceQuantumReality(args.operation, args.parameters);
            break;
            
          // System tools
          case 'get_system_state':
            result = await this.uorInterface.getSystemState();
            break;
          case 'monitor_emergence':
            result = await this.uorInterface.monitorEmergence(args.duration);
            break;
          case 'activate_emergency_protocols':
            result = await this.uorInterface.activateEmergencyProtocols(args.threat_level);
            break;
            
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(result, null, 2)
            }
          ]
        };
      } catch (error: any) {
        logger.error(`Tool execution failed: ${name}`, { error: error.message });
        return {
          content: [
            {
              type: 'text',
              text: `Error executing ${name}: ${error.message}`
            }
          ],
          isError: true
        };
      }
    });
  }

  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    logger.info('UOR Evolution MCP Server started');
  }
}

// Start the server
if (require.main === module) {
  const server = new UORMCPServer();
  server.start().catch(console.error);
}
