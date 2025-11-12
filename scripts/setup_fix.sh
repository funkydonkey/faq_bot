#!/bin/bash
# Fix FAQ Bot Python Environment
# This script recreates the virtual environment with Python 3.12

echo "=== FAQ Bot Environment Setup Fix ==="
echo ""
echo "Current issue: Using Python 3.13, but project requires Python 3.12"
echo "This will:"
echo "  1. Deactivate current venv (if active)"
echo "  2. Remove old venv directory"
echo "  3. Create new venv with Python 3.12"
echo "  4. Install all dependencies"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Step 1: Deactivate if active (this is a no-op if not active)
echo "Step 1: Deactivating current environment..."
deactivate 2>/dev/null || true

# Step 2: Remove old venv
echo "Step 2: Removing old venv directory..."
rm -rf venv

# Step 3: Create new venv with Python 3.12
echo "Step 3: Creating new virtual environment with Python 3.12..."
python3.12 -m venv venv

# Step 4: Activate new venv
echo "Step 4: Activating new environment..."
source venv/bin/activate

# Step 5: Upgrade pip
echo "Step 5: Upgrading pip..."
pip install --upgrade pip

# Step 6: Install dependencies
echo "Step 6: Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To activate this environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "Your Python version is now:"
python --version
