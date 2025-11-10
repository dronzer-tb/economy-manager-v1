# Economy Manager V1

![Version](https://img.shields.io/badge/version-0.2.3-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## Overview

**Economy Manager V1** is a Discord bot designed for Minecraft server administrators to manage player economies (gems and coins) through an intuitive button-based interface. No command syntax required—all interactions are driven by interactive buttons and dropdowns.

**Compatible with CoinsEngine plugin databases!**

## Features

- 🎮 **Player Selection**: Searchable dropdown menu with all players from your MySQL database
- 💎 **View Balances**: Display player's current gems and coins (supports decimal values)
- ➕ **Add Currency**: Easily add gems or coins to player accounts
- ➖ **Remove Currency**: Remove gems or coins with balance validation
- 🖱️ **Button Interface**: All actions accessible via buttons (no slash commands needed)
- 🔒 **Secure**: Role-based access control and SQL injection prevention
- 📊 **Transaction Logging**: Complete audit trail of all economy changes
- � **Discord Logging**: Optional dedicated channel for all bot actions
- �🔄 **CoinsEngine Compatible**: Works directly with CoinsEngine shared database

## Quick Install (New Two-Step Method)

```bash
curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install.sh | bash
```

This will:
1. ✅ Download the bot files
2. ✅ Install Python dependencies
3. ✅ Run interactive configuration wizard
4. ✅ Start the bot

**Why two-step?** The bootstrap script downloads files first, then runs an interactive setup so you can properly configure the database and Discord settings.

> ℹ️ When executed via `curl | bash`, the bootstrap script automatically reconnects to your terminal so the wizard can prompt for input safely. If a terminal is not available, it will instruct you to run `./setup-interactive.sh` manually.

## Manual Installation

```bash
# Clone the repository
git clone https://github.com/dronzer-tb/economy-manager-v1.git
cd economy-manager-v1

# Install dependencies
pip3 install -r requirements.txt

# Run interactive setup
./setup-interactive.sh
```

## Configuration

Configuration is stored in `.env` file:

```env
# Database Configuration
DB_HOST=localhost
### Configuration (.env file)

The interactive setup wizard will create a `.env` file with these settings:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=coinsengine_shared

# Discord Configuration
DISCORD_TOKEN=your_bot_token
GUILD_ID=your_server_id

# Optional Configuration
TABLE_NAME=coinsengine_users
ADMIN_ROLE_ID=your_admin_role_id
LOG_CHANNEL_ID=your_log_channel_id  # Optional: Channel for action logs

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

### Running the Bot

After configuration, start the bot:

```bash
python3 bot/main.py
```

Or run in background:

```bash
nohup python3 bot/main.py > logs/bot.log 2>&1 &
```

## Discord Logging Channel (Optional)

The bot can send action logs to a dedicated Discord channel:

1. Create a channel in your Discord server (e.g., `#economy-logs`)
2. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
3. Right-click the channel → Copy ID
4. Add the channel ID to your `.env` file:
   ```bash
   LOG_CHANNEL_ID=1234567890123456789
   ```

**What gets logged:**
- ✅ Bot startup/shutdown
- 💎 Gem additions/removals
- 🪙 Coin additions/removals
- 👤 Admin who performed the action
- ⏰ Timestamp of each transaction

## Database Schema

This bot is designed to work with the **CoinsEngine** plugin database structure:

```sql
CREATE TABLE coinsengine_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid MEDIUMTEXT NOT NULL,
    name MEDIUMTEXT NOT NULL,
    dateCreated BIGINT NOT NULL,
    last_online BIGINT NOT NULL,
    settings MEDIUMTEXT NOT NULL,
    hiddenFromTops TINYINT(1) NOT NULL,
    gems DOUBLE DEFAULT 0,
    coins DOUBLE DEFAULT 100,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

The bot uses the following columns:
- `name` - Player's username
- `uuid` - Player's UUID
- `gems` - Gem balance (DOUBLE, supports decimals)
- `coins` - Coin balance (DOUBLE, supports decimals)

## Usage

1. **Invoke the bot** in your Discord server
2. **Select "Manage Player"** from the main menu
3. **Choose a player** from the dropdown
4. **View their balance** (gems and coins displayed)
5. **Take action**: Add/Remove Gems or Coins
6. **Confirm transaction** and see the updated balance

## Project Structure

```
economy-manager/
├── bot/                    # Bot source code
│   ├── main.py            # Entry point
│   ├── cogs/              # Command modules
│   ├── database/          # Database layer
│   ├── ui/                # Discord UI components
│   └── utils/             # Utilities
├── docs/                  # Documentation
│   └── PRD.md            # Product Requirements
├── logs/                  # Agent activity logs
│   └── agent_log.md      # Development log
├── scripts/               # Installation/setup scripts
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── CHANGELOG.md          # Version history
├── VERSION               # Current version
└── README.md            # This file
```

## Development

This project follows strict development protocols:
- **Semantic Versioning**: All changes are versioned (MAJOR.MINOR.PATCH)
- **Agent Logging**: Complete activity log in `logs/agent_log.md`
- **Testing**: All features must pass tests before version increments
- **Documentation**: PRD and CHANGELOG maintained for all changes

See `prompts.txt` for complete development guidelines.

## Security

- ✅ Role-based access control
- ✅ SQL injection prevention (parameterized queries)
- ✅ Secure credential storage (.env)
- ✅ Transaction logging and audit trail
- ✅ Input validation

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the [PRD](docs/PRD.md) for detailed requirements
- Review [CHANGELOG](CHANGELOG.md) for recent updates

## License

MIT License - See LICENSE file for details

## Version

Current Version: **0.2.0** (CoinsEngine Compatible)

See [CHANGELOG.md](CHANGELOG.md) for version history.

## What's New in 0.2.0

- ✅ **CoinsEngine Database Support**: Now compatible with CoinsEngine plugin databases
- ✅ **Decimal Currency Support**: Supports decimal values for gems and coins
- ✅ **One-Line Installer**: Easy installation with automated setup
- ✅ **Improved Table Detection**: Automatically validates database schema
- ✅ **UUID Display**: Shows player UUIDs in the management interface

---

**Status**: ✅ Production Ready - CoinsEngine Compatible
