#!/bin/bash
# Economy Manager V1 - Interactive Setup Script
# Version: 1.0.0
# This script runs AFTER the repository has been cloned

set -e

# ────────────────────────────────────────────────
# Colors
# ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Ensure we are running in an interactive terminal
if [ ! -t 0 ]; then
    echo -e "${RED}ERROR:${NC} This setup wizard requires an interactive terminal with user input."
    echo "Please run: ./setup-interactive.sh" >&2
    exit 1
fi

# ────────────────────────────────────────────────
# Welcome Message
# ────────────────────────────────────────────────
echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║      Interactive Configuration Wizard       ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ────────────────────────────────────────────────
# Step 1: Install Python dependencies
# ────────────────────────────────────────────────
echo -e "${BLUE}[Step 1/4]${NC} Installing Python dependencies..."
echo ""

if pip3 install -r requirements.txt --user; then
  echo ""
  echo -e "${GREEN}  ✓ Dependencies installed successfully${NC}"
else
  echo ""
  echo -e "${RED}  ✗ Failed to install dependencies${NC}"
  exit 1
fi

# ────────────────────────────────────────────────
# Step 2: Interactive configuration with bash
# ────────────────────────────────────────────────
echo ""
echo -e "${BLUE}[Step 2/4]${NC} Database Configuration"
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

# Database configuration using bash read
echo "📊 Database Settings"
echo "--------------------------------------------------"

read -p "Database Host [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "Database Port [3306]: " DB_PORT
DB_PORT=${DB_PORT:-3306}

read -p "Database Username: " DB_USER

read -sp "Database Password: " DB_PASSWORD
echo ""

read -p "Database Name [coinsengine_shared]: " DB_NAME
DB_NAME=${DB_NAME:-coinsengine_shared}

read -p "Table Name [coinsengine_users]: " TABLE_NAME
TABLE_NAME=${TABLE_NAME:-coinsengine_users}

# Test database connection with Python
echo ""
echo "🔍 Testing database connection..."
python3 << PYTHON_TEST
import sys
import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host='$DB_HOST',
        port=int('$DB_PORT'),
        user='$DB_USER',
        password='$DB_PASSWORD',
        database='$DB_NAME'
    )
    
    if conn.is_connected():
        print("✅ Database connection successful!")
        
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE '$TABLE_NAME'")
        
        if cursor.fetchone():
            print(f"✅ Table '$TABLE_NAME' found")
        else:
            print(f"⚠️  Table '$TABLE_NAME' not found")
            print("\nExpected table structure:")
            print("  - name (MEDIUMTEXT)")
            print("  - uuid (MEDIUMTEXT)")
            print("  - gems (DOUBLE)")
            print("  - coins (DOUBLE)")
            
        cursor.close()
        conn.close()
        sys.exit(0)
    else:
        print("❌ Connection failed")
        sys.exit(1)
        
except Error as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
PYTHON_TEST

if [ $? -ne 0 ]; then
  echo ""
  read -p "⚠️  Database test failed. Continue anyway? (y/N): " CONTINUE
  if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
    echo "❌ Setup cancelled"
    exit 1
  fi
fi

# Discord configuration
echo ""
echo "🤖 Discord Settings"
echo "--------------------------------------------------"

read -p "Discord Bot Token: " DISCORD_TOKEN

read -p "Guild ID (Server ID) [optional]: " GUILD_ID

# Optional configuration
echo ""
echo "⚙️  Optional Settings"
echo "--------------------------------------------------"

read -p "Admin Role ID [optional]: " ADMIN_ROLE_ID

read -p "Log Channel ID [optional]: " LOG_CHANNEL_ID

# Write .env file using Python
echo ""
echo "💾 Writing configuration..."
python3 << PYTHON_WRITE
import os
import sys

try:
    with open(".env", "w") as f:
        f.write("# Economy Manager Configuration\n")
        f.write("# Generated by setup wizard\n\n")
        
        f.write("# Database Configuration\n")
        f.write(f"DB_HOST=$DB_HOST\n")
        f.write(f"DB_PORT=$DB_PORT\n")
        f.write(f"DB_USER=$DB_USER\n")
        f.write(f"DB_PASSWORD=$DB_PASSWORD\n")
        f.write(f"DB_NAME=$DB_NAME\n\n")
        
        f.write("# Discord Configuration\n")
        f.write(f"DISCORD_TOKEN=$DISCORD_TOKEN\n")
        if "$GUILD_ID":
            f.write(f"GUILD_ID=$GUILD_ID\n")
        f.write("\n")
        
        f.write("# Optional Configuration\n")
        f.write(f"TABLE_NAME=$TABLE_NAME\n")
        if "$ADMIN_ROLE_ID":
            f.write(f"ADMIN_ROLE_ID=$ADMIN_ROLE_ID\n")
        if "$LOG_CHANNEL_ID":
            f.write(f"LOG_CHANNEL_ID=$LOG_CHANNEL_ID\n")
        f.write("\n")
        
        f.write("# Logging\n")
        f.write("LOG_LEVEL=INFO\n")
        f.write("LOG_FILE=logs/bot.log\n")
        
    print("✅ Configuration saved to .env")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Failed to write .env file: {e}")
    sys.exit(1)
PYTHON_WRITE

if [ $? -ne 0 ]; then
  echo "❌ Configuration failed"
  exit 1
fi

echo ""
echo "=================================================="
echo "✅ Configuration complete!"
echo "=================================================="

# ────────────────────────────────────────────────
# Step 3: Create logs directory
# ────────────────────────────────────────────────
echo ""
echo -e "${BLUE}[Step 3/4]${NC} Setting up directories..."

mkdir -p logs
echo -e "${GREEN}  ✓ Logs directory created${NC}"

# ────────────────────────────────────────────────
# Step 4: Final instructions
# ────────────────────────────────────────────────
echo ""
echo -e "${BLUE}[Step 4/4]${NC} Ready to start!"
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}Configuration complete!${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo ""
echo "To start the bot:"
echo -e "  ${YELLOW}python3 bot/main.py${NC}"
echo ""
echo "To run in background:"
echo -e "  ${YELLOW}nohup python3 bot/main.py > logs/bot.log 2>&1 &${NC}"
echo ""
echo "To view logs:"
echo -e "  ${YELLOW}tail -f logs/bot.log${NC}"
echo ""

# Ask to start bot
read -p "Do you want to start the bot now? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
  echo ""
  echo -e "${GREEN}Starting Economy Manager Bot...${NC}"
  echo ""
  python3 bot/main.py
fi
