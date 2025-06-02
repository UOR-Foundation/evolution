#!/usr/bin/env python3
"""
Test script to verify unified API integration
"""

from unified_api import create_api, APIMode, quick_consciousness_demo, quick_vm_demo

def test_api_creation():
    """Test API creation in different modes"""
    print("Testing API creation in different modes...")
    
    modes_tested = 0
    modes_successful = 0
    
    for mode in APIMode:
        try:
            api = create_api(mode)
            print(f"✅ {mode.value} mode: SUCCESS")
            modes_successful += 1
        except Exception as e:
            print(f"❌ {mode.value} mode: FAILED - {str(e)}")
        modes_tested += 1
    
    print(f"\nAPI Creation: {modes_successful}/{modes_tested} modes successful")
    return modes_successful == modes_tested

def test_quick_demos():
    """Test quick demonstration functions"""
    print("\nTesting quick demonstration functions...")
    
    # Test consciousness demo
    try:
        consciousness_results = quick_consciousness_demo()
        print(f"✅ Consciousness demo: SUCCESS")
        print(f"   - Awakening: {consciousness_results.get('awakening', {}).get('success', False)}")
        print(f"   - Reflection: {consciousness_results.get('reflection', {}).get('success', False)}")
        consciousness_success = True
    except Exception as e:
        print(f"❌ Consciousness demo: FAILED - {str(e)}")
        consciousness_success = False
    
    # Test VM demo
    try:
        vm_results = quick_vm_demo()
        print(f"✅ VM demo: SUCCESS")
        print(f"   - Initialization: {vm_results.get('initialization', {}).get('success', False)}")
        vm_success = True
    except Exception as e:
        print(f"❌ VM demo: FAILED - {str(e)}")
        vm_success = False
    
    return consciousness_success and vm_success

def test_api_methods():
    """Test individual API methods"""
    print("\nTesting API methods...")
    
    api = create_api(APIMode.CONSCIOUSNESS)
    
    methods_to_test = [
        ('get_system_state', lambda: api.get_system_state()),
        ('generate_insights', lambda: api.generate_insights()),
        ('awaken_consciousness', lambda: api.awaken_consciousness()),
        ('self_reflect', lambda: api.self_reflect()),
    ]
    
    methods_tested = 0
    methods_successful = 0
    
    for method_name, method_func in methods_to_test:
        try:
            result = method_func()
            if hasattr(result, 'success'):
                if result.success:
                    print(f"✅ {method_name}: SUCCESS")
                    methods_successful += 1
                else:
                    print(f"⚠️  {method_name}: Returned with error - {result.error}")
            else:
                print(f"✅ {method_name}: Executed")
                methods_successful += 1
        except Exception as e:
            print(f"❌ {method_name}: FAILED - {str(e)}")
        methods_tested += 1
    
    print(f"\nAPI Methods: {methods_successful}/{methods_tested} successful")
    return methods_successful > 0

def main():
    """Run all tests"""
    print("=" * 60)
    print("Unified API Integration Test")
    print("=" * 60)
    
    # Run tests
    api_creation_success = test_api_creation()
    quick_demos_success = test_quick_demos()
    api_methods_success = test_api_methods()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"- API Creation: {'PASS' if api_creation_success else 'FAIL'}")
    print(f"- Quick Demos: {'PASS' if quick_demos_success else 'FAIL'}")
    print(f"- API Methods: {'PASS' if api_methods_success else 'FAIL'}")
    
    all_passed = api_creation_success and quick_demos_success and api_methods_success
    
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
