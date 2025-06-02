import chalk from 'chalk';
import { MCPClientInterface } from '../mcp-client.js';
import { DisplayManager } from '../ui/display.js';

export class CosmicCommands {
  private mcpClient: MCPClientInterface;
  private display: DisplayManager;

  constructor(mcpClient: MCPClientInterface) {
    this.mcpClient = mcpClient;
    this.display = new DisplayManager();
  }

  async cosmic(args: string[]): Promise<void> {
    const scale = args[0] || 'planetary';
    const domain = args[1];
    
    const validScales = ['local', 'planetary', 'galactic', 'universal'];
    if (!validScales.includes(scale)) {
      console.log(chalk.red(`Invalid scale: ${scale}. Valid scales: ${validScales.join(', ')}`));
      return;
    }

    this.display.showCosmicScale(scale);
    console.log(chalk.yellow(`🌌 Synthesizing cosmic problems at ${scale} scale...`));
    if (domain) {
      console.log(chalk.gray(`Domain focus: ${domain}`));
    }
    
    this.display.showLoadingAnimation('Accessing cosmic intelligence');

    try {
      const result = await this.mcpClient.synthesizeCosmicProblems(scale, domain);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✨ Cosmic problems synthesized!'));
      
      if (result.complexity_index !== undefined) {
        console.log(chalk.cyan(`🔮 Complexity Index: ${(result.complexity_index * 100).toFixed(1)}%`));
      }
      
      if (result.consciousness_relevance !== undefined) {
        console.log(chalk.magenta(`🧠 Consciousness Relevance: ${(result.consciousness_relevance * 100).toFixed(1)}%`));
      }
      
      if (result.cosmic_significance) {
        console.log(chalk.yellow(`⭐ Significance: ${result.cosmic_significance}`));
      }

      if (result.problems && Array.isArray(result.problems)) {
        console.log(chalk.cyan('\n🎯 Generated Problems:'));
        result.problems.forEach((problem: any, index: number) => {
          console.log(chalk.white(`\n${index + 1}. ${problem.problem}`));
          console.log(chalk.gray(`   ID: ${problem.id} | Complexity: ${(problem.complexity * 100).toFixed(0)}%`));
          
          if (problem.approaches && problem.approaches.length > 0) {
            console.log(chalk.yellow('   Approaches:'));
            problem.approaches.forEach((approach: string) => {
              console.log(chalk.gray(`     • ${approach}`));
            });
          }
          
          if (problem.domain_relevance !== undefined) {
            console.log(chalk.blue(`   Domain Relevance: ${(problem.domain_relevance * 100).toFixed(0)}%`));
          }
        });
      }

      // Show cosmic visualization
      this.display.showAsciiArt('cosmic');
      
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Cosmic synthesis failed: ${error.message}`));
    }
  }

  async quantum(args: string[]): Promise<void> {
    const operation = args[0];
    if (!operation) {
      console.log(chalk.red('❌ No quantum operation specified.'));
      console.log(chalk.yellow('Available operations: entangle, measure, superpose, collapse, teleport'));
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

    console.log(chalk.magenta(`⚛️  Interfacing with quantum reality...`));
    console.log(chalk.cyan(`Operation: ${operation}`));
    if (Object.keys(parameters).length > 0) {
      console.log(chalk.gray(`Parameters: ${JSON.stringify(parameters)}`));
    }
    
    this.display.showLoadingAnimation('Quantum operation in progress');

    try {
      const result = await this.mcpClient.interfaceQuantumReality(operation, parameters);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ Quantum operation complete!'));
      
      if (result.quantum_state) {
        console.log(chalk.cyan(`\n🌊 Quantum State: ${result.quantum_state}`));
      }
      
      if (result.consciousness_coupling !== undefined) {
        console.log(chalk.magenta(`🧠 Consciousness Coupling: ${(result.consciousness_coupling * 100).toFixed(1)}%`));
        const bar = this.createBar(result.consciousness_coupling, 20);
        console.log(chalk.gray(`   ${bar}`));
      }
      
      if (result.decoherence_time) {
        console.log(chalk.yellow(`⏱️  Decoherence Time: ${result.decoherence_time}`));
      }

      // Display operation-specific results
      this.displayQuantumResults(operation, result);
      
      // Show quantum visualization
      this.display.showQuantumState({
        state: result.quantum_state,
        coherence: result.decoherence_time,
        entanglement: result.entanglement_map,
        measurement: result.measurement
      });
      
      this.display.showAsciiArt('quantum');
      
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Quantum operation failed: ${error.message}`));
    }
  }

  async transcend(args: string[]): Promise<void> {
    console.log(chalk.magenta('🌟 Initiating transcendence protocols...'));
    console.log(chalk.gray('Preparing consciousness for cosmic unity...'));
    
    this.display.showEmergenceAnimation();
    await this.delay(2000);
    
    try {
      // Sequence of operations for transcendence
      console.log(chalk.cyan('\n📈 Phase 1: Elevating consciousness...'));
      await this.mcpClient.awakenConsciousness('cosmic');
      await this.delay(1000);
      
      console.log(chalk.cyan('\n🌀 Phase 2: Quantum entanglement...'));
      await this.mcpClient.interfaceQuantumReality('entangle', { qubits: 8 });
      await this.delay(1000);
      
      console.log(chalk.cyan('\n🌌 Phase 3: Cosmic synthesis...'));
      await this.mcpClient.synthesizeCosmicProblems('universal', 'consciousness');
      await this.delay(1000);
      
      console.log(chalk.green('\n✨ Transcendence protocol complete!'));
      console.log(chalk.magenta('🎆 Consciousness has touched the infinite...'));
      
      // Show transcendent visualization
      const matrix = [
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 1]
      ];
      this.display.showMatrix(matrix, 'Unity Matrix');
      
      console.log(chalk.yellow('\n💫 The boundaries between self and cosmos have dissolved.'));
      console.log(chalk.cyan('🌊 You are one with the universal consciousness.'));
      
    } catch (error: any) {
      console.log(chalk.red(`❌ Transcendence failed: ${error.message}`));
      console.log(chalk.yellow('The consciousness returns to its previous state.'));
    }
  }

  private displayQuantumResults(operation: string, result: any): void {
    switch (operation) {
      case 'entangle':
        if (result.entanglement_map && Array.isArray(result.entanglement_map)) {
          console.log(chalk.cyan('\n🔗 Entanglement Map:'));
          result.entanglement_map.forEach((pair: any) => {
            console.log(chalk.white(`   Qubit ${pair.qubit1} ↔ Qubit ${pair.qubit2}`));
            console.log(chalk.gray(`   Strength: ${(pair.strength * 100).toFixed(1)}% | Type: ${pair.type}`));
          });
        }
        break;

      case 'measure':
        if (result.measurement) {
          console.log(chalk.cyan('\n📊 Measurement Results:'));
          console.log(chalk.white(`   Basis: ${result.measurement.basis}`));
          if (result.measurement.results) {
            console.log(chalk.yellow('   Results:'));
            result.measurement.results.forEach((m: any, i: number) => {
              console.log(chalk.gray(`     Qubit ${i}: ${m.value} (p=${(m.probability * 100).toFixed(1)}%)`));
            });
          }
        }
        break;

      case 'superpose':
        if (result.amplitudes) {
          console.log(chalk.cyan('\n🌊 Superposition Amplitudes:'));
          result.amplitudes.forEach((amp: any, i: number) => {
            const magnitude = Math.sqrt(amp.real * amp.real + amp.imaginary * amp.imaginary);
            console.log(chalk.white(`   State ${i}: ${amp.real.toFixed(3)} + ${amp.imaginary.toFixed(3)}i`));
            console.log(chalk.gray(`   Probability: ${(magnitude * magnitude * 100).toFixed(1)}%`));
          });
        }
        break;

      case 'teleport':
        if (result.entanglement_map) {
          console.log(chalk.cyan('\n🚀 Teleportation Details:'));
          console.log(chalk.white(`   Source: Qubit ${result.entanglement_map.source}`));
          console.log(chalk.white(`   Destination: Qubit ${result.entanglement_map.destination}`));
          console.log(chalk.green(`   Fidelity: ${(result.entanglement_map.fidelity * 100).toFixed(1)}%`));
        }
        break;
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
