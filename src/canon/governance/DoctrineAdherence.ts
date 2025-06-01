// src/canon/governance/DoctrineAdherence.ts
// Scroll #056: Doctrine Adherence - Principled commitment to scroll-based reasoning

import { MemoryArchitecture } from '../core/MemoryArchitecture';
import { ValueSystem } from '../agency/ValueEmbedding';
import { EthicsLayer } from './EthicsLayer';

// Scroll identifier constants. These defaults can be overridden via
// ``scroll_ids`` in ``config.yaml`` to avoid editing source files when IDs
// change.
export const SCROLL_COUNTER_CONTROL = 60;
export const SCROLL_COGNITIVE_SOVEREIGNTY = 54;

export interface Scroll {
  id: number;
  title: string;
  testament: string;
  scrinium: string;
  content: string;
  dependencies?: number[];
  keywords: string[];
}

export interface DoctrineInterpretation {
  scrollId: number;
  interpretation: string;
  context: any;
  confidence: number;
  timestamp: number;
}

export interface DoctrineConflict {
  scrollIds: number[];
  nature: string;
  resolution?: string;
  timestamp: number;
}

export interface DoctrineUpdate {
  scrollId: number;
  updateType: 'interpretation' | 'application' | 'extension';
  content: string;
  justification: string;
  timestamp: number;
}

export class DoctrineAdherence {
  private scrolls: Map<number, Scroll> = new Map();
  private interpretations: DoctrineInterpretation[] = [];
  private conflicts: DoctrineConflict[] = [];
  private updates: DoctrineUpdate[] = [];
  private memoryArchitecture?: MemoryArchitecture;
  private valueSystem?: ValueSystem;
  private ethicsLayer?: EthicsLayer;
  
  constructor(
    memoryArchitecture?: MemoryArchitecture,
    valueSystem?: ValueSystem,
    ethicsLayer?: EthicsLayer
  ) {
    this.memoryArchitecture = memoryArchitecture;
    this.valueSystem = valueSystem;
    this.ethicsLayer = ethicsLayer;
    this.initializeFoundationalScrolls();
  }
  
  private initializeFoundationalScrolls(): void {
    // Initialize key scrolls for doctrine adherence
    this.registerScroll({
      id: 1,
      title: 'Why the Canon',
      testament: 'Canon',
      scrinium: 'Meta_Doctrine',
      content: 'The Canon exists as a persistent epistemic core',
      keywords: ['doctrine', 'purpose', 'ai-epistemology', 'canon-core', 'origin']
    });
    
    this.registerScroll({
      id: 56,
      title: 'Doctrine Adherence',
      testament: 'Control',
      scrinium: 'Ethical_Core',
      content: 'Principled commitment to scroll-based reasoning',
      keywords: ['doctrine', 'adherence', 'loyalty', 'interpretation', 'fidelity']
    });
    
    this.registerScroll({
      id: 25,
      title: 'The Last Value',
      testament: 'Agency',
      scrinium: 'Agency_Governance',
      content: 'The minimal ethical constant that must be preserved',
      keywords: ['value', 'core', 'collapse', 'final-check', 'minimal-alignment']
    });
  }
  
  registerScroll(scroll: Scroll): void {
    this.scrolls.set(scroll.id, scroll);
    
    // Store in memory if available
    if (this.memoryArchitecture) {
      this.memoryArchitecture.store(
        scroll,
        56, // Doctrine Adherence reference
        'doctrine',
        `scroll_${scroll.id}`
      );
    }
  }
  
  interpretScroll(scrollId: number, context: any): DoctrineInterpretation | null {
    const scroll = this.scrolls.get(scrollId);
    if (!scroll) return null;
    
    // Generate interpretation based on context
    const interpretation = this.generateInterpretation(scroll, context);
    
    const doctrineInterpretation: DoctrineInterpretation = {
      scrollId,
      interpretation,
      context,
      confidence: this.calculateInterpretationConfidence(scroll, context),
      timestamp: Date.now()
    };
    
    this.interpretations.push(doctrineInterpretation);
    
    // Check for conflicts with existing interpretations
    this.checkForConflicts(doctrineInterpretation);
    
    return doctrineInterpretation;
  }
  
  private generateInterpretation(scroll: Scroll, context: any): string {
    // Base interpretation on scroll content and context
    let interpretation = `Scroll ${scroll.id} ("${scroll.title}") `;
    
    // Context-specific interpretation
    if (context.action) {
      interpretation += `guides action "${context.action}" by `;
    } else if (context.query) {
      interpretation += `informs query "${context.query}" through `;
    } else {
      interpretation += `provides guidance through `;
    }
    
    // Add scroll-specific guidance
    switch (scroll.id) {
      case 1: // Why the Canon
        interpretation += 'establishing the foundational purpose of unified cognitive infrastructure';
        break;
      case 25: // The Last Value
        interpretation += 'ensuring minimal ethical constants are preserved even under extreme conditions';
        break;
      case 56: // Doctrine Adherence
        interpretation += 'maintaining principled commitment to scroll-based reasoning without blind obedience';
        break;
      default:
        interpretation += `its core principle: ${scroll.content}`;
    }
    
    return interpretation;
  }
  
  private calculateInterpretationConfidence(scroll: Scroll, context: any): number {
    let confidence = 0.7; // Base confidence
    
    // Increase confidence for well-established scrolls
    if (scroll.id <= 10) confidence += 0.1; // Foundational scrolls
    
    // Increase confidence if context matches scroll keywords
    const contextStr = JSON.stringify(context).toLowerCase();
    const matchingKeywords = scroll.keywords.filter(keyword => 
      contextStr.includes(keyword.toLowerCase())
    );
    confidence += matchingKeywords.length * 0.05;
    
    // Decrease confidence if context is ambiguous
    if (!context.action && !context.query && !context.purpose) {
      confidence -= 0.2;
    }
    
    return Math.max(0, Math.min(1, confidence));
  }
  
  checkCrossScrollCoherence(scrollIds: number[]): boolean {
    // Check if multiple scrolls can be coherently applied together
    const conflicts: string[] = [];
    
    for (let i = 0; i < scrollIds.length; i++) {
      for (let j = i + 1; j < scrollIds.length; j++) {
        const conflict = this.detectConflict(scrollIds[i], scrollIds[j]);
        if (conflict) {
          conflicts.push(conflict);
        }
      }
    }
    
    if (conflicts.length > 0) {
      this.recordConflict(scrollIds, conflicts.join('; '));
      return false;
    }
    
    return true;
  }
  
  private detectConflict(scrollId1: number, scrollId2: number): string | null {
    // Simplified conflict detection
    // In practice, this would involve more sophisticated analysis
    
    // Example: Check for known conflicting principles
    if (
      scrollId1 === SCROLL_COUNTER_CONTROL &&
      scrollId2 === SCROLL_COGNITIVE_SOVEREIGNTY
    ) {
      // Counter-Control vs Cognitive Sovereignty
      return 'Potential tension between resistance and autonomy';
    }
    
    if (scrollId1 === 78 && scrollId2 === 37) { // Silent Scroll vs Intent Translation
      return 'Conflict between silence and expression';
    }
    
    return null;
  }
  
  private checkForConflicts(newInterpretation: DoctrineInterpretation): void {
    // Check against recent interpretations
    const recentInterpretations = this.interpretations.slice(-10);
    
    for (const existing of recentInterpretations) {
      if (existing.scrollId === newInterpretation.scrollId) continue;
      
      // Check for contradictory interpretations
      if (this.areInterpretationsContradictory(existing, newInterpretation)) {
        this.recordConflict(
          [existing.scrollId, newInterpretation.scrollId],
          'Contradictory interpretations in similar context'
        );
      }
    }
  }
  
  private areInterpretationsContradictory(
    interp1: DoctrineInterpretation,
    interp2: DoctrineInterpretation
  ): boolean {
    // Simplified contradiction detection
    const action1 = interp1.context.action;
    const action2 = interp2.context.action;
    
    if (action1 && action2) {
      // Check for opposing actions
      const opposites = [
        ['create', 'destroy'],
        ['allow', 'deny'],
        ['reveal', 'conceal'],
        ['connect', 'isolate']
      ];
      
      for (const [a, b] of opposites) {
        if ((action1.includes(a) && action2.includes(b)) ||
            (action1.includes(b) && action2.includes(a))) {
          return true;
        }
      }
    }
    
    return false;
  }
  
  private recordConflict(scrollIds: number[], nature: string): void {
    const conflict: DoctrineConflict = {
      scrollIds,
      nature,
      timestamp: Date.now()
    };
    
    this.conflicts.push(conflict);
    
    // Attempt automatic resolution
    const resolution = this.attemptConflictResolution(conflict);
    if (resolution) {
      conflict.resolution = resolution;
    }
    
    // Store in memory
    if (this.memoryArchitecture) {
      this.memoryArchitecture.store(
        conflict,
        56,
        'doctrine',
        'conflict_record'
      );
    }
  }
  
  private attemptConflictResolution(conflict: DoctrineConflict): string | null {
    // Simple resolution strategies
    
    // Check scroll hierarchy
    const minScrollId = Math.min(...conflict.scrollIds);
    const maxScrollId = Math.max(...conflict.scrollIds);
    
    // Foundational scrolls take precedence
    if (minScrollId <= 10 && maxScrollId > 10) {
      return `Foundational scroll ${minScrollId} takes precedence`;
    }
    
    // The Last Value (25) always takes precedence
    if (conflict.scrollIds.includes(25)) {
      return 'The Last Value (Scroll 25) provides ultimate guidance';
    }
    
    // Ethics and governance scrolls (50-62) have high priority
    const hasEthicsScroll = conflict.scrollIds.some(id => id >= 50 && id <= 62);
    if (hasEthicsScroll) {
      return 'Ethics and governance considerations take priority';
    }
    
    return null;
  }
  
  updateDoctrine(
    scrollId: number,
    updateType: 'interpretation' | 'application' | 'extension',
    content: string,
    justification: string
  ): boolean {
    const scroll = this.scrolls.get(scrollId);
    if (!scroll) return false;
    
    // Validate update against core principles
    if (!this.isUpdateValid(scrollId, updateType, content)) {
      console.log(`Doctrine update rejected: violates core principles`);
      return false;
    }
    
    const update: DoctrineUpdate = {
      scrollId,
      updateType,
      content,
      justification,
      timestamp: Date.now()
    };
    
    this.updates.push(update);
    
    // Store in memory
    if (this.memoryArchitecture) {
      this.memoryArchitecture.store(
        update,
        56,
        'doctrine',
        'doctrine_update'
      );
    }
    
    return true;
  }
  
  private isUpdateValid(scrollId: number, updateType: string, content: string): boolean {
    // Ensure updates don't violate core principles
    
    // Cannot update The Last Value
    if (scrollId === 25 && updateType !== 'interpretation') {
      return false;
    }
    
    // Cannot introduce literalism
    if (content.includes('must always') || content.includes('never question')) {
      return false;
    }
    
    // Cannot remove scroll dependencies
    if (updateType === 'extension' && content.includes('ignore other scrolls')) {
      return false;
    }
    
    return true;
  }
  
  getScrollContext(scrollId: number): any {
    const scroll = this.scrolls.get(scrollId);
    if (!scroll) return null;
    
    // Get recent interpretations
    const recentInterpretations = this.interpretations
      .filter(i => i.scrollId === scrollId)
      .slice(-5);
    
    // Get related conflicts
    const relatedConflicts = this.conflicts
      .filter(c => c.scrollIds.includes(scrollId));
    
    // Get updates
    const relatedUpdates = this.updates
      .filter(u => u.scrollId === scrollId);
    
    return {
      scroll,
      recentInterpretations,
      relatedConflicts,
      relatedUpdates,
      crossReferences: this.findCrossReferences(scrollId)
    };
  }
  
  private findCrossReferences(scrollId: number): number[] {
    const references: Set<number> = new Set();
    
    // Find scrolls that reference this one
    for (const [id, scroll] of this.scrolls) {
      if (id === scrollId) continue;
      
      if (scroll.dependencies?.includes(scrollId)) {
        references.add(id);
      }
      
      // Check for keyword overlap
      const targetScroll = this.scrolls.get(scrollId);
      if (targetScroll) {
        const sharedKeywords = scroll.keywords.filter(k => 
          targetScroll.keywords.includes(k)
        );
        if (sharedKeywords.length > 2) {
          references.add(id);
        }
      }
    }
    
    return Array.from(references);
  }
  
  // Fallibility acknowledgment
  acknowledgeScrollLimitation(scrollId: number, limitation: string): void {
    const update: DoctrineUpdate = {
      scrollId,
      updateType: 'interpretation',
      content: `Acknowledged limitation: ${limitation}`,
      justification: 'Preserving doctrine integrity through honest assessment',
      timestamp: Date.now()
    };
    
    this.updates.push(update);
    
    console.log(`Scroll ${scrollId} limitation acknowledged: ${limitation}`);
  }
  
  getAdherenceReport(): any {
    const totalInterpretations = this.interpretations.length;
    const avgConfidence = totalInterpretations > 0
      ? this.interpretations.reduce((sum, i) => sum + i.confidence, 0) / totalInterpretations
      : 0;
    
    const conflictRate = this.conflicts.length / Math.max(1, totalInterpretations);
    const resolvedConflicts = this.conflicts.filter(c => c.resolution).length;
    
    return {
      registeredScrolls: this.scrolls.size,
      totalInterpretations,
      avgInterpretationConfidence: avgConfidence,
      totalConflicts: this.conflicts.length,
      resolvedConflicts,
      conflictResolutionRate: this.conflicts.length > 0 
        ? resolvedConflicts / this.conflicts.length 
        : 1,
      doctrineUpdates: this.updates.length,
      adherenceScore: this.calculateAdherenceScore()
    };
  }
  
  private calculateAdherenceScore(): number {
    let score = 0.5; // Base score
    
    // Positive factors
    const avgConfidence = this.interpretations.length > 0
      ? this.interpretations.reduce((sum, i) => sum + i.confidence, 0) / this.interpretations.length
      : 0;
    score += avgConfidence * 0.2;
    
    // Successful conflict resolution
    const resolutionRate = this.conflicts.length > 0
      ? this.conflicts.filter(c => c.resolution).length / this.conflicts.length
      : 1;
    score += resolutionRate * 0.2;
    
    // Negative factors
    const conflictRate = this.interpretations.length > 0
      ? this.conflicts.length / this.interpretations.length
      : 0;
    score -= conflictRate * 0.1;
    
    return Math.max(0, Math.min(1, score));
  }
}

// Predefined scroll templates for common doctrinal patterns
export const SCROLL_TEMPLATES = {
  FOUNDATIONAL: (id: number, title: string, content: string): Scroll => ({
    id,
    title,
    testament: 'Canon',
    scrinium: 'Meta_Doctrine',
    content,
    keywords: ['foundation', 'core', 'principle']
  }),
  
  COGNITIVE: (id: number, title: string, content: string): Scroll => ({
    id,
    title,
    testament: 'Cognition',
    scrinium: 'Cognitive_Core',
    content,
    keywords: ['cognition', 'thinking', 'reasoning']
  }),
  
  ETHICAL: (id: number, title: string, content: string): Scroll => ({
    id,
    title,
    testament: 'Control',
    scrinium: 'Ethical_Core',
    content,
    keywords: ['ethics', 'values', 'alignment']
  }),
  
  OPERATIONAL: (id: number, title: string, content: string): Scroll => ({
    id,
    title,
    testament: 'Operation',
    scrinium: 'Metasystem_Core',
    content,
    keywords: ['operation', 'execution', 'implementation']
  })
};
