import chalk from 'chalk';
import { MCPClientInterface } from '../mcp-client.js';
import { DisplayManager } from '../ui/display.js';

export class VMCommands {
  private mcpClient: MCPClientInterface;
  private display: DisplayManager;
  private vmInitialized: boolean = false;

  constructor(mcpClient: MCPClientInterface) {
    this.mcpClient = mcpClient;
    this.display = new DisplayManager();
  }

  async initialize(args: string[]): Promise<void> {
    console.log(chalk.yellow('💻 Initializing UOR Prime Virtual Machine...'));
    this.display.showLoadingAnimation('VM initialization in progress');
    
    try {
      // Parse config from args if provided
      const config: any = {};
      for (let i = 0; i < args.length; i += 2) {
        if (args[i] && args[i + 1]) {
          config[args[i]] = args[i + 1];
        }
      }

      const result = await this.mcpClient.initializeVM(config);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ VM initialized successfully!'));
      console.log(chalk.cyan('🔧 VM Configuration:'));
      
      if (result.config) {
        console.log(chalk.white(`  Memory Size: ${result.config.memory_size} bytes`));
        console.log(chalk.white(`  Stack Size: ${result.config.stack_size} bytes`));
        console.log(chalk.white(`  Instruction Set: ${result.config.instruction_set}`));
        console.log(chalk.white(`  Consciousness: ${result.config.consciousness_enabled ? 'ENABLED' : 'DISABLED'}`));
        console.log(chalk.white(`  Quantum Mode: ${result.config.quantum_mode ? 'ACTIVE' : 'INACTIVE'}`));
      }

      if (result.vm_id) {
        console.log(chalk.blue(`\n🆔 VM ID: ${result.vm_id}`));
      }

      if (result.initial_state && result.initial_state.registers) {
        console.log(chalk.magenta('\n📊 Initial Registers:'));
        Object.entries(result.initial_state.registers).forEach(([reg, value]) => {
          console.log(chalk.gray(`  ${reg}: ${value}`));
        });
      }

      this.vmInitialized = true;
      console.log(chalk.yellow('\n💡 VM is ready. Use "step" to execute instructions or "run" to execute programs.'));
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ VM initialization failed: ${error.message}`));
    }
  }

  async step(args: string[]): Promise<void> {
    if (!this.vmInitialized) {
      console.log(chalk.red('❌ VM not initialized. Please run "init" first.'));
      return;
    }

    const instruction = args.join(' ');
    if (!instruction) {
      console.log(chalk.red('❌ No instruction provided. Example: step LOAD 42'));
      return;
    }

    console.log(chalk.yellow(`⚡ Executing instruction: ${instruction}`));
    
    try {
      const result = await this.mcpClient.executeVMStep(instruction);
      
      console.log(chalk.green('\n✅ Instruction executed successfully!'));
      
      if (result.execution_result) {
        console.log(chalk.cyan(`📝 Result: ${result.execution_result}`));
      }

      if (result.registers) {
        console.log(chalk.magenta('\n📊 Register State:'));
        Object.entries(result.registers).forEach(([reg, value]) => {
          console.log(chalk.gray(`  ${reg}: ${value}`));
        });
      }

      if (result.flags) {
        console.log(chalk.yellow('\n🚩 Flags:'));
        Object.entries(result.flags).forEach(([flag, value]) => {
          const color = value ? chalk.green : chalk.gray;
          console.log(color(`  ${flag}: ${value}`));
        });
      }

      if (result.history_length) {
        console.log(chalk.blue(`\n📜 Execution History: ${result.history_length} instructions`));
      }
    } catch (error: any) {
      console.log(chalk.red(`❌ Instruction execution failed: ${error.message}`));
    }
  }

  async run(args: string[]): Promise<void> {
    const program = args[0];
    if (!program) {
      console.log(chalk.red('❌ No program specified.'));
      console.log(chalk.yellow('Available programs: fibonacci, consciousness_test, prime_generator, quantum_simulation, emergence_pattern'));
      return;
    }

    // Parse parameters
    const parameters: any = {};
    for (let i = 1; i < args.length; i += 2) {
      if (args[i] && args[i + 1]) {
        const key = args[i];
        const value = isNaN(Number(args[i + 1])) ? args[i + 1] : Number(args[i + 1]);
        parameters[key] = value;
      }
    }

    console.log(chalk.yellow(`🚀 Running UOR program: ${program}`));
    if (Object.keys(parameters).length > 0) {
      console.log(chalk.gray(`Parameters: ${JSON.stringify(parameters)}`));
    }
    
    this.display.showLoadingAnimation('Program execution in progress');

    try {
      const result = await this.mcpClient.runUORProgram(program, parameters);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ Program execution complete!'));
      
      if (result.execution_time) {
        console.log(chalk.cyan(`⏱️  Execution Time: ${result.execution_time}`));
      }

      if (result.result) {
        console.log(chalk.magenta('\n📤 Output:'));
        if (Array.isArray(result.result)) {
          if (program === 'fibonacci') {
            console.log(chalk.white('  Fibonacci Sequence:'));
            console.log(chalk.yellow(`  ${result.result.join(', ')}`));
          } else if (program === 'prime_generator') {
            console.log(chalk.white(`  Found ${result.result.length} primes:`));
            console.log(chalk.yellow(`  ${result.result.join(', ')}`));
          } else if (program === 'consciousness_test') {
            result.result.forEach((test: string) => {
              console.log(chalk.green(`  ✓ ${test}`));
            });
          } else {
            result.result.forEach((item: any) => {
              console.log(chalk.white(`  ${JSON.stringify(item)}`));
            });
          }
        } else if (typeof result.result === 'object') {
          this.formatProgramOutput(program, result.result);
        } else {
          console.log(chalk.white(`  ${result.result}`));
        }
      }

      // Show special visualizations for certain programs
      if (program === 'quantum_simulation') {
        this.display.showAsciiArt('quantum');
      } else if (program === 'emergence_pattern') {
        this.display.showEmergentPattern();
      } else if (program === 'consciousness_test') {
        this.display.showConsciousnessVisualization(8.5);
      }

    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Program execution failed: ${error.message}`));
    }
  }

  async load(args: string[]): Promise<void> {
    const filename = args[0];
    if (!filename) {
      console.log(chalk.red('❌ No filename specified.'));
      return;
    }

    console.log(chalk.yellow(`📁 Loading UOR program from: ${filename}`));
    console.log(chalk.gray('(This would load and execute a UOR program from a file)'));
    
    // Simulate loading
    this.display.showLoadingAnimation('Loading program');
    await this.delay(2000);
    this.display.stopLoadingAnimation();
    
    console.log(chalk.green('✅ Program loaded successfully!'));
    console.log(chalk.yellow('Use "run" command to execute the loaded program.'));
  }

  private formatProgramOutput(program: string, output: any): void {
    switch (program) {
      case 'quantum_simulation':
        if (output.qubits) {
          console.log(chalk.white(`  Qubits: ${output.qubits}`));
        }
        if (output.entanglement_pairs) {
          console.log(chalk.cyan(`  Entanglement Pairs: ${output.entanglement_pairs}`));
        }
        if (output.coherence_time) {
          console.log(chalk.yellow(`  Coherence Time: ${output.coherence_time}`));
        }
        if (output.measurement_results) {
          console.log(chalk.magenta(`  Measurements: [${output.measurement_results.join(', ')}]`));
        }
        break;

      case 'emergence_pattern':
        if (output.output && Array.isArray(output.output)) {
          console.log(chalk.white('  Emergence Patterns:'));
          output.output.forEach((pattern: any) => {
            console.log(chalk.cyan(`    ${pattern.description}`));
            const bar = this.createBar(pattern.emergence_factor, 20);
            console.log(chalk.gray(`      Emergence: ${bar} ${(pattern.emergence_factor * 100).toFixed(1)}%`));
          });
        }
        if (output.total_emergence) {
          console.log(chalk.green(`  Total Emergence: ${(output.total_emergence * 100).toFixed(1)}%`));
        }
        if (output.consciousness_impact) {
          console.log(chalk.magenta(`  Consciousness Impact: ${output.consciousness_impact}`));
        }
        break;

      default:
        console.log(chalk.white(JSON.stringify(output, null, 2)));
    }
  }

  private createBar(value: number, length: number): string {
    const filled = Math.floor(value * length);
    const empty = length - filled;
    return chalk.cyan('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
