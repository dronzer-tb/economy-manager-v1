# Economy Manager V1

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## Overview

**Economy Manager V1** is a Discord bot designed for Minecraft server administrators to manage player economies (gems and coins) through an intuitive button-based interface. No command syntax required—all interactions are driven by interactive buttons and dropdowns.

## Features

- 🎮 **Player Selection**: Searchable dropdown menu with all players from your MySQL database
- 💎 **View Balances**: Display player's current gems and coins
- ➕ **Add Currency**: Easily add gems or coins to player accounts
- ➖ **Remove Currency**: Remove gems or coins with balance validation
- 🖱️ **Button Interface**: All actions accessible via buttons (no slash commands needed)
- 🔒 **Secure**: Role-based access control and SQL injection prevention
- 📊 **Transaction Logging**: Complete audit trail of all economy changes

## Requirements

- Python 3.8 or higher
- MySQL database
- Discord Bot Token
- Discord Server with admin permissions

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/economy-manager.git
cd economy-manager

# Run the installation script
./install.sh  # Linux/macOS
# or
install.bat   # Windows
```

### Setup

```bash
# Run the setup script
python setup.py
```

The setup script will prompt you for:
- MySQL database credentials (host, port, username, password)
- Database name
- Discord bot token
- Server ID/Guild ID

### Running the Bot

```bash
python bot/main.py
```

## Configuration

Configuration is stored in `.env` file:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=minecraft_economy

# Discord Configuration
DISCORD_TOKEN=your_bot_token
GUILD_ID=your_server_id

# Optional Configuration
TABLE_NAME=players
ADMIN_ROLE_ID=your_admin_role_id
```

## Database Schema

Your MySQL database should have a table with the following structure:

```sql
CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    uuid VARCHAR(36),
    gems INT DEFAULT 0,
    coins INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

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

Current Version: **0.1.0** (Initial Setup)

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Status**: 🚧 In Development - Initial setup phase
