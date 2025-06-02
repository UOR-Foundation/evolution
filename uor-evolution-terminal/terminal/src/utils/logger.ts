import * as fs from 'fs';
import * as path from 'path';

export interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  data?: any;
}

export class Logger {
  private logFile: string;
  private logLevel: string;

  constructor(logFile?: string, logLevel: string = 'info') {
    this.logFile = logFile || path.join(process.cwd(), 'terminal.log');
    this.logLevel = logLevel;
  }

  private shouldLog(level: string): boolean {
    const levels = ['debug', 'info', 'warn', 'error'];
    const currentLevelIndex = levels.indexOf(this.logLevel);
    const messageLevelIndex = levels.indexOf(level);
    return messageLevelIndex >= currentLevelIndex;
  }

  private formatMessage(level: string, message: string, data?: any): string {
    const timestamp = new Date().toISOString();
    const logEntry: LogEntry = {
      timestamp,
      level,
      message,
      data
    };
    return JSON.stringify(logEntry);
  }

  private writeToFile(message: string): void {
    try {
      fs.appendFileSync(this.logFile, message + '\n');
    } catch (error) {
      console.error('Failed to write to log file:', error);
    }
  }

  debug(message: string, data?: any): void {
    if (this.shouldLog('debug')) {
      const formatted = this.formatMessage('debug', message, data);
      this.writeToFile(formatted);
    }
  }

  info(message: string, data?: any): void {
    if (this.shouldLog('info')) {
      const formatted = this.formatMessage('info', message, data);
      this.writeToFile(formatted);
    }
  }

  warn(message: string, data?: any): void {
    if (this.shouldLog('warn')) {
      const formatted = this.formatMessage('warn', message, data);
      this.writeToFile(formatted);
    }
  }

  error(message: string, data?: any): void {
    if (this.shouldLog('error')) {
      const formatted = this.formatMessage('error', message, data);
      this.writeToFile(formatted);
    }
  }
}

export const logger = new Logger();
