"""Standalone configuration application for document management and indexing.

This is a separate application that runs on port 8081 and should be accessible
only to administrators. It provides document upload, management, and indexing capabilities.

Usage:
    python src/config_app.py
    # Or from project root: python -m src.config_app

The app will start at: http://localhost:8081

For production deployment, use authentication middleware or firewall rules
to restrict access to authorized users only.
"""
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .config_ui import create_config_interface

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


def main():
    """Main function to run the configuration application."""
    # Check if API key is set (needed for indexing)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables.")
        print("   Indexing functionality will not work without an API key.")
        print("   Please create a .env file with your OpenAI API key.")
        print("   Example: OPENAI_API_KEY=sk-...")
        print()

    print("=" * 60)
    print("🔧 FAQ Bot - Configuration Interface")
    print("=" * 60)
    print()
    print("📍 Starting configuration server...")
    print("   URL: http://localhost:8081")
    print()
    print("⚠️  IMPORTANT: This interface should be restricted to")
    print("   administrators only. Use authentication middleware")
    print("   or firewall rules in production.")
    print()
    print("=" * 60)
    print()

    # Create and launch the configuration interface
    demo = create_config_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=8081,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
