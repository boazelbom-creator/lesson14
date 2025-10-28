#!/usr/bin/env bash
# Setup script for Multi-Agent Translation System

set -e  # Exit on error

echo "==========================================="
echo "Multi-Agent Translation System - Setup"
echo "==========================================="
echo

# Check Python version
echo "[1/5] Checking Python version..."
python3 --version || { echo "Error: Python 3 is not installed"; exit 1; }
echo "✓ Python 3 found"
echo

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo

# Install dependencies
echo "[4/5] Installing dependencies..."
echo "This may take several minutes (downloading ~3GB of packages)..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo

# Setup environment file
echo "[5/5] Setting up environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo
    echo "IMPORTANT: Please edit .env and add your Anthropic API key!"
    echo "Get your API key from: https://console.anthropic.com/"
else
    echo "✓ .env file already exists"
fi
echo

echo "==========================================="
echo "Setup Complete!"
echo "==========================================="
echo
echo "Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Add your API key to .env file"
echo "  3. Run the system: python main.py --sentences 20"
echo
echo "For help: python main.py --help"
echo "==========================================="
