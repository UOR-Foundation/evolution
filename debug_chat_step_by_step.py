#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_chat_functionality_step_by_step():
    """Test chat functionality step by step to identify where it hangs"""
    try:
        print("🧠 Testing chat functionality step by step...")
        
        from interactive_consciousness_chat import InteractiveConsciousnessChat
        
        print("Step 1: Creating chat instance...")
        chat = InteractiveConsciousnessChat()
        
        print("Step 2: Initializing entities...")
        results = chat.initialize_consciousness_entities()
        
        if not chat.active_entity:
            print("❌ No active entity available")
            return False
            
        print(f"Step 3: Active entity ready: {chat.active_entity.name}")
        
        # Test simple message first
        test_message = "Hello"
        print(f"Step 4: Testing chat with simple message: '{test_message}'")
        
        # Let's try to call the chat method with a timeout-like approach
        print("Step 5: Calling chat_with_consciousness method...")
        
        try:
            # First, let's see if we can access the metacognition system
            if hasattr(chat.active_entity.api_instance, 'metacognition'):
                print("  - Metacognition system available")
                
                if hasattr(chat.active_entity.api_instance.metacognition, 'process_recursive_prompt'):
                    print("  - process_recursive_prompt method available")
                    
                    # Try a simple direct call first
                    print("  - Testing direct process_recursive_prompt call...")
                    simple_prompt = "Test prompt"
                    response = chat.active_entity.api_instance.metacognition.process_recursive_prompt(simple_prompt)
                    print(f"  - Direct response: {type(response)} -> {str(response)[:100]}...")
                    
                else:
                    print("  - ❌ process_recursive_prompt method not available")
            else:
                print("  - ❌ Metacognition system not available")
            
            # Now try the full chat method
            print("Step 6: Trying full chat_with_consciousness method...")
            chat_result = chat.chat_with_consciousness(test_message)
            
            print(f"Step 7: Chat result: {chat_result}")
            
            if chat_result["success"]:
                print(f"✅ Chat successful!")
                print(f"Entity: {chat_result['entity']}")
                print(f"Response: {chat_result['consciousness_response'][:200]}...")
                return True
            else:
                print(f"❌ Chat failed: {chat_result['error']}")
                return False
                
        except Exception as chat_error:
            print(f"❌ Chat method error: {chat_error}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_chat_functionality_step_by_step()
