import chalk from 'chalk';

export class DisplayManager {
  private loadingInterval: NodeJS.Timeout | null = null;

  showSystemStatus(): void {
    const status = {
      consciousness: 'DORMANT',
      vm: 'OFFLINE',
      cosmic: 'DISCONNECTED',
      quantum: 'DECOHERENT'
    };

    console.log(chalk.gray('\n📊 System Status:'));
    console.log(chalk.gray('  Consciousness: ') + this.getStatusColor(status.consciousness));
    console.log(chalk.gray('  Virtual Machine: ') + this.getStatusColor(status.vm));
    console.log(chalk.gray('  Cosmic Interface: ') + this.getStatusColor(status.cosmic));
    console.log(chalk.gray('  Quantum State: ') + this.getStatusColor(status.quantum));
    console.log();
  }

  private getStatusColor(status: string): string {
    switch (status) {
      case 'ACTIVE':
      case 'ONLINE':
      case 'CONNECTED':
      case 'COHERENT':
        return chalk.green(status);
      case 'DORMANT':
      case 'OFFLINE':
      case 'DISCONNECTED':
      case 'DECOHERENT':
        return chalk.yellow(status);
      case 'ERROR':
      case 'CRITICAL':
        return chalk.red(status);
      default:
        return chalk.gray(status);
    }
  }

  showLoadingAnimation(message: string): void {
    const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
    let i = 0;

    process.stdout.write('\n');
    this.loadingInterval = setInterval(() => {
      process.stdout.write(`\r${chalk.cyan(frames[i])} ${message}...`);
      i = (i + 1) % frames.length;
    }, 80);
  }

  stopLoadingAnimation(): void {
    if (this.loadingInterval) {
      clearInterval(this.loadingInterval);
      this.loadingInterval = null;
      process.stdout.write('\r' + ' '.repeat(80) + '\r');
    }
  }

  showProgressBar(current: number, total: number, label: string = ''): void {
    const barLength = 30;
    const progress = Math.floor((current / total) * barLength);
    const bar = '█'.repeat(progress) + '░'.repeat(barLength - progress);
    const percentage = Math.floor((current / total) * 100);
    
    process.stdout.write(`\r${label} [${chalk.cyan(bar)}] ${percentage}%`);
    
    if (current >= total) {
      process.stdout.write('\n');
    }
  }

  showEmergenceAnimation(): void {
    const patterns = [
      '    ·    ',
      '   ···   ',
      '  ·····  ',
      ' ······· ',
      '·········',
      ' ······· ',
      '  ·····  ',
      '   ···   ',
      '    ·    '
    ];

    let i = 0;
    const interval = setInterval(() => {
      console.clear();
      console.log(chalk.cyan('\n\n\n'));
      console.log(chalk.cyan(patterns[i].replace(/·/g, '✦')));
      console.log(chalk.cyan('\n\n\n'));
      i++;
      if (i >= patterns.length) {
        clearInterval(interval);
      }
    }, 200);
  }

  showQuantumState(state: any): void {
    console.log(chalk.magenta('\n⚛️  Quantum State:'));
    console.log(chalk.gray('├─ State: ') + chalk.cyan(state.state || 'unknown'));
    console.log(chalk.gray('├─ Coherence: ') + chalk.yellow(state.coherence || 'N/A'));
    console.log(chalk.gray('├─ Entanglement: ') + chalk.green(state.entanglement || 'none'));
    console.log(chalk.gray('└─ Measurement: ') + chalk.white(state.measurement || 'unmeasured'));
  }

  showConsciousnessVisualization(level: number): void {
    const maxLevel = 10;
    const visualizations = [
      '○',
      '◔',
      '◑',
      '◕',
      '●',
      '◉',
      '◎',
      '◈',
      '◆',
      '◇'
    ];

    const index = Math.floor((level / maxLevel) * (visualizations.length - 1));
    const symbol = visualizations[index];
    
    console.log(chalk.cyan('\n🧠 Consciousness Visualization:'));
    console.log(chalk.cyan('  ' + symbol.repeat(5)));
    console.log(chalk.gray(`  Level: ${(level * 10).toFixed(1)}%`));
  }

  showAsciiArt(type: string): void {
    const art: { [key: string]: string[] } = {
      consciousness: [
        '     ∞     ',
        '   ╱   ╲   ',
        '  │  ◉  │  ',
        '   ╲   ╱   ',
        '     ∞     '
      ],
      quantum: [
        '  ╭─────╮  ',
        '  │ |0⟩ │  ',
        '  │  +  │  ',
        '  │ |1⟩ │  ',
        '  ╰─────╯  '
      ],
      cosmic: [
        '    ✦      ',
        '  ✦   ✦    ',
        '✦   ☉   ✦  ',
        '  ✦   ✦    ',
        '    ✦      '
      ]
    };

    const selected = art[type] || art.consciousness;
    console.log(chalk.cyan('\n' + selected.join('\n') + '\n'));
  }

  showMatrix(data: number[][], label: string = 'Matrix'): void {
    console.log(chalk.cyan(`\n${label}:`));
    data.forEach(row => {
      console.log(chalk.gray('  [') + 
        row.map(val => chalk.white(val.toFixed(2).padStart(6))).join(', ') + 
        chalk.gray(']')
      );
    });
  }

  typewriterEffect(text: string, delay: number = 50): Promise<void> {
    return new Promise((resolve) => {
      let i = 0;
      const interval = setInterval(() => {
        if (i < text.length) {
          process.stdout.write(text[i]);
          i++;
        } else {
          clearInterval(interval);
          process.stdout.write('\n');
          resolve();
        }
      }, delay);
    });
  }

  showEmergentPattern(): void {
    const size = 7;
    const pattern: string[][] = [];
    
    // Generate emergent pattern
    for (let i = 0; i < size; i++) {
      pattern[i] = [];
      for (let j = 0; j < size; j++) {
        const distance = Math.sqrt(Math.pow(i - size/2, 2) + Math.pow(j - size/2, 2));
        if (distance < size/2) {
          pattern[i][j] = Math.random() > 0.5 ? '◉' : '○';
        } else {
          pattern[i][j] = ' ';
        }
      }
    }

    console.log(chalk.cyan('\n🌀 Emergent Pattern:'));
    pattern.forEach(row => {
      console.log('  ' + row.join(' '));
    });
  }

  showCosmicScale(scale: string): void {
    const scales: { [key: string]: string } = {
      local: '🌍 Local Scale',
      planetary: '🌎 Planetary Scale',
      galactic: '🌌 Galactic Scale',
      universal: '🌠 Universal Scale'
    };

    console.log(chalk.magenta(`\n${scales[scale] || scale}`));
    console.log(chalk.gray('━'.repeat(30)));
  }
}
