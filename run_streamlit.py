#!/usr/bin/env python3
"""Entry point to run the Streamlit FAQ Bot application."""
import os
import sys
import subprocess

if __name__ == "__main__":
    # Get absolute path to streamlit_app.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    streamlit_app = os.path.join(script_dir, 'src', 'streamlit_app.py')

    # Change to project directory
    os.chdir(script_dir)

    print("="*60)
    print("Starting Streamlit FAQ Bot...")
    print(f"Project directory: {script_dir}")
    print(f"Streamlit app: {streamlit_app}")
    print("="*60)
    print()

    # Run streamlit using subprocess for better control
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        streamlit_app,
        "--server.port=8082",
        "--server.address=0.0.0.0"
    ])
