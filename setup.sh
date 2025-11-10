#!/bin/bash
# Economy Manager V1 - Unified Interactive Installer
# Version: 1.0.0
# Usage: curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/setup.sh | bash

set -e

# ────────────────────────────────────────────────
# Colors
# ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ────────────────────────────────────────────────
# Header
# ────────────────────────────────────────────────
echo -e "${GREEN}"
echo "==============================================="
echo "  Economy Manager V1 - Unified Installer"
echo "==============================================="
echo -e "${NC}"

REPO_URL="https://github.com/dronzer-tb/economy-manager-v1.git"
INSTALL_DIR="economy-manager-v1"

# ────────────────────────────────────────────────
# Step 1: Prerequisite check
# ────────────────────────────────────────────────
echo -e "${GREEN}Step 1/5:${NC} Checking prerequisites..."

for cmd in git python3 pip3; do
  if ! command -v $cmd &> /dev/null; then
    echo -e "${RED}❌ $cmd is not installed.${NC}"
    echo "Please install it and rerun this script."
    exit 1
  fi
  echo -e "${GREEN}✅${NC} $cmd found"
done

# ────────────────────────────────────────────────
# Step 2: Clone or update repo
# ────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Step 2/5:${NC} Preparing repository..."

if [ -d "$INSTALL_DIR" ]; then
  echo -e "${YELLOW}⚠️  Directory '$INSTALL_DIR' already exists.${NC}"
  
  if [ -t 0 ]; then
    # Interactive mode - ask user
    read -p "Do you want to [U]pdate, [R]einstall, or [C]ancel? (u/r/c): " choice
    case "$choice" in
      [Uu]* )
        echo -e "${GREEN}🔄 Updating existing repository...${NC}"
        cd "$INSTALL_DIR" && git pull
        ;;
      [Rr]* )
        echo -e "${YELLOW}🧹 Removing and reinstalling...${NC}"
        rm -rf "$INSTALL_DIR"
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
        ;;
      * )
        echo -e "${RED}❌ Cancelled.${NC}"
        exit 1
        ;;
    esac
  else
    # Non-interactive mode - update by default
    echo -e "${GREEN}🔄 Updating existing repository...${NC}"
    cd "$INSTALL_DIR" && git pull
  fi
else
  git clone "$REPO_URL" "$INSTALL_DIR"
  echo -e "${GREEN}✅${NC} Repository cloned successfully"
  cd "$INSTALL_DIR" || {
    echo -e "${RED}❌ Failed to enter directory $INSTALL_DIR${NC}"
    exit 1
  }
fi

# ────────────────────────────────────────────────
# Step 3: Install Python dependencies
# ────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Step 3/5:${NC} Installing dependencies..."
pip3 install -r requirements.txt --user
echo -e "${GREEN}✅ Dependencies installed successfully${NC}"

# ────────────────────────────────────────────────
# Step 4: Interactive setup
# ────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Step 4/5:${NC} Configuration setup..."
echo ""

# Check if running interactively or via pipe
if [ -t 0 ]; then
  # Interactive mode - run full setup
  echo "Running interactive configuration..."
  
  # Inline Python script for setup.py logic
  python3 << 'PYTHON_SETUP'
import os, sys, mysql.connector
from mysql.connector import Error

def get_input(prompt, default=None):
    if default:
        val = input(f"{prompt} [{default}]: ").strip()
        return val or default
    return input(f"{prompt}: ").strip()

def test_db(cfg):
    print("\n🔍 Testing database connection...")
    try:
        conn = mysql.connector.connect(
            host=cfg['db_host'],
            port=int(cfg['db_port']),
            user=cfg['db_user'],
            password=cfg['db_password'],
            database=cfg['db_name']
        )
        if conn.is_connected():
            print("✅ Database connection successful!")
            cursor = conn.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{cfg['table_name']}'")
            if not cursor.fetchone():
                print(f"⚠️ Table '{cfg['table_name']}' not found. Expected structure:")
                print("""
CREATE TABLE coinsengine_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid MEDIUMTEXT NOT NULL,
    name MEDIUMTEXT NOT NULL,
    gems DOUBLE DEFAULT 0,
    coins DOUBLE DEFAULT 100,
    dateCreated BIGINT NOT NULL,
    last_online BIGINT NOT NULL,
    settings MEDIUMTEXT NOT NULL,
    hiddenFromTops TINYINT(1) NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
""")
            cursor.close()
            conn.close()
            return True
        return False
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return False

def write_env(cfg):
    try:
        with open(".env", "w") as f:
            f.write("# Economy Manager Configuration\n")
            for k, v in cfg.items():
                f.write(f"{k.upper()}={v}\n")
        print("✅ Configuration saved to .env")
    except Exception as e:
        print(f"❌ Failed to write .env: {e}")
        sys.exit(1)

def main():
    print("="*50)
    print("📊 Database Configuration")
    print("="*50)
    cfg = {}
    cfg['db_host'] = get_input("Database Host", "localhost")
    cfg['db_port'] = get_input("Database Port", "3306")
    cfg['db_user'] = get_input("Database User")
    cfg['db_password'] = get_input("Database Password")
    cfg['db_name'] = get_input("Database Name", "coinsengine_shared")
    cfg['table_name'] = get_input("Table Name", "coinsengine_users")

    if not test_db(cfg):
        print("❌ Cannot continue due to database error.")
        sys.exit(1)

    print("\n🤖 Discord Configuration")
    print("="*50)
    cfg['discord_token'] = get_input("Discord Bot Token")
    cfg['guild_id'] = get_input("Guild ID (optional)")
    cfg['admin_role_id'] = get_input("Admin Role ID (optional)")
    write_env(cfg)
    print("\n✅ Setup complete. You can now start the bot.")
    
main()
PYTHON_SETUP

else
  # Non-interactive mode (piped from curl) - create example config
  echo -e "${YELLOW}⚠️  Running in non-interactive mode${NC}"
  echo "Creating example configuration file..."
  
  if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env from template${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  IMPORTANT: You must edit .env with your configuration before running the bot!${NC}"
    echo ""
    echo "Required steps:"
    echo "  1. Edit .env file: nano .env"
    echo "  2. Fill in your database credentials"
    echo "  3. Add your Discord bot token"
    echo "  4. Start the bot: python3 bot/main.py"
  else
    echo -e "${YELLOW}⚠️  .env already exists, skipping...${NC}"
  fi
fi

# ────────────────────────────────────────────────
# Step 5: Start the bot
# ────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Step 5/5:${NC} Completion"
echo ""

if [ -t 0 ]; then
  # Interactive mode - ask to start bot
  read -p "Do you want to start the bot now? (Y/n): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo -e "${GREEN}Starting bot...${NC}"
    python3 bot/main.py
  else
    echo -e "${GREEN}✅ Installation complete!${NC}"
    echo ""
    echo "To start the bot:"
    echo "  cd $INSTALL_DIR"
    echo "  python3 bot/main.py"
    echo ""
    echo "Or run in background:"
    echo "  nohup python3 bot/main.py > bot.log 2>&1 &"
  fi
else
  # Non-interactive mode - show instructions
  echo -e "${GREEN}✅ Installation complete!${NC}"
  echo ""
  echo -e "${YELLOW}Next steps:${NC}"
  echo "  1. cd $INSTALL_DIR"
  echo "  2. nano .env  # Configure your database and Discord token"
  echo "  3. python3 bot/main.py  # Start the bot"
  echo ""
  echo "To run in background:"
  echo "  nohup python3 bot/main.py > bot.log 2>&1 &"
fi
