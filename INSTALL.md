# Installation Instructions

## One-Line Installation (Recommended)

The easiest way to install Economy Manager V1:

```bash
curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash
```

### What This Does:

1. ✅ Checks for Python 3.8+, Git, and pip3
2. ✅ Clones the repository to `economy-manager-v1/`
3. ✅ Installs all Python dependencies
4. ✅ Runs interactive setup wizard
5. ✅ Prompts to start the bot automatically

### Prerequisites

The installer will check for these automatically:
- **Python 3.8+** 
- **Git**
- **pip3**

If missing, install them first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip git
```

**CentOS/RHEL:**
```bash
sudo yum install python3 python3-pip git
```

## Manual Installation

If you prefer manual installation:

### 1. Clone Repository

```bash
git clone https://github.com/dronzer-tb/economy-manager-v1.git
cd economy-manager-v1
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure Bot

Run the setup wizard:
```bash
python3 scripts/setup.py
```

Or manually create `.env` file:
```bash
cp .env.example .env
nano .env
```

Required configuration:
```env
DB_HOST=172.18.0.1
DB_PORT=3306
DB_USER=coinsengine
DB_PASSWORD=your_password
DB_NAME=coinsengine_shared
DISCORD_TOKEN=your_bot_token
GUILD_ID=your_server_id
TABLE_NAME=coinsengine_users
```

### 4. Start Bot

```bash
python3 bot/main.py
```

## Running in Background

### Using nohup:
```bash
nohup python3 bot/main.py > bot.log 2>&1 &
```

### Using screen:
```bash
screen -S economy-bot
python3 bot/main.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r economy-bot
```

### Using systemd (Linux):

Create `/etc/systemd/system/economy-bot.service`:
```ini
[Unit]
Description=Economy Manager Discord Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/economy-manager-v1
ExecStart=/usr/bin/python3 /path/to/economy-manager-v1/bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable economy-bot
sudo systemctl start economy-bot
sudo systemctl status economy-bot
```

## Database Requirements

This bot is designed for **CoinsEngine** plugin databases.

Required table: `coinsengine_users`

Required columns:
- `name` (MEDIUMTEXT) - Player username
- `uuid` (MEDIUMTEXT) - Player UUID
- `gems` (DOUBLE) - Gem balance
- `coins` (DOUBLE) - Coin balance

If using CoinsEngine, this table already exists!

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Go to "Bot" → Create Bot
4. Copy bot token to `.env` file
5. Enable these intents:
   - Server Members Intent
   - Message Content Intent
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot`, `applications.commands`
8. Select permissions: `Administrator`
9. Copy URL and invite bot to server

## Troubleshooting

### Installation fails
```bash
# Update pip
pip3 install --upgrade pip

# Install dependencies with --user flag
pip3 install -r requirements.txt --user
```

### Bot won't start
```bash
# Check .env file exists
ls -la .env

# Verify database connection
python3 scripts/setup.py

# Check logs
tail -f logs/bot.log
```

### Database connection fails
- Verify MySQL/MariaDB is running
- Check DB_HOST (use `172.18.0.1` for Docker containers)
- Verify credentials are correct
- Test connection: `mysql -h DB_HOST -u DB_USER -p`

### Command not showing in Discord
- Wait 5-10 minutes for Discord to sync
- Try kicking and re-inviting the bot
- Verify bot has `applications.commands` scope
- Check bot has proper permissions in server

## Getting Help

- Check [README.md](README.md) for full documentation
- Review [QUICKSTART.md](QUICKSTART.md) for detailed guide
- Check logs at `logs/bot.log`
- Open issue on GitHub

## Version

Current: **0.2.0** (CoinsEngine Compatible)

---

For more information, see the [README](README.md).
