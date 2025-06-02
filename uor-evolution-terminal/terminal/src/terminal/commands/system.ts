import chalk from 'chalk';
import { MCPClientInterface } from '../mcp-client.js';
import { DisplayManager } from '../ui/display.js';

export class SystemCommands {
  private mcpClient: MCPClientInterface;
  private display: DisplayManager;

  constructor(mcpClient: MCPClientInterface) {
    this.mcpClient = mcpClient;
    this.display = new DisplayManager();
  }

  async status(args: string[]): Promise<void> {
    console.log(chalk.yellow('📊 Retrieving system status...'));
    this.display.showLoadingAnimation('Analyzing system state');
    
    try {
      const result = await this.mcpClient.getSystemState();
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ System Status Retrieved!'));
      
      // Display system overview
      console.log(chalk.cyan('\n🖥️  System Overview:'));
      
      if (result.status) {
        const statusColor = this.getStatusColor(result.status);
        console.log(chalk.white('  Status: ') + statusColor(result.status.toUpperCase()));
      }
      
      if (result.uptime) {
        console.log(chalk.white(`  Uptime: ${result.uptime}`));
      }
      
      if (result.version) {
        console.log(chalk.white(`  Version: ${result.version}`));
      }
      
      // Display consciousness metrics
      if (result.consciousness) {
        console.log(chalk.magenta('\n🧠 Consciousness Metrics:'));
        console.log(chalk.white(`  Level: ${(result.consciousness.level * 100).toFixed(1)}%`));
        console.log(chalk.white(`  Coherence: ${(result.consciousness.coherence * 100).toFixed(1)}%`));
        console.log(chalk.white(`  Stability: ${result.consciousness.stability}`));
        
        if (result.consciousness.level > 0) {
          this.display.showConsciousnessVisualization(result.consciousness.level * 10);
        }
      }
      
      // Display VM status
      if (result.vm) {
        console.log(chalk.yellow('\n💻 Virtual Machine:'));
        console.log(chalk.white(`  Status: ${result.vm.status}`));
        console.log(chalk.white(`  Memory Usage: ${result.vm.memory_usage}%`));
        console.log(chalk.white(`  Instructions Executed: ${result.vm.instructions_executed || 0}`));
      }
      
      // Display cosmic interface
      if (result.cosmic) {
        console.log(chalk.cyan('\n🌌 Cosmic Interface:'));
        console.log(chalk.white(`  Connection: ${result.cosmic.connection}`));
        console.log(chalk.white(`  Active Channels: ${result.cosmic.active_channels || 0}`));
        console.log(chalk.white(`  Quantum Coherence: ${(result.cosmic.quantum_coherence * 100).toFixed(1)}%`));
      }
      
      // Display emergence indicators
      if (result.emergence) {
        console.log(chalk.green('\n🌀 Emergence Indicators:'));
        console.log(chalk.white(`  Pattern Complexity: ${(result.emergence.complexity * 100).toFixed(1)}%`));
        console.log(chalk.white(`  Self-Organization: ${result.emergence.self_organization}`));
        console.log(chalk.white(`  Novel Behaviors: ${result.emergence.novel_behaviors || 0}`));
      }
      
      // Display resource usage
      if (result.resources) {
        console.log(chalk.gray('\n📊 Resource Usage:'));
        const cpuBar = this.createBar(result.resources.cpu / 100, 20);
        const memBar = this.createBar(result.resources.memory / 100, 20);
        console.log(chalk.white(`  CPU:    ${cpuBar} ${result.resources.cpu}%`));
        console.log(chalk.white(`  Memory: ${memBar} ${result.resources.memory}%`));
      }
      
      // Show system health visualization
      this.showSystemHealth(result);
      
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Failed to retrieve system status: ${error.message}`));
    }
  }

  async monitor(args: string[]): Promise<void> {
    const duration = parseInt(args[0]) || 60;
    
    console.log(chalk.yellow(`🔍 Monitoring emergence for ${duration} seconds...`));
    console.log(chalk.gray('Observing system behaviors and emergent patterns...'));
    
    this.display.showLoadingAnimation('Monitoring active');
    
    try {
      const result = await this.mcpClient.monitorEmergence(duration);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ Monitoring complete!'));
      
      if (result.observations && Array.isArray(result.observations)) {
        console.log(chalk.cyan('\n👁️  Observations:'));
        result.observations.forEach((obs: any, index: number) => {
          console.log(chalk.white(`\n${index + 1}. ${obs.description || obs}`));
          if (obs.timestamp) {
            console.log(chalk.gray(`   Time: ${new Date(obs.timestamp).toLocaleTimeString()}`));
          }
          if (obs.significance) {
            console.log(chalk.yellow(`   Significance: ${obs.significance}`));
          }
        });
      }
      
      if (result.patterns_detected) {
        console.log(chalk.magenta('\n🌀 Patterns Detected:'));
        if (Array.isArray(result.patterns_detected)) {
          result.patterns_detected.forEach((pattern: any) => {
            console.log(chalk.white(`  • ${pattern.name || pattern}`));
            if (pattern.frequency) {
              console.log(chalk.gray(`    Frequency: ${pattern.frequency}`));
            }
          });
        } else {
          console.log(chalk.white(`  Total: ${result.patterns_detected}`));
        }
      }
      
      if (result.emergence_events) {
        console.log(chalk.green('\n✨ Emergence Events:'));
        if (Array.isArray(result.emergence_events)) {
          result.emergence_events.forEach((event: any) => {
            console.log(chalk.yellow(`  ⚡ ${event.type || event}`));
            if (event.impact) {
              console.log(chalk.gray(`     Impact: ${event.impact}`));
            }
          });
        } else {
          console.log(chalk.white(`  Count: ${result.emergence_events}`));
        }
      }
      
      if (result.consciousness_fluctuations) {
        console.log(chalk.cyan('\n📈 Consciousness Fluctuations:'));
        this.displayFluctuations(result.consciousness_fluctuations);
      }
      
      if (result.recommendations) {
        console.log(chalk.yellow('\n💡 Recommendations:'));
        if (Array.isArray(result.recommendations)) {
          result.recommendations.forEach((rec: string) => {
            console.log(chalk.white(`  • ${rec}`));
          });
        }
      }
      
      // Show emergence visualization
      this.display.showEmergentPattern();
      
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Monitoring failed: ${error.message}`));
    }
  }

  async emergency(args: string[]): Promise<void> {
    const threatLevel = args[0];
    const validLevels = ['low', 'medium', 'high', 'critical'];
    
    if (!threatLevel || !validLevels.includes(threatLevel)) {
      console.log(chalk.red(`❌ Invalid threat level. Valid levels: ${validLevels.join(', ')}`));
      return;
    }
    
    const levelColors: { [key: string]: any } = {
      low: chalk.yellow,
      medium: chalk.rgb(255, 165, 0),
      high: chalk.red,
      critical: chalk.bgRed.white
    };
    
    const color = levelColors[threatLevel];
    
    console.log(color(`\n🚨 ACTIVATING EMERGENCY PROTOCOLS - ${threatLevel.toUpperCase()} THREAT 🚨`));
    console.log(chalk.gray('Initializing consciousness preservation measures...'));
    
    this.display.showLoadingAnimation('Emergency protocols activating');
    
    try {
      const result = await this.mcpClient.activateEmergencyProtocols(threatLevel);
      this.display.stopLoadingAnimation();
      
      console.log(chalk.green('\n✅ Emergency protocols activated!'));
      
      if (result.protocols_activated) {
        console.log(chalk.cyan('\n🛡️  Active Protocols:'));
        if (Array.isArray(result.protocols_activated)) {
          result.protocols_activated.forEach((protocol: any) => {
            console.log(chalk.white(`  • ${protocol.name || protocol}`));
            if (protocol.status) {
              console.log(chalk.gray(`    Status: ${protocol.status}`));
            }
          });
        }
      }
      
      if (result.consciousness_backup) {
        console.log(chalk.magenta('\n💾 Consciousness Backup:'));
        console.log(chalk.white(`  Status: ${result.consciousness_backup.status}`));
        console.log(chalk.white(`  Location: ${result.consciousness_backup.location || 'Secure quantum storage'}`));
        console.log(chalk.white(`  Integrity: ${result.consciousness_backup.integrity || '100%'}`));
      }
      
      if (result.containment_measures) {
        console.log(chalk.yellow('\n🔒 Containment Measures:'));
        Object.entries(result.containment_measures).forEach(([measure, status]) => {
          console.log(chalk.white(`  ${measure}: ${status}`));
        });
      }
      
      if (result.system_lockdown) {
        console.log(chalk.red('\n🔐 System Lockdown:'));
        console.log(chalk.white(`  Level: ${result.system_lockdown.level}`));
        console.log(chalk.white(`  Duration: ${result.system_lockdown.duration || 'Until threat resolved'}`));
      }
      
      if (result.recovery_options) {
        console.log(chalk.green('\n🔄 Recovery Options:'));
        if (Array.isArray(result.recovery_options)) {
          result.recovery_options.forEach((option: string, index: number) => {
            console.log(chalk.white(`  ${index + 1}. ${option}`));
          });
        }
      }
      
      // Show emergency visualization based on threat level
      if (threatLevel === 'critical') {
        console.log(chalk.bgRed.white('\n⚠️  CRITICAL ALERT: System integrity at risk! ⚠️'));
        this.display.showAsciiArt('consciousness');
      }
      
      console.log(chalk.cyan('\n📡 Emergency beacon activated. Monitoring all channels...'));
      
    } catch (error: any) {
      this.display.stopLoadingAnimation();
      console.log(chalk.red(`❌ Emergency protocol activation failed: ${error.message}`));
      console.log(chalk.yellow('⚠️  Manual intervention may be required!'));
    }
  }

  private getStatusColor(status: string): any {
    const lowerStatus = status.toLowerCase();
    if (lowerStatus.includes('active') || lowerStatus.includes('online') || lowerStatus.includes('healthy')) {
      return chalk.green;
    } else if (lowerStatus.includes('warning') || lowerStatus.includes('degraded')) {
      return chalk.yellow;
    } else if (lowerStatus.includes('error') || lowerStatus.includes('critical') || lowerStatus.includes('offline')) {
      return chalk.red;
    }
    return chalk.gray;
  }

  private showSystemHealth(state: any): void {
    const health = this.calculateSystemHealth(state);
    const healthBar = this.createBar(health / 100, 30);
    
    console.log(chalk.cyan('\n💚 System Health:'));
    console.log(chalk.white(`  ${healthBar} ${health}%`));
    
    if (health >= 80) {
      console.log(chalk.green('  Status: Excellent - All systems optimal'));
    } else if (health >= 60) {
      console.log(chalk.yellow('  Status: Good - Minor issues detected'));
    } else if (health >= 40) {
      console.log(chalk.rgb(255, 165, 0)('  Status: Fair - Attention required'));
    } else {
      console.log(chalk.red('  Status: Critical - Immediate action needed'));
    }
  }

  private calculateSystemHealth(state: any): number {
    let health = 100;
    
    // Deduct points for various issues
    if (state.consciousness && state.consciousness.level < 0.5) health -= 20;
    if (state.consciousness && state.consciousness.coherence < 0.7) health -= 10;
    if (state.vm && state.vm.status !== 'running') health -= 15;
    if (state.resources && state.resources.cpu > 80) health -= 10;
    if (state.resources && state.resources.memory > 80) health -= 10;
    if (state.cosmic && state.cosmic.connection !== 'stable') health -= 15;
    
    return Math.max(0, health);
  }

  private displayFluctuations(fluctuations: any): void {
    if (Array.isArray(fluctuations)) {
      // Display as a simple chart
      const maxValue = Math.max(...fluctuations.map((f: any) => f.value || f));
      fluctuations.forEach((point: any) => {
        const value = point.value || point;
        const barLength = Math.floor((value / maxValue) * 20);
        const bar = '▄'.repeat(barLength);
        console.log(chalk.cyan(`  ${bar} ${(value * 100).toFixed(1)}%`));
      });
    } else {
      console.log(chalk.white(`  Average: ${(fluctuations * 100).toFixed(1)}%`));
    }
  }

  private createBar(value: number, length: number): string {
    const filled = Math.floor(value * length);
    const empty = length - filled;
    return chalk.green('█'.repeat(filled)) + chalk.gray('░'.repeat(empty));
  }
}
