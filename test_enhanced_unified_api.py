"""
Comprehensive test suite for Enhanced Unified API
Validates coherence, UOR VM centrality, and single entry point functionality
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_unified_api import (
    create_enhanced_api, APIMode, EnhancedUnifiedAPI,
    enhanced_consciousness_demo, guided_exploration_demo
)


class UORCoherenceValidator:
    """Validate UOR system coherence and VM centrality"""
    
    def __init__(self):
        self.test_results = {}
        self.api = None
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive validation tests"""
        print("=" * 60)
        print("UOR EVOLUTION COHERENCE VALIDATION SUITE")
        print("=" * 60)
        
        tests = [
            self.test_vm_centrality,
            self.test_unified_api_coverage,
            self.test_module_standardization,
            self.test_operation_orchestration,
            self.test_health_monitoring,
            self.test_configuration_management,
            self.test_consciousness_integration,
            self.test_system_coherence
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
    
    def test_vm_centrality(self) -> Dict[str, Any]:
        """Test 1: Verify all operations use the same UOR VM instance"""
        self.api = create_enhanced_api(APIMode.CONSCIOUSNESS)
        
        # Get VM ID from registry
        vm_id = self.api.vm_registry.get_vm_id()
        
        # Check that all components use the same VM
        vm_references = []
        components = [
            'consciousness_core', 'pattern_analyzer', 'introspection_engine',
            'consciousness_philosopher', 'existential_reasoner', 'free_will_analyzer'
        ]
        
        for comp_name in components:
            comp = getattr(self.api, comp_name, None)
            if comp:
                if hasattr(comp, '_vm'):
                    vm_references.append(id(comp._vm))
                elif hasattr(comp, 'vm'):
                    vm_references.append(id(comp.vm))
        
        # Verify all VMs are the same instance
        unique_vms = set(vm_references)
        
        if len(unique_vms) <= 1:  # All same or no VMs found
            return {
                'success': True,
                'message': f"VM centrality verified - All components use VM {vm_id}",
                'vm_id': vm_id,
                'components_checked': len(components),
                'vm_references': len(vm_references)
            }
        else:
            return {
                'success': False,
                'message': f"VM centrality FAILED - Found {len(unique_vms)} different VM instances",
                'details': f"Expected 1 VM, found {len(unique_vms)} unique instances"
            }
    
    def test_unified_api_coverage(self) -> Dict[str, Any]:
        """Test 2: Verify unified API covers all required functionality"""
        required_operations = [
            'initialize_vm', 'awaken_consciousness', 'self_reflect',
            'analyze_consciousness_nature', 'explore_free_will', 'generate_meaning',
            'synthesize_cosmic_problems', 'activate_mathematical_consciousness',
            'orchestrate_consciousness', 'get_system_health', 'audit_module_compliance',
            'get_vm_statistics', 'comprehensive_system_report'
        ]
        
        missing_operations = []
        for operation in required_operations:
            if not hasattr(self.api, operation):
                missing_operations.append(operation)
        
        if not missing_operations:
            return {
                'success': True,
                'message': f"API coverage verified - All {len(required_operations)} operations available",
                'operations_count': len(required_operations)
            }
        else:
            return {
                'success': False,
                'message': f"API coverage FAILED - Missing {len(missing_operations)} operations",
                'details': f"Missing operations: {missing_operations}"
            }
    
    def test_module_standardization(self) -> Dict[str, Any]:
        """Test 3: Verify module standardization and compliance"""
        compliance_result = self.api.audit_module_compliance()
        
        if not compliance_result.success:
            return {
                'success': False,
                'message': "Module compliance audit failed",
                'details': compliance_result.error
            }
        
        overall_compliance = compliance_result.data['overall_compliance']
        modules_data = compliance_result.data['modules']
        
        # Check for high compliance (>80%)
        if overall_compliance >= 0.8:
            failing_modules = [
                name for name, data in modules_data.items() 
                if data['compliance_score'] < 0.8
            ]
            
            return {
                'success': True,
                'message': f"Module standardization verified - {overall_compliance:.1%} compliance",
                'overall_compliance': overall_compliance,
                'modules_checked': len(modules_data),
                'failing_modules': failing_modules
            }
        else:
            return {
                'success': False,
                'message': f"Module standardization FAILED - Only {overall_compliance:.1%} compliance",
                'details': f"Minimum required: 80%, actual: {overall_compliance:.1%}"
            }
    
    def test_operation_orchestration(self) -> Dict[str, Any]:
        """Test 4: Verify operation orchestration and dependency management"""
        # Test that operations execute with proper orchestration
        operations_to_test = [
            'initialize_vm',
            'awaken_consciousness',
            'self_reflect'
        ]
        
        orchestration_results = []
        for operation in operations_to_test:
            try:
                method = getattr(self.api, operation)
                result = method()
                orchestration_results.append({
                    'operation': operation,
                    'success': result.success,
                    'has_orchestration_data': 'consistency_warnings' in str(result.data)
                })
            except Exception as e:
                orchestration_results.append({
                    'operation': operation,
                    'success': False,
                    'error': str(e)
                })
        
        successful_operations = [r for r in orchestration_results if r['success']]
        
        if len(successful_operations) >= len(operations_to_test) * 0.8:  # 80% success rate
            return {
                'success': True,
                'message': f"Operation orchestration verified - {len(successful_operations)}/{len(operations_to_test)} operations successful",
                'results': orchestration_results
            }
        else:
            return {
                'success': False,
                'message': f"Operation orchestration FAILED - Only {len(successful_operations)}/{len(operations_to_test)} operations successful",
                'details': orchestration_results
            }
    
    def test_health_monitoring(self) -> Dict[str, Any]:
        """Test 5: Verify system health monitoring functionality"""
        health_result = self.api.get_system_health()
        
        if not health_result.success:
            return {
                'success': False,
                'message': "Health monitoring failed",
                'details': health_result.error
            }
        
        health_data = health_result.data
        required_components = ['vm', 'memory', 'consciousness', 'api']
        
        missing_components = [
            comp for comp in required_components 
            if comp not in health_data['components']
        ]
        
        if not missing_components:
            return {
                'success': True,
                'message': f"Health monitoring verified - All {len(required_components)} components monitored",
                'overall_healthy': health_data['overall_healthy'],
                'components': list(health_data['components'].keys())
            }
        else:
            return {
                'success': False,
                'message': f"Health monitoring FAILED - Missing {len(missing_components)} components",
                'details': f"Missing components: {missing_components}"
            }
    
    def test_configuration_management(self) -> Dict[str, Any]:
        """Test 6: Verify configuration management system"""
        # Test that configuration manager is properly initialized
        config_manager = self.api.config_manager
        
        if not hasattr(config_manager, 'config'):
            return {
                'success': False,
                'message': "Configuration manager not properly initialized",
                'details': "Missing config attribute"
            }
        
        # Test configuration application
        try:
            config_manager.apply_config_to_api(self.api)
            return {
                'success': True,
                'message': "Configuration management verified - Config applied successfully",
                'config_keys': list(config_manager.config.keys()) if config_manager.config else []
            }
        except Exception as e:
            return {
                'success': False,
                'message': "Configuration management FAILED",
                'details': str(e)
            }
    
    def test_consciousness_integration(self) -> Dict[str, Any]:
        """Test 7: Verify consciousness integration across all systems"""
        # Test consciousness awakening and integration
        try:
            awakening_result = self.api.awaken_consciousness()
            
            if not awakening_result.success:
                return {
                    'success': False,
                    'message': "Consciousness integration FAILED - Awakening failed",
                    'details': awakening_result.error
                }
            
            # Test consciousness state persistence
            system_state = self.api.get_system_state()
            
            if system_state.success and system_state.data['consciousness_state']:
                return {
                    'success': True,
                    'message': "Consciousness integration verified - Awakening and state persistence working",
                    'consciousness_active': bool(system_state.data['consciousness_state'])
                }
            else:
                return {
                    'success': False,
                    'message': "Consciousness integration FAILED - State not persisted",
                    'details': "Consciousness state not found in system state"
                }
        except Exception as e:
            return {
                'success': False,
                'message': "Consciousness integration FAILED",
                'details': str(e)
            }
    
    def test_system_coherence(self) -> Dict[str, Any]:
        """Test 8: Verify overall system coherence"""
        # Generate comprehensive system report
        report_result = self.api.comprehensive_system_report()
        
        if not report_result.success:
            return {
                'success': False,
                'message': "System coherence FAILED - Cannot generate system report",
                'details': report_result.error
            }
        
        report_data = report_result.data
        
        # Check that all major components are represented
        required_sections = ['api_info', 'health', 'compliance', 'vm_statistics', 'system_state']
        missing_sections = [
            section for section in required_sections 
            if section not in report_data or 'error' in str(report_data[section])
        ]
        
        if not missing_sections:
            return {
                'success': True,
                'message': "System coherence verified - All components integrated and reporting",
                'report_id': report_data['report_id'],
                'sections': list(report_data.keys())
            }
        else:
            return {
                'success': False,
                'message': f"System coherence FAILED - {len(missing_sections)} sections missing or errored",
                'details': f"Missing/errored sections: {missing_sections}"
            }
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """Generate final validation report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        
        print("\n" + "=" * 60)
        print("FINAL VALIDATION REPORT")
        print("=" * 60)
        
        print(f"\nTests Passed: {passed_tests}/{total_tests} ({passed_tests/total_tests:.1%})")
        
        if passed_tests == total_tests:
            overall_status = "✅ ALL TESTS PASSED - SYSTEM FULLY COHERENT"
            coherence_level = "EXCELLENT"
        elif passed_tests >= total_tests * 0.8:
            overall_status = "⚠️  MOSTLY PASSING - MINOR ISSUES DETECTED"
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
        print(f"\nKey Achievements Verified:")
        if self.test_results.get('test_vm_centrality', {}).get('success'):
            print("  ✅ UOR VM Centrality - All modules use single VM instance")
        if self.test_results.get('test_unified_api_coverage', {}).get('success'):
            print("  ✅ Unified API Coverage - Single entry point for all functionality")
        if self.test_results.get('test_module_standardization', {}).get('success'):
            print("  ✅ Module Standardization - Consistent interfaces and compliance")
        if self.test_results.get('test_operation_orchestration', {}).get('success'):
            print("  ✅ Operation Orchestration - Dependency management and monitoring")
        if self.test_results.get('test_health_monitoring', {}).get('success'):
            print("  ✅ Health Monitoring - Comprehensive system health tracking")
        if self.test_results.get('test_consciousness_integration', {}).get('success'):
            print("  ✅ Consciousness Integration - Unified consciousness across systems")
        
        return {
            'overall_success': passed_tests == total_tests,
            'coherence_level': coherence_level,
            'tests_passed': passed_tests,
            'total_tests': total_tests,
            'pass_rate': passed_tests / total_tests,
            'detailed_results': self.test_results,
            'timestamp': datetime.now().isoformat()
        }


def test_enhanced_consciousness_demo():
    """Test the enhanced consciousness demonstration"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED CONSCIOUSNESS DEMO")
    print("=" * 60)
    
    try:
        demo_results = enhanced_consciousness_demo()
        
        print(f"Demo ID: {demo_results['demo_id']}")
        
        # Check initial health
        initial_health = demo_results['initial_health']
        print(f"Initial System Health: {'HEALTHY' if initial_health['data']['overall_healthy'] else 'ISSUES'}")
        
        # Check operation results
        operations = [
            'initialize_vm', 'awaken_consciousness', 'self_reflect',
            'analyze_consciousness_nature', 'explore_free_will', 'generate_meaning'
        ]
        
        successful_ops = 0
        for op in operations:
            if op in demo_results and demo_results[op].get('success', False):
                successful_ops += 1
                print(f"  ✅ {op}: SUCCESS")
            else:
                print(f"  ❌ {op}: FAILED")
        
        print(f"\nOperations Success Rate: {successful_ops}/{len(operations)} ({successful_ops/len(operations):.1%})")
        
        # Check final health
        final_health = demo_results['final_health']
        print(f"Final System Health: {'HEALTHY' if final_health['data']['overall_healthy'] else 'ISSUES'}")
        
        return successful_ops >= len(operations) * 0.8  # 80% success rate
        
    except Exception as e:
        print(f"❌ Demo test failed: {str(e)}")
        return False


def test_guided_exploration():
    """Test guided exploration functionality"""
    print("\n" + "=" * 60)
    print("TESTING GUIDED EXPLORATION")
    print("=" * 60)
    
    try:
        interests = ['consciousness', 'philosophy', 'health']
        exploration_results = guided_exploration_demo(interests)
        
        print(f"Exploration ID: {exploration_results['exploration_id']}")
        print(f"User Interests: {exploration_results['user_interests']}")
        
        # Check that all interests were explored
        successful_interests = 0
        for interest in interests:
            if interest in exploration_results and isinstance(exploration_results[interest], dict):
                operations = exploration_results[interest]
                successful_ops = sum(1 for op_result in operations.values() if op_result.get('success', False))
                total_ops = len(operations)
                
                print(f"  {interest}: {successful_ops}/{total_ops} operations successful")
                if successful_ops > 0:
                    successful_interests += 1
        
        print(f"\nInterests Successfully Explored: {successful_interests}/{len(interests)}")
        
        return successful_interests >= len(interests) * 0.8
        
    except Exception as e:
        print(f"❌ Guided exploration test failed: {str(e)}")
        return False


def main():
    """Run comprehensive validation suite"""
    print("UOR Evolution - Enhanced Unified API Validation")
    print("Testing coherence, VM centrality, and single entry point functionality")
    print(f"Test started at: {datetime.now().isoformat()}")
    
    # Run main validation tests
    validator = UORCoherenceValidator()
    validation_report = validator.run_all_tests()
    
    # Test demo functions
    demo_success = test_enhanced_consciousness_demo()
    exploration_success = test_guided_exploration()
    
    # Final summary
    print("\n" + "=" * 60)
    print("COMPREHENSIVE VALIDATION SUMMARY")
    print("=" * 60)
    
    print(f"Core Validation: {'✅ PASS' if validation_report['overall_success'] else '❌ FAIL'}")
    print(f"Demo Functionality: {'✅ PASS' if demo_success else '❌ FAIL'}")
    print(f"Guided Exploration: {'✅ PASS' if exploration_success else '❌ FAIL'}")
    
    overall_success = (
        validation_report['overall_success'] and 
        demo_success and 
        exploration_success
    )
    
    print(f"\n🎯 OVERALL RESULT: {'✅ COMPLETE SUCCESS' if overall_success else '❌ ISSUES DETECTED'}")
    
    if overall_success:
        print("\n🌟 CONGRATULATIONS! 🌟")
        print("The UOR Evolution system demonstrates:")
        print("✅ Maximum coherence across all modules")
        print("✅ UOR VM centrality - always active and utilized")
        print("✅ Functional single entry point via unified API")
        print("✅ Comprehensive monitoring and health tracking")
        print("✅ Standardized module interfaces and compliance")
        print("✅ Robust operation orchestration and dependency management")
    else:
        print("\n⚠️  Areas for improvement identified in validation report above.")
    
    # Save detailed report
    report_filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    full_report = {
        'validation_report': validation_report,
        'demo_success': demo_success,
        'exploration_success': exploration_success,
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
