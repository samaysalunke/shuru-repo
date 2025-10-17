"""
Quick test script to validate the new dashboard structure
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import streamlit: {e}")
        return False
    
    try:
        from ui_components import (
            inject_dashboard_styles,
            display_metric_card,
            display_case_study_item,
            display_panel_header,
            display_status_badge,
            display_dashboard_header
        )
        print("✓ UI components imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ui_components: {e}")
        return False
    
    try:
        from app import ShuruTechRAGBot
        print("✓ ShuruTechRAGBot imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ShuruTechRAGBot: {e}")
        return False
    
    return True


def test_knowledge_base():
    """Test that knowledge base exists and has valid structure"""
    print("\nTesting knowledge base...")
    
    if not os.path.exists('knowledge_base.json'):
        print("✗ knowledge_base.json not found")
        return False
    
    try:
        import json
        with open('knowledge_base.json', 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        if 'case_studies' not in kb:
            print("✗ No 'case_studies' key in knowledge base")
            return False
        
        num_case_studies = len(kb.get('case_studies', []))
        print(f"✓ Knowledge base loaded: {num_case_studies} case studies found")
        return True
    except Exception as e:
        print(f"✗ Failed to load knowledge base: {e}")
        return False


def test_env_config():
    """Test that environment configuration is set up"""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("⚠ .env file not found (optional)")
        return True
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            print(f"✓ ANTHROPIC_API_KEY configured (length: {len(api_key)})")
        else:
            print("⚠ ANTHROPIC_API_KEY not set in .env")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load .env: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("DASHBOARD STRUCTURE VALIDATION")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_knowledge_base,
        test_env_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✅ All tests passed! Dashboard structure is valid.")
        print("\nTo run the application:")
        print("  streamlit run app.py")
        return 0
    else:
        print("\n⚠ Some tests failed. Please fix the issues before running.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

