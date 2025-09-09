#!/usr/bin/env python3
"""
Test script for AI Chat Offline project.
This script performs basic functionality tests without requiring model download.
"""

import sys
import os
from typing import List, Tuple

def test_imports() -> bool:
    """Test if all required modules can be imported."""
    try:
        import torch
        import transformers
        from bot import ChatbotConfig, Chatbot
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config_creation() -> bool:
    """Test ChatbotConfig creation."""
    try:
        from bot import ChatbotConfig
        config = ChatbotConfig()
        assert hasattr(config, 'model_name')
        assert hasattr(config, 'max_length')
        assert hasattr(config, 'temperature')
        print("✅ ChatbotConfig creation successful")
        return True
    except Exception as e:
        print(f"❌ Config creation error: {e}")
        return False

def test_chatbot_instantiation() -> bool:
    """Test Chatbot instantiation."""
    try:
        from bot import ChatbotConfig, Chatbot
        config = ChatbotConfig()
        chatbot = Chatbot(config)
        assert hasattr(chatbot, 'config')
        assert hasattr(chatbot, 'tokenizer')
        assert hasattr(chatbot, 'model')
        print("✅ Chatbot instantiation successful")
        return True
    except Exception as e:
        print(f"❌ Chatbot instantiation error: {e}")
        return False

def test_input_validation() -> bool:
    """Test input validation functionality."""
    try:
        from bot import ChatbotConfig, Chatbot
        config = ChatbotConfig()
        chatbot = Chatbot(config)
        
        # Test valid input
        assert chatbot.validate_input("Hello world") == True
        # Test empty input
        assert chatbot.validate_input("") == False
        assert chatbot.validate_input("   ") == False
        # Test None input
        assert chatbot.validate_input(None) == False
        
        print("✅ Input validation tests passed")
        return True
    except Exception as e:
        print(f"❌ Input validation error: {e}")
        return False

def test_syntax() -> bool:
    """Test Python syntax compilation."""
    try:
        import py_compile
        py_compile.compile('bot.py', doraise=True)
        print("✅ Syntax check passed")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Syntax error: {e}")
        return False

def run_tests() -> Tuple[bool, List[str]]:
    """Run all tests and return results."""
    tests = [
        ("Syntax Check", test_syntax),
        ("Import Test", test_imports),
        ("Config Creation", test_config_creation),
        ("Chatbot Instantiation", test_chatbot_instantiation),
        ("Input Validation", test_input_validation),
    ]
    
    results = []
    passed = 0
    total = len(tests)
    
    print("🧪 Running AI Chat Offline Tests")
    print("=" * 40)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                passed += 1
                results.append(f"✅ {test_name}")
            else:
                results.append(f"❌ {test_name}")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append(f"❌ {test_name} (Exception)")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    for result in results:
        print(result)
    
    if passed == total:
        print("\n🎉 All tests passed! The chatbot is ready to use.")
        print("💡 Run './run_chatbot.sh' or 'python3 bot.py' to start chatting!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
    
    return passed == total, results

if __name__ == "__main__":
    success, _ = run_tests()
    sys.exit(0 if success else 1)
