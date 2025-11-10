#!/bin/bash
# Economy Manager V1 - One-Line Installer
# Version: 0.2.0
# Usage: curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash

set -e

echo "================================"
echo "Economy Manager V1 - Auto Installer"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repository URL
REPO_URL="https://github.com/dronzer-tb/economy-manager-v1.git"
INSTALL_DIR="economy-manager-v1"

echo -e "${GREEN}Step 1/5:${NC} Checking prerequisites..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git is not installed.${NC}"
    echo "Please install git first:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  CentOS/RHEL: sudo yum install git"
    exit 1
fi
echo -e "${GREEN}✅${NC} Git found"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed.${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi
echo -e "${GREEN}✅${NC} Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed.${NC}"
    echo "Please install pip3:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3-pip"
    exit 1
fi
echo -e "${GREEN}✅${NC} pip3 found"

echo ""
echo -e "${GREEN}Step 2/5:${NC} Cloning repository..."

# Remove existing directory if it exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory $INSTALL_DIR already exists.${NC}"
    read -p "Do you want to remove it and reinstall? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}✅${NC} Removed existing directory"
    else
        echo -e "${RED}❌ Installation cancelled.${NC}"
        exit 1
    fi
fi

# Clone repository
git clone "$REPO_URL" "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo -e "${GREEN}✅${NC} Repository cloned successfully"

echo ""
echo -e "${GREEN}Step 3/5:${NC} Installing Python dependencies..."

# Install dependencies
pip3 install -r requirements.txt --user

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅${NC} Dependencies installed successfully"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Step 4/5:${NC} Running setup wizard..."

# Run setup script
python3 scripts/setup.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Setup failed. Please check your configuration and try again.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Step 5/5:${NC} Starting the bot..."
echo ""

# Ask if user wants to start the bot now
read -p "Do you want to start the bot now? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo -e "${GREEN}Starting Economy Manager Bot...${NC}"
    echo "Press Ctrl+C to stop the bot"
    echo ""
    sleep 2
    python3 bot/main.py
else
    echo ""
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}✅ Installation Complete!${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo "To start the bot later, run:"
    echo -e "  ${YELLOW}cd $INSTALL_DIR${NC}"
    echo -e "  ${YELLOW}python3 bot/main.py${NC}"
    echo ""
    echo "To run in background:"
    echo -e "  ${YELLOW}nohup python3 bot/main.py > bot.log 2>&1 &${NC}"
    echo ""
fi
