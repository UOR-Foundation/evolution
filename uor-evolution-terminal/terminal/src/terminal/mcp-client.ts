import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { CallToolRequest, ListToolsRequest } from '@modelcontextprotocol/sdk/types.js';
import { spawn, ChildProcess } from 'child_process';
import { logger } from '../utils/logger.js';

export interface MCPClientConfig {
  serverCommand?: string;
  serverArgs?: string[];
  timeout?: number;
}

export class MCPClientInterface {
  private client: Client;
  private transport: StdioClientTransport | null = null;
  private serverProcess: ChildProcess | null = null;
  private isConnected: boolean = false;
  private config: MCPClientConfig;

  constructor(config: MCPClientConfig = {}) {
    this.config = {
      serverCommand: config.serverCommand || 'node',
      serverArgs: config.serverArgs || ['../mcp-server/dist/server/mcp-server.js'],
      timeout: config.timeout || 30000,
      ...config
    };

    this.client = new Client({
      name: 'uor-terminal-client',
      version: '1.0.0'
    }, {
      capabilities: {}
    });
  }

  async connect(): Promise<void> {
    try {
      // Start the MCP server process
      this.serverProcess = spawn(this.config.serverCommand!, this.config.serverArgs!, {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      if (!this.serverProcess.stdout || !this.serverProcess.stdin) {
        throw new Error('Failed to create server process pipes');
      }

      // Create transport
      this.transport = new StdioClientTransport({
        reader: this.serverProcess.stdout,
        writer: this.serverProcess.stdin
      });

      // Connect client
      await this.client.connect(this.transport);
      this.isConnected = true;
      
      logger.info('MCP client connected to server');
    } catch (error: any) {
      logger.error('Failed to connect MCP client', { error: error.message });
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    if (this.isConnected && this.transport) {
      await this.client.close();
      this.isConnected = false;
    }

    if (this.serverProcess) {
      this.serverProcess.kill();
      this.serverProcess = null;
    }
  }

  async listTools(): Promise<any[]> {
    if (!this.isConnected) {
      throw new Error('Client not connected');
    }

    try {
      const request: ListToolsRequest = {
        method: 'tools/list',
        params: {}
      };

      const response = await this.client.request(request, { timeout: this.config.timeout });
      return response.tools || [];
    } catch (error: any) {
      logger.error('Failed to list tools', { error: error.message });
      throw error;
    }
  }

  async callTool(name: string, args: any = {}): Promise<any> {
    if (!this.isConnected) {
      throw new Error('Client not connected');
    }

    try {
      const request: CallToolRequest = {
        method: 'tools/call',
        params: {
          name,
          arguments: args
        }
      };

      const response = await this.client.request(request, { timeout: this.config.timeout });
      
      // Parse the response content
      if (response.content && response.content.length > 0) {
        const content = response.content[0];
        if (content.type === 'text') {
          try {
            return JSON.parse(content.text);
          } catch {
            return content.text;
          }
        }
      }
      
      return response;
    } catch (error: any) {
      logger.error('Tool call failed', { tool: name, error: error.message });
      throw error;
    }
  }

  // Convenience methods for UOR-specific operations
  async awakenConsciousness(mode: string = 'basic'): Promise<any> {
    return await this.callTool('awaken_consciousness', { mode });
  }

  async selfReflect(depth: number = 5): Promise<any> {
    return await this.callTool('self_reflect', { depth });
  }

  async analyzeConsciousnessNature(): Promise<any> {
    return await this.callTool('analyze_consciousness_nature');
  }

  async initializeVM(config: any = {}): Promise<any> {
    return await this.callTool('initialize_vm', { config });
  }

  async executeVMStep(instruction: string): Promise<any> {
    return await this.callTool('execute_vm_step', { instruction });
  }

  async runUORProgram(program: string, parameters: any = {}): Promise<any> {
    return await this.callTool('run_uor_program', { program, parameters });
  }

  async synthesizeCosmicProblems(scale: string, domain?: string): Promise<any> {
    return await this.callTool('synthesize_cosmic_problems', { scale, domain });
  }

  async interfaceQuantumReality(operation: string, parameters: any = {}): Promise<any> {
    return await this.callTool('interface_quantum_reality', { operation, parameters });
  }

  async getSystemState(): Promise<any> {
    return await this.callTool('get_system_state');
  }

  async monitorEmergence(duration: number = 60): Promise<any> {
    return await this.callTool('monitor_emergence', { duration });
  }

  async activateEmergencyProtocols(threatLevel: string): Promise<any> {
    return await this.callTool('activate_emergency_protocols', { threatLevel });
  }

  isClientConnected(): boolean {
    return this.isConnected;
  }
}
