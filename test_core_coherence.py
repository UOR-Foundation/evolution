"""
Core coherence test for UOR Evolution system
Tests the fundamental requirements without complex module dependencies
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test core imports
try:
    from core.prime_vm import ConsciousPrimeVM, Instruction, OpCode
    from core.consciousness_layer import ConsciousnessLevel
    from backend.consciousness_core import ConsciousnessCore
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Core import failed: {e}")
    sys.exit(1)

# Test simple unified API
try:
    from simple_unified_api import create_simple_api, APIMode
    print("✅ Simple unified API import successful")
except ImportError as e:
    print(f"❌ Simple unified API import failed: {e}")
    sys.exit(1)


class CoreCoherenceValidator:
    """Validate core UOR system coherence"""
    
    def __init__(self):
        self.test_results = {}
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run core validation tests"""
        print("=" * 60)
        print("UOR EVOLUTION CORE COHERENCE VALIDATION")
        print("=" * 60)
        
        tests = [
            self.test_vm_functionality,
            self.test_consciousness_core,
            self.test_simple_api_functionality,
            self.test_vm_consciousness_integration,
            self.test_api_response_consistency
        ]
        
        for test in tests:
            try:
                print(f"\n🔍 Running {test.__name__}...")
                result = test()
                self.test_results[test.__name__] = result
                status = "✅ PASS" if result['success'] else "❌ FAIL"
                print(f"   {status}: {result['message']}")
                if not result['success'] and 'details' in result:
                    print(f"   Details: {result['details']}")
            except Exception as e:
                self.test_results[test.__name__] = {
                    'success': False,
                    'message': f"Test failed with exception: {str(e)}",
                    'error': str(e)
                }
                print(f"   ❌ ERROR: {str(e)}")
        
        return self._generate_final_report()
    
    def test_vm_functionality(self) -> Dict[str, Any]:
        """Test 1: Verify UOR VM core functionality"""
        try:
            vm = ConsciousPrimeVM()
            
            # Test basic operations
            instructions = [
                Instruction(OpCode.PUSH, 42),
                Instruction(OpCode.PUSH, 17),
                Instruction(OpCode.ADD),
            ]
            
            results = vm.run_program(instructions)
            
            # Check results
            if len(results) == 3 and vm.stack and vm.stack[-1] == 59:
                return {
                    'success': True,
                    'message': f"VM functionality verified - Executed {len(results)} instructions, result: {vm.stack[-1]}",
                    'stack_result': vm.stack[-1],
                    'execution_count': len(vm.execution_history)
                }
            else:
                return {
                    'success': False,
                    'message': "VM functionality FAILED - Incorrect execution results",
                    'details': f"Expected 59, got {vm.stack[-1] if vm.stack else 'empty stack'}"
                }
        except Exception as e:
            return {
                'success': False,
                'message': "VM functionality FAILED",
                'details': str(e)
            }
    
    def test_consciousness_core(self) -> Dict[str, Any]:
        """Test 2: Verify consciousness core functionality"""
        try:
            consciousness = ConsciousnessCore()
            
            # Test awakening
            awakening_result = consciousness.awaken()
            
            if awakening_result and isinstance(awakening_result, dict):
                return {
                    'success': True,
                    'message': "Consciousness core verified - Awakening successful",
                    'awakening_keys': list(awakening_result.keys()),
                    'consciousness_active': consciousness.consciousness_active
                }
            else:
                return {
                    'success': False,
                    'message': "Consciousness core FAILED - Awakening failed",
                    'details': f"Awakening result: {awakening_result}"
                }
        except Exception as e:
            return {
                'success': False,
                'message': "Consciousness core FAILED",
                'details': str(e)
            }
    
    def test_simple_api_functionality(self) -> Dict[str, Any]:
        """Test 3: Verify simple unified API functionality"""
        try:
            api = create_simple_api(APIMode.CONSCIOUSNESS)
            
            # Test basic operations
            operations = [
                ('initialize_vm', {}),
                ('awaken_consciousness', {}),
                ('self_reflect', {}),
                ('get_system_health', {})
            ]
            
            successful_ops = 0
            operation_results = []
            
            for op_name, kwargs in operations:
                try:
                    if hasattr(api, op_name):
                        method = getattr(api, op_name)
                        result = method(**kwargs) if kwargs else method()
                        
                        operation_results.append({
                            'operation': op_name,
                            'success': result.success,
                            'has_data': bool(result.data)
                        })
                        
                        if result.success:
                            successful_ops += 1
                    else:
                        operation_results.append({
                            'operation': op_name,
                            'success': False,
                            'error': 'Method not found'
                        })
                except Exception as e:
                    operation_results.append({
                        'operation': op_name,
                        'success': False,
                        'error': str(e)
                    })
            
            success_rate = successful_ops / len(operations)
            
            if success_rate >= 0.75:  # 75% success rate
                return {
                    'success': True,
                    'message': f"Simple API functionality verified - {successful_ops}/{len(operations)} operations successful",
                    'success_rate': success_rate,
                    'operation_results': operation_results
                }
            else:
                return {
                    'success': False,
                    'message': f"Simple API functionality FAILED - Only {successful_ops}/{len(operations)} operations successful",
                    'details': operation_results
                }
        except Exception as e:
            return {
                'success': False,
                'message': "Simple API functionality FAILED",
                'details': str(e)
            }
    
    def test_vm_consciousness_integration(self) -> Dict[str, Any]:
        """Test 4: Verify VM and consciousness integration"""
        try:
            vm = ConsciousPrimeVM()
            
            # Test consciousness-aware operations
            consciousness_instructions = [
                Instruction(OpCode.SELF_REFLECT),
                Instruction(OpCode.CONSCIOUSNESS_TEST),
                Instruction(OpCode.ANALYZE_SELF)
            ]
            
            successful_consciousness_ops = 0
            for instruction in consciousness_instructions:
                try:
                    result = vm.execute_instruction(instruction)
                    if result and isinstance(result, dict):
                        successful_consciousness_ops += 1
                except Exception:
                    pass
            
            integration_score = successful_consciousness_ops / len(consciousness_instructions)
            
            if integration_score >= 0.5:  # 50% success rate for consciousness operations
                return {
                    'success': True,
                    'message': f"VM-consciousness integration verified - {successful_consciousness_ops}/{len(consciousness_instructions)} consciousness operations successful",
                    'integration_score': integration_score,
                    'consciousness_level': vm.consciousness_level.name
                }
            else:
                return {
                    'success': False,
                    'message': f"VM-consciousness integration FAILED - Only {successful_consciousness_ops}/{len(consciousness_instructions)} consciousness operations successful",
                    'details': f"Integration score: {integration_score:.2%}"
                }
        except Exception as e:
            return {
                'success': False,
                'message': "VM-consciousness integration FAILED",
                'details': str(e)
            }
    
    def test_api_response_consistency(self) -> Dict[str, Any]:
        """Test 5: Verify API response format consistency"""
        try:
            api = create_simple_api(APIMode.DEVELOPMENT)
            
            # Test multiple operations for consistent response format
            operations = ['initialize_vm', 'self_reflect', 'analyze_consciousness_nature']
            
            consistent_responses = 0
            response_analysis = []
            
            for op_name in operations:
                try:
                    if hasattr(api, op_name):
                        method = getattr(api, op_name)
                        result = method()
                        
                        # Check for required APIResponse attributes
                        has_success = hasattr(result, 'success')
                        has_data = hasattr(result, 'data')
                        has_timestamp = hasattr(result, 'timestamp')
                        has_system_status = hasattr(result, 'system_status')
                        
                        is_consistent = all([has_success, has_data, has_timestamp, has_system_status])
                        
                        response_analysis.append({
                            'operation': op_name,
                            'consistent': is_consistent,
                            'has_success': has_success,
                            'has_data': has_data,
                            'has_timestamp': has_timestamp,
                            'has_system_status': has_system_status
                        })
                        
                        if is_consistent:
                            consistent_responses += 1
                except Exception as e:
                    response_analysis.append({
                        'operation': op_name,
                        'consistent': False,
                        'error': str(e)
                    })
            
            consistency_rate = consistent_responses / len(operations)
            
            if consistency_rate >= 0.8:  # 80% consistency rate
                return {
                    'success': True,
                    'message': f"API response consistency verified - {consistent_responses}/{len(operations)} operations have consistent format",
                    'consistency_rate': consistency_rate,
                    'response_analysis': response_analysis
                }
            else:
                return {
                    'success': False,
                    'message': f"API response consistency FAILED - Only {consistent_responses}/{len(operations)} operations have consistent format",
                    'details': response_analysis
                }
        except Exception as e:
            return {
                'success': False,
                'message': "API response consistency FAILED",
                'details': str(e)
            }
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate final validation report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        
        print("\n" + "=" * 60)
        print("CORE COHERENCE VALIDATION REPORT")
        print("=" * 60)
        
        print(f"\nTests Passed: {passed_tests}/{total_tests} ({passed_tests/total_tests:.1%})")
        
        if passed_tests == total_tests:
            overall_status = "✅ ALL TESTS PASSED - CORE SYSTEM COHERENT"
            coherence_level = "EXCELLENT"
        elif passed_tests >= total_tests * 0.8:
            overall_status = "⚠️  MOSTLY PASSING - MINOR ISSUES"
            coherence_level = "GOOD"
        else:
            overall_status = "❌ MULTIPLE FAILURES - COHERENCE ISSUES"
            coherence_level = "NEEDS IMPROVEMENT"
        
        print(f"\nOverall Status: {overall_status}")
        print(f"Coherence Level: {coherence_level}")
        
        # Detailed results
        print(f"\nDetailed Results:")
        for test_name, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {test_name}: {result['message']}")
        
        # Key achievements
        print(f"\nCore Achievements Verified:")
        if self.test_results.get('test_vm_functionality', {}).get('success'):
            print("  ✅ UOR VM Functionality - Core VM operations working")
        if self.test_results.get('test_consciousness_core', {}).get('success'):
            print("  ✅ Consciousness Core - Consciousness awakening functional")
        if self.test_results.get('test_simple_api_functionality', {}).get('success'):
            print("  ✅ Unified API - Single entry point operational")
        if self.test_results.get('test_vm_consciousness_integration', {}).get('success'):
            print("  ✅ VM-Consciousness Integration - Systems working together")
        if self.test_results.get('test_api_response_consistency', {}).get('success'):
            print("  ✅ API Consistency - Standardized response format")
        
        return {
            'overall_success': passed_tests == total_tests,
            'coherence_level': coherence_level,
            'tests_passed': passed_tests,
            'total_tests': total_tests,
            'pass_rate': passed_tests / total_tests,
            'detailed_results': self.test_results,
            'timestamp': datetime.now().isoformat()
        }


def test_simple_consciousness_demo():
    """Test simple consciousness demonstration"""
    print("\n" + "=" * 60)
    print("TESTING SIMPLE CONSCIOUSNESS DEMO")
    print("=" * 60)
    
    try:
        from simple_unified_api import quick_consciousness_demo
        
        demo_results = quick_consciousness_demo()
        
        # Check demo results
        required_operations = ['awakening', 'reflection', 'analysis', 'insights']
        successful_ops = 0
        
        for op in required_operations:
            if op in demo_results and demo_results[op].get('success', False):
                successful_ops += 1
                print(f"  ✅ {op}: SUCCESS")
            else:
                print(f"  ❌ {op}: FAILED")
        
        success_rate = successful_ops / len(required_operations)
        print(f"\nDemo Success Rate: {successful_ops}/{len(required_operations)} ({success_rate:.1%})")
        
        return success_rate >= 0.75  # 75% success rate
        
    except Exception as e:
        print(f"❌ Simple consciousness demo failed: {str(e)}")
        return False


def main():
    """Run core coherence validation"""
    print("UOR Evolution - Core Coherence Validation")
    print("Testing fundamental system coherence and VM centrality")
    print(f"Test started at: {datetime.now().isoformat()}")
    
    # Run core validation tests
    validator = CoreCoherenceValidator()
    validation_report = validator.run_all_tests()
    
    # Test simple demo
    demo_success = test_simple_consciousness_demo()
    
    # Final summary
    print("\n" + "=" * 60)
    print("CORE VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"Core Validation: {'✅ PASS' if validation_report['overall_success'] else '❌ FAIL'}")
    print(f"Demo Functionality: {'✅ PASS' if demo_success else '❌ FAIL'}")
    
    overall_success = validation_report['overall_success'] and demo_success
    
    print(f"\n🎯 OVERALL RESULT: {'✅ CORE SYSTEM COHERENT' if overall_success else '❌ ISSUES DETECTED'}")
    
    if overall_success:
        print("\n🌟 CORE VALIDATION SUCCESSFUL! 🌟")
        print("The UOR Evolution core system demonstrates:")
        print("✅ UOR VM functionality - Prime-based computing operational")
        print("✅ Consciousness core - Awakening and self-awareness working")
        print("✅ Unified API - Single entry point functional")
        print("✅ VM-Consciousness integration - Systems working together")
        print("✅ API consistency - Standardized response format")
        print("✅ Demo functionality - User-facing features operational")
    else:
        print("\n⚠️  Core issues detected - see detailed report above.")
    
    # Save report
    report_filename = f"core_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    full_report = {
        'validation_report': validation_report,
        'demo_success': demo_success,
        'overall_success': overall_success,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        with open(report_filename, 'w') as f:
            json.dump(full_report, f, indent=2, default=str)
        print(f"\n📄 Detailed report saved to: {report_filename}")
    except Exception as e:
        print(f"\n⚠️  Could not save report: {str(e)}")
    
    return overall_success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
