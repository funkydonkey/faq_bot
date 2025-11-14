#!/usr/bin/env python3
"""Test script to verify Streamlit app imports work correctly."""
import sys
import os

# Add paths like streamlit_app.py does
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, current_dir)

print("Testing Streamlit app imports...")
print(f"Current dir: {current_dir}")
print(f"Src dir: {src_dir}")
print(f"sys.path: {sys.path[:3]}")
print()

try:
    print("1. Testing OpenAIAgentRunner import...")
    from src.openai_agent import OpenAIAgentRunner
    print("   ✅ OpenAIAgentRunner imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

try:
    print("2. Testing Streamlit import...")
    import streamlit as st
    print("   ✅ Streamlit imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

try:
    print("3. Testing pathlib...")
    from pathlib import Path
    print("   ✅ pathlib imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()
print("✅ All imports successful! Streamlit app should work.")
print()
print("To run the app:")
print("  python run_streamlit.py")
print("  OR")
print("  streamlit run src/streamlit_app.py --server.port=8082")
