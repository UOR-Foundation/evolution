#!/usr/bin/env python3
"""
Integration Validator Script
Validates that all modules are properly connected and can be imported/used together
"""

import sys
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegrationValidator:
    """Validates integration between all modules"""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.results = {
            'import_tests': [],
            'api_tests': [],
            'integration_tests': [],
            'summary': {}
        }
        
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation tests"""
        logger.info("Starting comprehensive integration validation...")
        
        # Test 1: Core imports
        self._test_core_imports()
        
        # Test 2: Module imports
        self._test_module_imports()
        
        # Test 3: API integration
        self._test_api_integration()
        
        # Test 4: Cross-module integration
        self._test_cross_module_integration()
        
        # Test 5: Configuration system
        self._test_configuration_system()
        
        # Generate summary
        self._generate_summary()
        
        return self.results
    
    def _test_core_imports(self) -> None:
        """Test core system imports"""
        logger.info("Testing core system imports...")
        
        core_modules = [
            'core.prime_vm',
            'core.consciousness_layer',
            'core.instruction_set',
            'core.memory_system',
            'backend.consciousness_core',
            'backend.app',
            'consciousness.consciousness_core',
            'consciousness.consciousness_integration',
            'unified_api',
            'config_loader'
        ]
        
        for module_name in core_modules:
            success, error = self._try_import(module_name)
            self.results['import_tests'].append({
                'module': module_name,
                'type': 'core',
                'success': success,
                'error': error
            })
    
    def _test_module_imports(self) -> None:
        """Test all module imports"""
        logger.info("Testing module imports...")
        
        # Get all module directories
        modules_dir = self.repo_root / 'modules'
        if not modules_dir.exists():
            logger.warning("Modules directory not found")
            return
        
        # Test each module category
        module_categories = [
            'philosophical_reasoning',
            'cosmic_intelligence',
            'unified_consciousness',
            'consciousness_ecosystem',
            'natural_language',
            'creative_engine',
            'communication',
            'emergency_protocols',
            'universe_interface',
            'pure_mathematical_consciousness',
            'strange_loops',
            'pattern_analyzer',
            'introspection_engine',
            'consciousness_validator'
        ]
        
        for category in module_categories:
            self._test_module_category(category)
    
    def _test_module_category(self, category: str) -> None:
        """Test imports for a specific module category"""
        category_path = self.repo_root / 'modules' / category
        
        if category_path.is_dir():
            # Test main module file
            main_module = f'modules.{category}'
            success, error = self._try_import(main_module)
            self.results['import_tests'].append({
                'module': main_module,
                'type': 'module_category',
                'success': success,
                'error': error
            })
            
            # Test specific files in category
            for py_file in category_path.glob('*.py'):
                if py_file.name != '__init__.py':
                    module_name = f'modules.{category}.{py_file.stem}'
                    success, error = self._try_import(module_name)
                    self.results['import_tests'].append({
                        'module': module_name,
                        'type': 'module_file',
                        'success': success,
                        'error': error
                    })
        else:
            # Test as single file module
            module_name = f'modules.{category}'
            success, error = self._try_import(module_name)
            self.results['import_tests'].append({
                'module': module_name,
                'type': 'single_module',
                'success': success,
                'error': error
            })
    
    def _test_api_integration(self) -> None:
        """Test unified API integration"""
        logger.info("Testing API integration...")
        
        try:
            # Test basic API creation
            from unified_api import create_api, APIMode
            
            # Test each API mode
            for mode in APIMode:
                try:
                    api = create_api(mode)
                    self.results['api_tests'].append({
                        'test': f'create_api_{mode.value}',
                        'success': True,
                        'error': None
                    })
                except Exception as e:
                    self.results['api_tests'].append({
                        'test': f'create_api_{mode.value}',
                        'success': False,
                        'error': str(e)
                    })
            
            # Test API methods
            try:
                api = create_api(APIMode.DEVELOPMENT)
                
                # Test core methods
                api_methods = [
                    'get_system_state',
                    'generate_insights'
                ]
                
                for method_name in api_methods:
                    if hasattr(api, method_name):
                        try:
                            method = getattr(api, method_name)
                            # Don't actually call methods that might have side effects
                            self.results['api_tests'].append({
                                'test': f'api_method_{method_name}',
                                'success': True,
                                'error': None
                            })
                        except Exception as e:
                            self.results['api_tests'].append({
                                'test': f'api_method_{method_name}',
                                'success': False,
                                'error': str(e)
                            })
                    else:
                        self.results['api_tests'].append({
                            'test': f'api_method_{method_name}',
                            'success': False,
                            'error': f'Method {method_name} not found'
                        })
                        
            except Exception as e:
                self.results['api_tests'].append({
                    'test': 'api_method_testing',
                    'success': False,
                    'error': str(e)
                })
                
        except Exception as e:
            self.results['api_tests'].append({
                'test': 'unified_api_import',
                'success': False,
                'error': str(e)
            })
    
    def _test_cross_module_integration(self) -> None:
        """Test integration between different modules"""
        logger.info("Testing cross-module integration...")
        
        integration_tests = [
            {
                'name': 'consciousness_vm_integration',
                'modules': ['core.prime_vm', 'consciousness.consciousness_core'],
                'test': self._test_consciousness_vm_integration
            },
            {
                'name': 'api_consciousness_integration',
                'modules': ['unified_api', 'backend.consciousness_core'],
                'test': self._test_api_consciousness_integration
            },
            {
                'name': 'philosophical_consciousness_integration',
                'modules': ['modules.philosophical_reasoning.consciousness_philosopher', 'consciousness.consciousness_integration'],
                'test': self._test_philosophical_consciousness_integration
            }
        ]
        
        for test_config in integration_tests:
            try:
                # Check if all required modules can be imported
                modules_available = True
                for module_name in test_config['modules']:
                    success, _ = self._try_import(module_name)
                    if not success:
                        modules_available = False
                        break
                
                if modules_available:
                    # Run the integration test
                    test_result = test_config['test']()
                    self.results['integration_tests'].append({
                        'test': test_config['name'],
                        'success': test_result['success'],
                        'error': test_result.get('error'),
                        'details': test_result.get('details')
                    })
                else:
                    self.results['integration_tests'].append({
                        'test': test_config['name'],
                        'success': False,
                        'error': 'Required modules not available',
                        'details': f"Modules: {test_config['modules']}"
                    })
                    
            except Exception as e:
                self.results['integration_tests'].append({
                    'test': test_config['name'],
                    'success': False,
                    'error': str(e),
                    'details': traceback.format_exc()
                })
    
    def _test_configuration_system(self) -> None:
        """Test configuration system integration"""
        logger.info("Testing configuration system...")
        
        try:
            from config_loader import get_config_value
            
            # Test basic config access
            test_value = get_config_value('vm.log_file', 'default.log')
            
            self.results['integration_tests'].append({
                'test': 'configuration_system',
                'success': True,
                'error': None,
                'details': f'Config value retrieved: {test_value}'
            })
            
        except Exception as e:
            self.results['integration_tests'].append({
                'test': 'configuration_system',
                'success': False,
                'error': str(e),
                'details': traceback.format_exc()
            })
    
    def _test_consciousness_vm_integration(self) -> Dict[str, Any]:
        """Test consciousness and VM integration"""
        try:
            from core.prime_vm import ConsciousPrimeVM
            from consciousness.consciousness_core import ConsciousnessCore
            
            # Try to create instances
            vm = ConsciousPrimeVM()
            consciousness = ConsciousnessCore()
            
            return {
                'success': True,
                'details': 'Successfully created VM and consciousness instances'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'details': traceback.format_exc()
            }
    
    def _test_api_consciousness_integration(self) -> Dict[str, Any]:
        """Test API and consciousness integration"""
        try:
            from unified_api import create_api, APIMode
            
            # Try to create consciousness API
            api = create_api(APIMode.CONSCIOUSNESS)
            
            return {
                'success': True,
                'details': 'Successfully created consciousness API'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'details': traceback.format_exc()
            }
    
    def _test_philosophical_consciousness_integration(self) -> Dict[str, Any]:
        """Test philosophical reasoning and consciousness integration"""
        try:
            # Try importing philosophical modules
            success1, _ = self._try_import('modules.philosophical_reasoning.consciousness_philosopher')
            success2, _ = self._try_import('consciousness.consciousness_integration')
            
            if success1 and success2:
                return {
                    'success': True,
                    'details': 'Philosophical and consciousness modules can be imported'
                }
            else:
                return {
                    'success': False,
                    'error': 'One or more modules failed to import',
                    'details': f'consciousness_philosopher: {success1}, consciousness_integration: {success2}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'details': traceback.format_exc()
            }
    
    def _try_import(self, module_name: str) -> Tuple[bool, str]:
        """Try to import a module and return success status"""
        try:
            importlib.import_module(module_name)
            return True, None
        except Exception as e:
            return False, str(e)
    
    def _generate_summary(self) -> None:
        """Generate validation summary"""
        # Count successes and failures
        import_success = sum(1 for test in self.results['import_tests'] if test['success'])
        import_total = len(self.results['import_tests'])
        
        api_success = sum(1 for test in self.results['api_tests'] if test['success'])
        api_total = len(self.results['api_tests'])
        
        integration_success = sum(1 for test in self.results['integration_tests'] if test['success'])
        integration_total = len(self.results['integration_tests'])
        
        total_success = import_success + api_success + integration_success
        total_tests = import_total + api_total + integration_total
        
        self.results['summary'] = {
            'total_tests': total_tests,
            'total_success': total_success,
            'total_failures': total_tests - total_success,
            'success_rate': total_success / total_tests if total_tests > 0 else 0,
            'import_tests': {
                'success': import_success,
                'total': import_total,
                'rate': import_success / import_total if import_total > 0 else 0
            },
            'api_tests': {
                'success': api_success,
                'total': api_total,
                'rate': api_success / api_total if api_total > 0 else 0
            },
            'integration_tests': {
                'success': integration_success,
                'total': integration_total,
                'rate': integration_success / integration_total if integration_total > 0 else 0
            }
        }
    
    def generate_report(self) -> str:
        """Generate a detailed validation report"""
        report = ["Integration Validation Report", "=" * 50, ""]
        
        # Summary
        summary = self.results['summary']
        report.append(f"Overall Success Rate: {summary['success_rate']:.1%}")
        report.append(f"Total Tests: {summary['total_tests']}")
        report.append(f"Successful: {summary['total_success']}")
        report.append(f"Failed: {summary['total_failures']}")
        report.append("")
        
        # Import tests
        report.append("Import Tests:")
        report.append(f"  Success Rate: {summary['import_tests']['rate']:.1%}")
        report.append(f"  Successful: {summary['import_tests']['success']}/{summary['import_tests']['total']}")
        
        # Show failed imports
        failed_imports = [test for test in self.results['import_tests'] if not test['success']]
        if failed_imports:
            report.append("  Failed Imports:")
            for test in failed_imports[:10]:  # Show first 10
                report.append(f"    - {test['module']}: {test['error']}")
            if len(failed_imports) > 10:
                report.append(f"    ... and {len(failed_imports) - 10} more")
        report.append("")
        
        # API tests
        report.append("API Tests:")
        report.append(f"  Success Rate: {summary['api_tests']['rate']:.1%}")
        report.append(f"  Successful: {summary['api_tests']['success']}/{summary['api_tests']['total']}")
        
        # Show failed API tests
        failed_api = [test for test in self.results['api_tests'] if not test['success']]
        if failed_api:
            report.append("  Failed API Tests:")
            for test in failed_api:
                report.append(f"    - {test['test']}: {test['error']}")
        report.append("")
        
        # Integration tests
        report.append("Integration Tests:")
        report.append(f"  Success Rate: {summary['integration_tests']['rate']:.1%}")
        report.append(f"  Successful: {summary['integration_tests']['success']}/{summary['integration_tests']['total']}")
        
        # Show failed integration tests
        failed_integration = [test for test in self.results['integration_tests'] if not test['success']]
        if failed_integration:
            report.append("  Failed Integration Tests:")
            for test in failed_integration:
                report.append(f"    - {test['test']}: {test['error']}")
        report.append("")
        
        # Recommendations
        report.append("Recommendations:")
        if summary['success_rate'] >= 0.9:
            report.append("  ✅ Excellent integration! System is highly coherent.")
        elif summary['success_rate'] >= 0.7:
            report.append("  ✅ Good integration. Minor issues to address.")
        elif summary['success_rate'] >= 0.5:
            report.append("  ⚠️  Moderate integration. Several issues need attention.")
        else:
            report.append("  ❌ Poor integration. Major issues require immediate attention.")
        
        if failed_imports:
            report.append("  - Fix import errors to improve module connectivity")
        if failed_api:
            report.append("  - Address API integration issues")
        if failed_integration:
            report.append("  - Resolve cross-module integration problems")
        
        return "\n".join(report)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate repository integration')
    parser.add_argument('--repo-root', default='.', help='Repository root directory')
    parser.add_argument('--report', default='integration_validation_report.txt', help='Report output file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    validator = IntegrationValidator(args.repo_root)
    results = validator.validate_all()
    
    # Generate and save report
    report = validator.generate_report()
    
    with open(args.report, 'w') as f:
        f.write(report)
    
    print(f"Integration validation complete. Report saved to {args.report}")
    print(f"Success rate: {results['summary']['success_rate']:.1%}")
    
    # Return appropriate exit code
    if results['summary']['success_rate'] >= 0.8:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
