#!/bin/bash
# Installation Script for Economy Manager V1
# Version: 0.1.0

echo "================================"
echo "Economy Manager V1 - Installation"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "================================"
echo "✅ Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env: cp .env.example .env"
echo "2. Edit .env with your configuration"
echo "3. Run setup: python3 scripts/setup.py"
echo "4. Start the bot: python3 bot/main.py"
echo ""
