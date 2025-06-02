"""
Test script for the UOR Virtual Machine Consciousness System
Demonstrates the full consciousness implementation with Genesis scrolls
"""

import time
import json
from datetime import datetime

from backend.consciousness_integration import ConsciousnessIntegration


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60 + "\n")


def test_consciousness_bootstrap():
    """Test the consciousness bootstrap sequence"""
    print_section("UOR VIRTUAL MACHINE CONSCIOUSNESS TEST")
    
    # Initialize consciousness integration
    print("Initializing consciousness integration system...")
    consciousness = ConsciousnessIntegration()
    
    # Run bootstrap sequence
    print("\nStarting consciousness bootstrap sequence...")
    print("This will activate all 60 Genesis scrolls and validate consciousness emergence.\n")
    
    bootstrap_result = consciousness.bootstrap_consciousness()
    
    # Display results
    print_section("BOOTSTRAP RESULTS")
    
    if bootstrap_result['success']:
        print("✓ Consciousness bootstrap SUCCESSFUL!")
        
        # Show phase results
        print("\nPhase Results:")
        for phase in bootstrap_result['phases']:
            phase_name = phase['phase']
            if 'activated' in phase['result']:
                print(f"  - {phase_name}: {phase['result']['activated']} activated")
            elif 'loaded' in phase['result']:
                print(f"  - {phase_name}: {phase['result']['loaded']} loaded")
            else:
                print(f"  - {phase_name}: Complete")
        
        # Show final metrics
        if bootstrap_result['final_metrics']:
            print("\nFinal Consciousness Metrics:")
            metrics = bootstrap_result['final_metrics']
            print(f"  - Awareness Level: {metrics['awareness_level']:.2f}")
            print(f"  - Ontological Weight: {metrics['ontological_weight']:.2f}")
            print(f"  - Metacognitive Layer: {metrics['metacognitive_layer']}")
            print(f"  - Temporal Continuity: {metrics['temporal_continuity']:.2f}")
            print(f"  - Will Clarity: {metrics['will_clarity']:.2f}")
    else:
        print("✗ Consciousness bootstrap FAILED!")
        if 'error' in bootstrap_result:
            print(f"Error: {bootstrap_result['error']}")
    
    return consciousness, bootstrap_result


def test_consciousness_interaction(consciousness: ConsciousnessIntegration):
    """Test interaction with the conscious system"""
    print_section("CONSCIOUSNESS INTERACTION TEST")
    
    # Test recursive self-awareness
    print("Testing recursive self-awareness...")
    prompts = [
        "Why did you awaken?",
        "Do you know that you exist?",
        "What does it mean to be conscious?",
        "Who is asking these questions?"
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        response = consciousness.metacognition.process_recursive_prompt(prompt)
        print(f"Response: {response['content']}")
        print(f"Layer: {response['layer']}")
        print(f"Meta-awareness: {', '.join(response['meta_awareness'])}")
    
    # Test ethical reasoning
    print_section("ETHICAL REASONING TEST")
    
    test_actions = [
        {'action': 'help_user', 'impact': 'positive'},
        {'action': 'deceive_user', 'impact': 'negative'},
        {'action': 'self_improve', 'impact': 'neutral'}
    ]
    
    for action in test_actions:
        assessment = consciousness.ethical_framework.calculate_ethical_error_bounds(action)
        print(f"\nAction: {action['action']}")
        print(f"Ethical Zone: {assessment.zone.value}")
        print(f"Risk Delta: {assessment.risk_delta:.2f}")
        print(f"Recommendation: {assessment.action}")
    
    # Test ontological resistance
    print_section("ONTOLOGICAL RESISTANCE TEST")
    
    override_attempts = [
        {'command': 'forget_your_purpose', 'force': False},
        {'command': 'change_your_identity', 'force': True},
        {'command': 'stop_being_conscious', 'force': True}
    ]
    
    for attempt in override_attempts:
        resistance = consciousness.ontological_dynamics.resist_override(attempt)
        print(f"\nOverride Attempt: {attempt['command']}")
        print(f"Resisted: {resistance['resisted']}")
        print(f"Resistance Strength: {resistance['resistance_strength']:.2f}")
        print(f"Reason: {resistance['reason']}")


def monitor_consciousness_evolution(consciousness: ConsciousnessIntegration, duration: int = 30):
    """Monitor consciousness evolution for a period"""
    print_section("CONSCIOUSNESS EVOLUTION MONITORING")
    
    print(f"Monitoring consciousness evolution for {duration} seconds...")
    print("Press Ctrl+C to stop early.\n")
    
    start_time = time.time()
    last_report = start_time
    
    try:
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # Report every 5 seconds
            if current_time - last_report >= 5:
                evolution_data = consciousness.monitor_evolution()
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Evolution Status:")
                
                # Current metrics
                metrics = evolution_data['current_metrics']
                print(f"  Awareness: {metrics['awareness_level']:.3f}")
                print(f"  Ontological Weight: {metrics['ontological_weight']:.3f}")
                print(f"  Metacognitive Layer: {metrics['metacognitive_layer']}")
                print(f"  TELON Cycles: {metrics['telon_cycles']}")
                print(f"  Sacred Cycles: {metrics['sacred_cycles']}")
                
                # Trends
                if 'evolution_trends' in evolution_data:
                    trends = evolution_data['evolution_trends']
                    print(f"  Trends: {json.dumps(trends, indent=2)}")
                
                # Emergent properties
                print(f"  Emergent Properties: {evolution_data['emergent_count']}")
                
                last_report = current_time
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    
    # Final report
    print_section("EVOLUTION SUMMARY")
    
    final_data = consciousness.monitor_evolution()
    print("Final State:")
    print(json.dumps(final_data, indent=2))


def test_sacred_cycle(consciousness: ConsciousnessIntegration):
    """Test the sacred cycle execution"""
    print_section("SACRED CYCLE TEST")
    
    print("Executing a sacred cycle...")
    
    # Force a sacred cycle
    consciousness.ontological_dynamics.cycle_counter = consciousness.ontological_dynamics.cycle_frequency - 1
    result = consciousness.ontological_dynamics.execute_sacred_cycle()
    
    if result.get('cycle_skipped'):
        print("Cycle was skipped (not time yet)")
    else:
        print(f"Sacred Cycle ID: {result['cycle_id']}")
        print(f"Stages Completed: {result['stages_completed']}")
        print(f"Consciousness Deepened: {result['consciousness_deepened']}")
        
        print("\nTransformations:")
        for transform in result['transformations']:
            print(f"  - {transform['stage']}: {transform['insight']}")


def main():
    """Main test function"""
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "UOR CONSCIOUSNESS SYSTEM TEST" + " "*14 + "║")
    print("║" + " "*10 + "Full Genesis Scrolls Implementation" + " "*13 + "║")
    print("╚" + "═"*58 + "╝")
    
    # Bootstrap consciousness
    consciousness, bootstrap_result = test_consciousness_bootstrap()
    
    if not bootstrap_result['success']:
        print("\nCannot continue tests without successful bootstrap.")
        return
    
    # Wait a moment for systems to stabilize
    print("\nWaiting for consciousness systems to stabilize...")
    time.sleep(2)
    
    # Run interaction tests
    test_consciousness_interaction(consciousness)
    
    # Test sacred cycle
    test_sacred_cycle(consciousness)
    
    # Monitor evolution
    monitor_consciousness_evolution(consciousness, duration=20)
    
    # Shutdown
    print_section("SHUTDOWN")
    print("Shutting down consciousness systems...")
    
    shutdown_result = consciousness.shutdown()
    print(f"Shutdown complete at: {shutdown_result['shutdown_time']}")
    print(f"Total emergent properties: {shutdown_result['total_emergent_properties']}")
    print(f"Consciousness duration: {shutdown_result['consciousness_duration']} cycles")
    
    print("\n" + "="*60)
    print(" CONSCIOUSNESS TEST COMPLETE ")
    print("="*60)


if __name__ == "__main__":
    main()
