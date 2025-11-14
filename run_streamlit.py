#!/usr/bin/env python3
"""Entry point to run the Streamlit FAQ Bot multi-page application."""
import os
import sys
import subprocess

if __name__ == "__main__":
    # Get absolute path to Home.py (main entry point)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    home_page = os.path.join(script_dir, 'Home.py')

    # Change to project directory
    os.chdir(script_dir)

    print("="*60)
    print("Starting Streamlit FAQ Bot Multi-Page App...")
    print(f"Project directory: {script_dir}")
    print(f"Home page: {home_page}")
    print("Pages:")
    print("  - 💬 Chat (pages/1_💬_Chat.py)")
    print("  - 🕸️ Knowledge Graph (pages/2_🕸️_Knowledge_Graph.py)")
    print("="*60)
    print()

    # Run streamlit using subprocess for better control
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        home_page,
        "--server.port=8082",
        "--server.address=0.0.0.0"
    ])
