#!/bin/bash
# Economy Manager V1 - Bootstrap Installer
# Version: 1.0.0
# Usage: curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install.sh | bash

set -e

# ────────────────────────────────────────────────
# Colors
# ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────
clear
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════╗"
echo "║   Economy Manager V1 - Bootstrap Installer   ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

REPO_URL="https://github.com/dronzer-tb/economy-manager-v1.git"
INSTALL_DIR="economy-manager-v1"

# ────────────────────────────────────────────────
# Step 1: Prerequisite check
# ────────────────────────────────────────────────
echo -e "${BLUE}[1/3]${NC} Checking prerequisites..."

MISSING_DEPS=()

for cmd in git python3 pip3; do
  if ! command -v $cmd &> /dev/null; then
    MISSING_DEPS+=($cmd)
    echo -e "${RED}  ✗ $cmd not found${NC}"
  else
    echo -e "${GREEN}  ✓ $cmd found${NC}"
  fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
  echo ""
  echo -e "${RED}ERROR: Missing required dependencies${NC}"
  echo "Please install the following and try again:"
  for dep in "${MISSING_DEPS[@]}"; do
    echo "  - $dep"
  done
  exit 1
fi

# ────────────────────────────────────────────────
# Step 2: Clone or update repository
# ────────────────────────────────────────────────
echo ""
echo -e "${BLUE}[2/3]${NC} Downloading Economy Manager..."

if [ -d "$INSTALL_DIR" ]; then
  echo -e "${YELLOW}  ! Directory '$INSTALL_DIR' already exists${NC}"
  echo -e "${YELLOW}  ! Updating repository...${NC}"
  cd "$INSTALL_DIR"
  git pull origin main
else
  git clone "$REPO_URL" "$INSTALL_DIR"
  echo -e "${GREEN}  ✓ Repository cloned successfully${NC}"
  cd "$INSTALL_DIR" || {
    echo -e "${RED}ERROR: Failed to enter directory $INSTALL_DIR${NC}"
    exit 1
  }
fi

# ────────────────────────────────────────────────
# Step 3: Run interactive installer
# ────────────────────────────────────────────────
echo ""
echo -e "${BLUE}[3/3]${NC} Launching interactive setup..."
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo ""

# Make interactive installer executable
chmod +x setup-interactive.sh

# Reattach to controlling terminal if script is running non-interactively
if [ ! -t 0 ]; then
  if [ -r /dev/tty ]; then
    echo -e "${YELLOW}⚠️  Detected non-interactive execution (e.g., curl pipe). Switching to direct terminal for prompts...${NC}" > /dev/tty
    exec </dev/tty
    exec >/dev/tty
    exec 2>/dev/tty
  else
    echo -e "${RED}ERROR:${NC} Unable to acquire an interactive terminal."
    echo "Please run the following command manually after this script finishes:"
    echo "  cd $INSTALL_DIR && ./setup-interactive.sh"
    exit 1
  fi
fi

# Run the interactive installer
./setup-interactive.sh

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Installation Complete! 🎉           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
