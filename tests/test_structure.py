#!/usr/bin/env python3
"""Test script to verify the new project structure."""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_structure():
    """Test that all expected files and directories exist."""
    print("=" * 60)
    print("Testing FAQ Bot Project Structure")
    print("=" * 60)
    print()

    # Define expected structure
    tests = [
        ("Entry point: run_app.py", "run_app.py"),
        ("Entry point: run_config.py", "run_config.py"),
        ("Source directory", "src/"),
        ("Source: app.py", "src/app.py"),
        ("Source: config_app.py", "src/config_app.py"),
        ("Source: config_ui.py", "src/config_ui.py"),
        ("Source: openai_agent.py", "src/openai_agent.py"),
        ("Source: clarification_agent.py", "src/clarification_agent.py"),
        ("Source: autogen_agent.py", "src/autogen_agent.py"),
        ("Source: docx_reader.py", "src/docx_reader.py"),
        ("Source: indexing.py", "src/indexing.py"),
        ("Source: __init__.py", "src/__init__.py"),
        ("Scripts directory", "scripts/"),
        ("Script: demo_indexing.py", "scripts/demo_indexing.py"),
        ("Script: graph.py", "scripts/graph.py"),
        ("Script: start_both.sh", "scripts/start_both.sh"),
        ("Tests directory", "tests/"),
        ("Test: test.py", "tests/test.py"),
        ("Test: test_hybrid.py", "tests/test_hybrid.py"),
        ("Test: test_threshold.py", "tests/test_threshold.py"),
        ("Docs directory", "docs/"),
        ("Documentation: README.md", "README.md"),
        ("Documentation: CLAUDE.md", "CLAUDE.md"),
    ]

    passed = 0
    failed = 0

    for description, path in tests:
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            print(f"✅ {description}")
            passed += 1
        else:
            print(f"❌ {description} - NOT FOUND: {path}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("✅ All structural tests passed!")
        return True
    else:
        print(f"❌ {failed} test(s) failed")
        return False

if __name__ == "__main__":
    success = test_structure()
    sys.exit(0 if success else 1)
