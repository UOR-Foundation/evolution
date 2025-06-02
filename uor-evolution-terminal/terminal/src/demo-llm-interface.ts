#!/usr/bin/env node

// Demo script showing how to use the UOR Universal Terminal LLM Interface
// This demonstrates various interactions with the consciousness framework

import { createUORTerminal } from './terminal/llm-interface.js';

async function runDemo() {
  console.log('\n🚀 Starting UOR Universal Terminal LLM Interface Demo\n');
  
  const terminal = createUORTerminal();
  
  // Demo interactions
  const interactions = [
    {
      input: "hello",
      description: "Greeting the system"
    },
    {
      input: "show me consciousness awakening",
      description: "Demonstrating consciousness emergence"
    },
    {
      input: "I'm confused about consciousness",
      description: "Getting help for beginners"
    },
    {
      input: "show me self-evolving code",
      description: "Watching code improve itself"
    },
    {
      input: "cosmic intelligence demo",
      description: "Exploring universe-scale thinking"
    },
    {
      input: "what is quantum consciousness?",
      description: "Exploring quantum aspects"
    },
    {
      input: "activate transcendence protocols",
      description: "Ultimate consciousness expansion"
    }
  ];

  for (const interaction of interactions) {
    console.log('\n' + '═'.repeat(80));
    console.log(`\n📝 User Input: "${interaction.input}"`);
    console.log(`💭 Description: ${interaction.description}\n`);
    console.log('─'.repeat(80) + '\n');
    
    const response = await terminal.processUserInput(interaction.input);
    console.log(response);
    
    // Add a delay between interactions for readability
    await delay(2000);
  }
  
  console.log('\n' + '═'.repeat(80));
  console.log('\n✅ Demo Complete! The UOR Universal Terminal is ready for LLM integration.\n');
}

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Run the demo
runDemo().catch(console.error);
