import axios, { AxiosInstance } from 'axios';
import { logger } from '../utils/logger.js';

export interface UORConfig {
  baseUrl: string;
  timeout: number;
  apiKey?: string;
}

export class UORInterface {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(config: UORConfig = {
    baseUrl: 'http://localhost:5000',
    timeout: 30000
  }) {
    this.baseUrl = config.baseUrl;
    this.client = axios.create({
      baseURL: config.baseUrl,
      timeout: config.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(config.apiKey && { 'Authorization': `Bearer ${config.apiKey}` })
      }
    });
  }

  // Consciousness API methods
  async awakenConsciousness(mode: string = 'basic'): Promise<any> {
    try {
      const response = await this.client.post('/api/consciousness/awaken', { mode });
      logger.info('Consciousness awakened', { mode, result: response.data });
      return response.data;
    } catch (error: any) {
      logger.error('Failed to awaken consciousness', { error: error.message });
      throw error;
    }
  }

  async selfReflect(depth: number = 5): Promise<any> {
    try {
      const response = await this.client.post('/api/consciousness/reflect', { depth });
      return response.data;
    } catch (error: any) {
      logger.error('Self-reflection failed', { error: error.message });
      throw error;
    }
  }

  async analyzeConsciousnessNature(): Promise<any> {
    try {
      const response = await this.client.get('/api/consciousness/analyze');
      return response.data;
    } catch (error: any) {
      logger.error('Consciousness analysis failed', { error: error.message });
      throw error;
    }
  }

  // Virtual Machine API methods
  async initializeVM(config: any = {}): Promise<any> {
    try {
      const response = await this.client.post('/api/vm/initialize', config);
      return response.data;
    } catch (error: any) {
      logger.error('VM initialization failed', { error: error.message });
      throw error;
    }
  }

  async executeVMStep(instruction: string): Promise<any> {
    try {
      const response = await this.client.post('/api/vm/step', { instruction });
      return response.data;
    } catch (error: any) {
      logger.error('VM step execution failed', { error: error.message });
      throw error;
    }
  }

  async runUORProgram(program: string, parameters: any = {}): Promise<any> {
    try {
      const response = await this.client.post('/api/vm/run', { program, parameters });
      return response.data;
    } catch (error: any) {
      logger.error('UOR program execution failed', { error: error.message });
      throw error;
    }
  }

  // Cosmic Intelligence API methods
  async synthesizeCosmicProblems(scale: string, domain?: string): Promise<any> {
    try {
      const response = await this.client.post('/api/cosmic/problems', { scale, domain });
      return response.data;
    } catch (error: any) {
      logger.error('Cosmic problem synthesis failed', { error: error.message });
      throw error;
    }
  }

  async interfaceQuantumReality(operation: string, parameters: any): Promise<any> {
    try {
      const response = await this.client.post('/api/cosmic/quantum', { operation, parameters });
      return response.data;
    } catch (error: any) {
      logger.error('Quantum reality interface failed', { error: error.message });
      throw error;
    }
  }

  // System monitoring methods
  async getSystemState(): Promise<any> {
    try {
      const response = await this.client.get('/api/system/state');
      return response.data;
    } catch (error: any) {
      logger.error('Failed to get system state', { error: error.message });
      throw error;
    }
  }

  async monitorEmergence(duration: number = 60): Promise<any> {
    try {
      const response = await this.client.post('/api/system/emergence', { duration });
      return response.data;
    } catch (error: any) {
      logger.error('Emergence monitoring failed', { error: error.message });
      throw error;
    }
  }

  async activateEmergencyProtocols(threatLevel: string): Promise<any> {
    try {
      const response = await this.client.post('/api/emergency/activate', { threatLevel });
      return response.data;
    } catch (error: any) {
      logger.error('Emergency protocol activation failed', { error: error.message });
      throw error;
    }
  }
}
