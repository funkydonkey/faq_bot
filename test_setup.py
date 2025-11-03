"""Test script to verify the installation and setup."""
import sys
import os


def check_imports():
    """Check if all required packages are installed."""
    print("Checking required packages...")
    packages = {
        'gradio': 'gradio',
        'openai': 'openai',
        'docx': 'python-docx',
        'autogen': 'pyautogen',
        'dotenv': 'python-dotenv'
    }

    missing = []
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED")
            missing.append(package)

    return missing


def check_env():
    """Check if .env file exists and has API key."""
    print("\nChecking environment setup...")

    if not os.path.exists('.env'):
        print("✗ .env file not found")
        print("  Please create a .env file with your OPENAI_API_KEY")
        return False

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OPENAI_API_KEY not set in .env file")
        return False

    if api_key.startswith('sk-'):
        print("✓ OPENAI_API_KEY is set")
        return True
    else:
        print("✗ OPENAI_API_KEY format looks incorrect")
        return False


def main():
    """Run all checks."""
    print("=" * 50)
    print("FAQ Bot Setup Test")
    print("=" * 50)

    # Check imports
    missing = check_imports()

    # Check environment
    env_ok = check_env()

    # Summary
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)

    if missing:
        print(f"\n✗ Missing packages: {', '.join(missing)}")
        print("  Run: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\n✓ All packages installed")

    if not env_ok:
        print("✗ Environment setup incomplete")
        print("  Please configure your .env file with OPENAI_API_KEY")
        sys.exit(1)
    else:
        print("✓ Environment configured")

    print("\n🎉 Setup complete! You can now run: python app.py")
    sys.exit(0)


if __name__ == "__main__":
    main()
