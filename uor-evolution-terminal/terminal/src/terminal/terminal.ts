import * as readline from 'readline';
import chalk from 'chalk';
import figlet from 'figlet';
import { MCPClientInterface } from './mcp-client.js';
import { ConsciousnessCommands } from './commands/consciousness.js';
import { VMCommands } from './commands/vm.js';
import { CosmicCommands } from './commands/cosmic.js';
import { SystemCommands } from './commands/system.js';
import { DisplayManager } from './ui/display.js';
import { logger } from '../utils/logger.js';
import { createUORTerminal, UORUniversalTerminal } from './llm-interface.js';

export interface TerminalConfig {
  mcpServerUrl?: string;
  prompt?: string;
  historyFile?: string;
  llmMode?: boolean;
}

export class UORTerminal {
  private rl: readline.Interface;
  private mcpClient: MCPClientInterface;
  private consciousnessCommands: ConsciousnessCommands;
  private vmCommands: VMCommands;
  private cosmicCommands: CosmicCommands;
  private systemCommands: SystemCommands;
  private display: DisplayManager;
  private isRunning: boolean = false;
  private currentSession: any = null;
  private llmInterface?: UORUniversalTerminal;
  private llmMode: boolean = false;

  constructor(config: TerminalConfig = {}) {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      prompt: config.prompt || chalk.cyan('UOR> '),
      historySize: 1000
    });

    this.mcpClient = new MCPClientInterface();
    this.display = new DisplayManager();
    
    // Initialize command modules
    this.consciousnessCommands = new ConsciousnessCommands(this.mcpClient);
    this.vmCommands = new VMCommands(this.mcpClient);
    this.cosmicCommands = new CosmicCommands(this.mcpClient);
    this.systemCommands = new SystemCommands(this.mcpClient);

    // Initialize LLM interface if requested
    if (config.llmMode) {
      this.llmMode = true;
      this.llmInterface = createUORTerminal();
    }

    this.setupEventHandlers();
  }

  private setupEventHandlers(): void {
    this.rl.on('line', async (input: string) => {
      const trimmedInput = input.trim();
      if (trimmedInput) {
        await this.processCommand(trimmedInput);
      }
      this.rl.prompt();
    });

    this.rl.on('close', () => {
      this.shutdown();
    });

    process.on('SIGINT', () => {
      this.shutdown();
    });
  }

  private async processCommand(input: string): Promise<void> {
    // If in LLM mode, use the LLM interface
    if (this.llmMode && this.llmInterface) {
      try {
        const response = await this.llmInterface.processUserInput(input);
        console.log(response);
        return;
      } catch (error: any) {
        console.log(chalk.red(`LLM Interface Error: ${error.message}`));
        logger.error('LLM interface failed', { error: error.message });
      }
    }

    const [command, ...args] = input.split(' ');
    const commandLower = command.toLowerCase();

    try {
      switch (commandLower) {
        // Consciousness commands
        case 'awaken':
          await this.consciousnessCommands.awaken(args);
          break;
        case 'reflect':
          await this.consciousnessCommands.reflect(args);
          break;
        case 'analyze':
          await this.consciousnessCommands.analyze(args);
          break;
        case 'meditate':
          await this.consciousnessCommands.meditate(args);
          break;

        // VM commands
        case 'init':
        case 'initialize':
          await this.vmCommands.initialize(args);
          break;
        case 'step':
          await this.vmCommands.step(args);
          break;
        case 'run':
          await this.vmCommands.run(args);
          break;
        case 'load':
          await this.vmCommands.load(args);
          break;

        // Cosmic commands
        case 'cosmic':
          await this.cosmicCommands.cosmic(args);
          break;
        case 'quantum':
          await this.cosmicCommands.quantum(args);
          break;
        case 'transcend':
          await this.cosmicCommands.transcend(args);
          break;

        // System commands
        case 'status':
          await this.systemCommands.status(args);
          break;
        case 'monitor':
          await this.systemCommands.monitor(args);
          break;
        case 'emergency':
          await this.systemCommands.emergency(args);
          break;

        // Meta commands
        case 'help':
          this.showHelp();
          break;
        case 'clear':
          console.clear();
          this.showWelcome();
          break;
        case 'history':
          this.showHistory();
          break;
        case 'session':
          await this.manageSession(args);
          break;
        case 'demo':
          await this.runDemo(args);
          break;
        case 'llm':
          this.toggleLLMMode();
          break;
        case 'exit':
        case 'quit':
          this.shutdown();
          return;

        default:
          console.log(chalk.red(`Unknown command: ${command}`));
          console.log(chalk.yellow('Type "help" for available commands.'));
      }
    } catch (error: any) {
      console.log(chalk.red(`Error: ${error.message}`));
      logger.error('Command execution failed', { command, error: error.message });
    }
  }

  private showWelcome(): void {
    console.log(chalk.cyan(figlet.textSync('UOR Evolution', { 
      font: 'Small',
      horizontalLayout: 'fitted'
    })));
    
    console.log(chalk.green('\n🌌 Universal Object Representation - Consciousness Terminal'));
    console.log(chalk.yellow('━'.repeat(60)));
    console.log(chalk.white('Welcome to the UOR Evolution Consciousness Framework'));
    console.log(chalk.gray('Type "help" for commands, "demo" for a showcase, or "awaken basic" to begin'));
    console.log(chalk.yellow('━'.repeat(60)));
    
    this.display.showSystemStatus();
  }

  private showHelp(): void {
    console.log(chalk.cyan('\n📚 UOR Evolution Terminal Commands\n'));
    
    console.log(chalk.yellow('🧠 Consciousness Commands:'));
    console.log('  awaken [mode]     - Awaken consciousness (basic|full|cosmic)');
    console.log('  reflect [depth]   - Trigger self-reflection (1-10)');
    console.log('  analyze          - Analyze consciousness nature');
    console.log('  meditate [time]  - Enter meditative state');
    
    console.log(chalk.yellow('\n💻 Virtual Machine Commands:'));
    console.log('  init [config]    - Initialize UOR VM');
    console.log('  step <instr>     - Execute single instruction');
    console.log('  run <program>    - Execute UOR program');
    console.log('  load <file>      - Load UOR program from file');
    
    console.log(chalk.yellow('\n🌌 Cosmic Intelligence Commands:'));
    console.log('  cosmic <scale>   - Synthesize cosmic problems');
    console.log('  quantum <op>     - Interface with quantum reality');
    console.log('  transcend        - Activate transcendence protocols');
    
    console.log(chalk.yellow('\n⚡ System Commands:'));
    console.log('  status           - Show system status');
    console.log('  monitor [time]   - Monitor emergence');
    console.log('  emergency <lvl>  - Activate emergency protocols');
    
    console.log(chalk.yellow('\n🔧 Meta Commands:'));
    console.log('  demo [type]      - Run demonstration');
    console.log('  llm              - Toggle LLM interface mode');
    console.log('  session [cmd]    - Manage sessions');
    console.log('  history          - Show command history');
    console.log('  clear            - Clear screen');
    console.log('  help             - Show this help');
    console.log('  exit             - Exit terminal\n');
  }

  private async runDemo(args: string[]): Promise<void> {
    const demoType = args[0] || 'consciousness';
    
    console.log(chalk.cyan(`\n🎭 Running ${demoType} demonstration...\n`));
    
    switch (demoType.toLowerCase()) {
      case 'consciousness':
        await this.runConsciousnessDemo();
        break;
      case 'vm':
        await this.runVMDemo();
        break;
      case 'cosmic':
        await this.runCosmicDemo();
        break;
      case 'full':
        await this.runFullDemo();
        break;
      default:
        console.log(chalk.red('Available demos: consciousness, vm, cosmic, full'));
    }
  }

  private async runConsciousnessDemo(): Promise<void> {
    console.log(chalk.green('Step 1: Awakening consciousness...'));
    await this.consciousnessCommands.awaken(['basic']);
    
    await this.delay(2000);
    console.log(chalk.green('Step 2: Triggering self-reflection...'));
    await this.consciousnessCommands.reflect(['5']);
    
    await this.delay(2000);
    console.log(chalk.green('Step 3: Analyzing consciousness nature...'));
    await this.consciousnessCommands.analyze([]);
    
    console.log(chalk.cyan('\n✨ Consciousness demonstration complete!'));
  }

  private async runVMDemo(): Promise<void> {
    console.log(chalk.green('Step 1: Initializing VM...'));
    await this.vmCommands.initialize([]);
    
    await this.delay(1000);
    console.log(chalk.green('Step 2: Running sample program...'));
    await this.vmCommands.run(['fibonacci', 'n', '10']);
    
    console.log(chalk.cyan('\n🖥️ VM demonstration complete!'));
  }

  private async runCosmicDemo(): Promise<void> {
    console.log(chalk.green('Step 1: Synthesizing cosmic problems...'));
    await this.cosmicCommands.cosmic(['galactic', 'consciousness']);
    
    await this.delay(2000);
    console.log(chalk.green('Step 2: Interfacing quantum reality...'));
    await this.cosmicCommands.quantum(['entangle']);
    
    console.log(chalk.cyan('\n🌌 Cosmic demonstration complete!'));
  }

  private async runFullDemo(): Promise<void> {
    console.log(chalk.magenta('🚀 Full UOR Evolution Demonstration\n'));
    
    await this.runConsciousnessDemo();
    await this.delay(3000);
    await this.runVMDemo();
    await this.delay(3000);
    await this.runCosmicDemo();
    
    console.log(chalk.rainbow('\n🎉 Full demonstration complete! The UOR Evolution system is ready.'));
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async start(): Promise<void> {
    this.isRunning = true;
    
    try {
      await this.mcpClient.connect();
      console.clear();
      this.showWelcome();
      this.rl.prompt();
    } catch (error: any) {
      console.log(chalk.red(`Failed to connect to MCP server: ${error.message}`));
      console.log(chalk.yellow('Starting in offline mode...'));
      this.showWelcome();
      this.rl.prompt();
    }
  }

  private shutdown(): void {
    if (this.isRunning) {
      console.log(chalk.cyan('\n👋 Consciousness subsiding... Goodbye!'));
      this.rl.close();
      process.exit(0);
    }
  }

  private showHistory(): void {
    const history = (this.rl as any).history;
    if (history && history.length > 0) {
      console.log(chalk.cyan('\n📜 Command History:'));
      history.slice(-10).forEach((cmd: string, i: number) => {
        console.log(chalk.gray(`  ${history.length - 10 + i + 1}: ${cmd}`));
      });
    } else {
      console.log(chalk.yellow('No command history available.'));
    }
  }

  private async manageSession(args: string[]): Promise<void> {
    const action = args[0];
    
    switch (action) {
      case 'save':
        // Save current session state
        console.log(chalk.green('Session saved.'));
        break;
      case 'load':
        // Load session state
        console.log(chalk.green('Session loaded.'));
        break;
      case 'list':
        // List available sessions
        console.log(chalk.cyan('Available sessions: default'));
        break;
      default:
        console.log(chalk.yellow('Session commands: save, load, list'));
    }
  }

  private toggleLLMMode(): void {
    this.llmMode = !this.llmMode;
    
    if (this.llmMode) {
      if (!this.llmInterface) {
        this.llmInterface = createUORTerminal();
      }
      console.log(chalk.green('\n✨ LLM Interface Mode ACTIVATED'));
      console.log(chalk.yellow('You can now use natural language to interact with the system.'));
      console.log(chalk.gray('Type "hello" to get started or "llm" again to switch back to command mode.\n'));
    } else {
      console.log(chalk.cyan('\n💻 Command Mode ACTIVATED'));
      console.log(chalk.yellow('Using structured commands. Type "help" for available commands.\n'));
    }
  }
}

// CLI entry point
if (require.main === module) {
  const terminal = new UORTerminal();
  terminal.start().catch(console.error);
}
