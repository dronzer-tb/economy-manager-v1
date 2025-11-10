# Economy Manager Bot# Economy Manager V1



![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)![Version](https://img.shields.io/badge/version-0.2.3-blue.svg)

![Python](https://img.shields.io/badge/python-3.8+-green.svg)![Python](https://img.shields.io/badge/python-3.8+-green.svg)

![Discord.py](https://img.shields.io/badge/discord.py-2.0+-purple.svg)![License](https://img.shields.io/badge/license-MIT-orange.svg)

![License](https://img.shields.io/badge/license-MIT-orange.svg)

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)## Overview



## 🎮 Overview**Economy Manager V1** is a Discord bot designed for Minecraft server administrators to manage player economies (gems and coins) through an intuitive button-based interface. No command syntax required—all interactions are driven by interactive buttons and dropdowns.



**Economy Manager Bot** is a powerful Discord bot for Minecraft server administrators to manage player economies through an intuitive Discord interface. Designed for **CoinsEngine** plugin databases, it provides a seamless way to manage gems and coins with modern UI components.**Compatible with CoinsEngine plugin databases!**



### ✨ Key Features## Features



- 🎯 **Smart Player Search**: Fuzzy search finds players even with typos- 🎮 **Player Selection**: Searchable dropdown menu with all players from your MySQL database

- 📄 **Pagination**: Navigate through unlimited players (25 per page)- 💎 **View Balances**: Display player's current gems and coins (supports decimal values)

- 💎 **Dual Currency**: Manage both gems and coins (decimal support)- ➕ **Add Currency**: Easily add gems or coins to player accounts

- 🔘 **Button Interface**: No commands to remember—everything is clickable- ➖ **Remove Currency**: Remove gems or coins with balance validation

- 🔄 **Real-time Updates**: Refresh button shows latest balances- 🖱️ **Button Interface**: All actions accessible via buttons (no slash commands needed)

- 📊 **Transaction Logging**: Complete audit trail in Discord channel- 🔒 **Secure**: Role-based access control and SQL injection prevention

- 🔒 **Role-Based Security**: Only authorized users can manage economy- 📊 **Transaction Logging**: Complete audit trail of all economy changes

- ⚡ **Fast Setup**: One-line installation command- � **Discord Logging**: Optional dedicated channel for all bot actions

- 🎨 **Beautiful UI**: Rich embeds, emojis, and color-coded buttons- �🔄 **CoinsEngine Compatible**: Works directly with CoinsEngine shared database



---## Quick Install (New Two-Step Method)



## 🚀 Quick Installation```bash

curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install.sh | bash

### One-Line Install```



```bashThis will:

git clone https://github.com/dronzer-tb/economy-manager-v1.git && cd economy-manager-v1 && pip3 install -r requirements.txt -q && chmod +x setup-interactive.sh && ./setup-interactive.sh1. ✅ Download the bot files

```2. ✅ Install Python dependencies

3. ✅ Run interactive configuration wizard

This single command will:4. ✅ Start the bot

1. ✅ Clone the repository

2. ✅ Install Python dependencies (quietly)**Why two-step?** The bootstrap script downloads files first, then runs an interactive setup so you can properly configure the database and Discord settings.

3. ✅ Make setup script executable

4. ✅ Run interactive configuration wizard> ℹ️ When executed via `curl | bash`, the bootstrap script automatically reconnects to your terminal so the wizard can prompt for input safely. If a terminal is not available, it will instruct you to run `./setup-interactive.sh` manually.



The wizard will guide you through:## Manual Installation

- 🗄️ Database connection (MySQL/MariaDB)

- 🤖 Discord bot token```bash

- 🏠 Guild/Server ID# Clone the repository

- 👑 Admin role ID (optional)git clone https://github.com/dronzer-tb/economy-manager-v1.git

- 📢 Log channel ID (optional)cd economy-manager-v1



---# Install dependencies

pip3 install -r requirements.txt

## 📋 Requirements

# Run interactive setup

- **Python**: 3.8 or higher./setup-interactive.sh

- **Database**: MySQL or MariaDB```

- **Discord Bot**: Created in [Discord Developer Portal](https://discord.com/developers/applications)

- **CoinsEngine**: Plugin installed on your Minecraft server (or compatible database)## Configuration



### Required Python PackagesConfiguration is stored in `.env` file:

```

discord.py >= 2.0.0```env

mysql-connector-python >= 8.0.0# Database Configuration

python-dotenv >= 0.19.0DB_HOST=localhost

```### Configuration (.env file)



---The interactive setup wizard will create a `.env` file with these settings:



## 🎯 Discord Bot Setup```bash

# Database Configuration

### 1. Create Discord ApplicationDB_HOST=localhost

DB_PORT=3306

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)DB_USER=your_username

2. Click **New Application** and give it a nameDB_PASSWORD=your_password

3. Go to **Bot** section and click **Add Bot**DB_NAME=coinsengine_shared

4. Copy the **Token** (you'll need this during setup)

# Discord Configuration

### 2. Enable Intents (Required!)DISCORD_TOKEN=your_bot_token

GUILD_ID=your_server_id

In the Bot section, scroll down to **Privileged Gateway Intents** and enable:

- ✅ **Server Members Intent**# Optional Configuration

- ✅ **Message Content Intent**TABLE_NAME=coinsengine_users

ADMIN_ROLE_ID=your_admin_role_id

### 3. Invite Bot to ServerLOG_CHANNEL_ID=your_log_channel_id  # Optional: Channel for action logs



1. Go to **OAuth2** → **URL Generator**# Logging

2. Select scopes:LOG_LEVEL=INFO

   - ✅ `bot`LOG_FILE=logs/bot.log

   - ✅ `applications.commands````

3. Select bot permissions:

   - ✅ Send Messages### Running the Bot

   - ✅ Embed Links

   - ✅ Use Slash CommandsAfter configuration, start the bot:

4. Copy the generated URL and open it in browser

5. Select your server and authorize```bash

python3 bot/main.py

---```



## ⚙️ ConfigurationOr run in background:



### Environment Variables```bash

nohup python3 bot/main.py > logs/bot.log 2>&1 &

After running the setup wizard, a `.env` file is created:```



```env## Discord Logging Channel (Optional)

# Database Configuration (CoinsEngine)

DB_HOST=localhostThe bot can send action logs to a dedicated Discord channel:

DB_PORT=3306

DB_USER=minecraft1. Create a channel in your Discord server (e.g., `#economy-logs`)

DB_PASSWORD=your_password2. Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)

DB_NAME=coinsengine_shared3. Right-click the channel → Copy ID

TABLE_NAME=coinsengine_users4. Add the channel ID to your `.env` file:

   ```bash

# Discord Configuration   LOG_CHANNEL_ID=1234567890123456789

DISCORD_TOKEN=your_bot_token_here   ```

GUILD_ID=1234567890123456789

**What gets logged:**

# Access Control (Optional)- ✅ Bot startup/shutdown

ADMIN_ROLE_ID=1234567890123456789  # Only this role can use /manage- 💎 Gem additions/removals

- 🪙 Coin additions/removals

# Logging (Optional)- 👤 Admin who performed the action

LOG_CHANNEL_ID=1234567890123456789  # Discord channel for transaction logs- ⏰ Timestamp of each transaction

LOG_LEVEL=INFO

LOG_FILE=logs/bot.log## Database Schema

```

This bot is designed to work with the **CoinsEngine** plugin database structure:

### Getting Discord IDs

```sql

Enable **Developer Mode**: User Settings → Advanced → Developer ModeCREATE TABLE coinsengine_users (

    id INT AUTO_INCREMENT PRIMARY KEY,

Then right-click to copy IDs:    uuid MEDIUMTEXT NOT NULL,

- **Guild ID**: Right-click server icon → Copy Server ID    name MEDIUMTEXT NOT NULL,

- **Role ID**: Server Settings → Roles → Right-click role → Copy ID      dateCreated BIGINT NOT NULL,

- **Channel ID**: Right-click channel → Copy Channel ID    last_online BIGINT NOT NULL,

    settings MEDIUMTEXT NOT NULL,

---    hiddenFromTops TINYINT(1) NOT NULL,

    gems DOUBLE DEFAULT 0,

## 📖 Usage Guide    coins DOUBLE DEFAULT 100,

    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

### Starting the Bot);

```

```bash

# Foreground (see live logs)The bot uses the following columns:

python3 bot/main.py- `name` - Player's username

- `uuid` - Player's UUID

# Background (persistent)- `gems` - Gem balance (DOUBLE, supports decimals)

nohup python3 bot/main.py > logs/bot.log 2>&1 &- `coins` - Coin balance (DOUBLE, supports decimals)

```

## Usage

### Using the Bot in Discord

1. **Invoke the bot** in your Discord server

1. **Run the command**: Type `/manage` in Discord2. **Select "Manage Player"** from the main menu

3. **Choose a player** from the dropdown

2. **First view** (Page 1):4. **View their balance** (gems and coins displayed)

   ```5. **Take action**: Add/Remove Gems or Coins

   Economy Manager6. **Confirm transaction** and see the updated balance

   📊 Total Players: 127

   📋 Showing: 1-25## Project Structure

   

   🔍 Search: Fuzzy search enabled - type partial names```

   ⬅️➡️ Navigate: Use Previous/Next buttonseconomy-manager/

   ├── bot/                    # Bot source code

   [Player Dropdown ▼]│   ├── main.py            # Entry point

   [Search Player 🔍] [Next ➡️] [Page 1/6]│   ├── cogs/              # Command modules

   ```│   ├── database/          # Database layer

│   ├── ui/                # Discord UI components

3. **Navigate pages**: Click **Next** or **Previous** to browse players│   └── utils/             # Utilities

├── docs/                  # Documentation

4. **Search for player**: │   └── PRD.md            # Product Requirements

   - Click **Search Player 🔍**├── logs/                  # Agent activity logs

   - Type player name (fuzzy matching works!)│   └── agent_log.md      # Development log

   - Examples: "dronz" finds "DronzerTB"├── scripts/               # Installation/setup scripts

├── .env.example          # Environment template

5. **Manage currency**:├── requirements.txt      # Python dependencies

   - Select player from dropdown├── CHANGELOG.md          # Version history

   - View their balance (gems & coins)├── VERSION               # Current version

   - Click **Add Gems/Coins** or **Remove Gems/Coins**└── README.md            # This file

   - Enter amount and confirm```

   - Click **Refresh 🔄** to see updated balance

## Development

### Example Workflow

This project follows strict development protocols:

```- **Semantic Versioning**: All changes are versioned (MAJOR.MINOR.PATCH)

/manage- **Agent Logging**: Complete activity log in `logs/agent_log.md`

→ Search "dronzer" - **Testing**: All features must pass tests before version increments

→ Select DronzerTB- **Documentation**: PRD and CHANGELOG maintained for all changes

→ Click "Add Gems 💎"

→ Enter "100.50"See `prompts.txt` for complete development guidelines.

→ Confirm ✅

→ Log appears in #economy-log## Security

```

- ✅ Role-based access control

---- ✅ SQL injection prevention (parameterized queries)

- ✅ Secure credential storage (.env)

## 🗄️ Database Schema- ✅ Transaction logging and audit trail

- ✅ Input validation

### CoinsEngine Compatible Table

## Support

```sql

CREATE TABLE coinsengine_users (For issues, questions, or contributions:

    id INT AUTO_INCREMENT PRIMARY KEY,- Open an issue on GitHub

    uuid MEDIUMTEXT NOT NULL,- Check the [PRD](docs/PRD.md) for detailed requirements

    name MEDIUMTEXT NOT NULL,- Review [CHANGELOG](CHANGELOG.md) for recent updates

    gems DOUBLE DEFAULT 0,

    coins DOUBLE DEFAULT 0,## License

    last_online BIGINT,

    -- other CoinsEngine fields...MIT License - See LICENSE file for details

);

```## Version



**Used Columns:**Current Version: **0.2.0** (CoinsEngine Compatible)

- `uuid` - Player's Minecraft UUID (unique identifier)

- `name` - Player's username (for display)See [CHANGELOG.md](CHANGELOG.md) for version history.

- `gems` - Gem balance (supports decimals)

- `coins` - Coin balance (supports decimals)## What's New in 0.2.0



---- ✅ **CoinsEngine Database Support**: Now compatible with CoinsEngine plugin databases

- ✅ **Decimal Currency Support**: Supports decimal values for gems and coins

## 🎨 Features Breakdown- ✅ **One-Line Installer**: Easy installation with automated setup

- ✅ **Improved Table Detection**: Automatically validates database schema

### 🔍 Fuzzy Search- ✅ **UUID Display**: Shows player UUIDs in the management interface

- **Smart matching**: Finds players with typos or partial names

- **Relevance ranking**: Exact match → Contains → Fuzzy (40%+ similarity)---

- **Case-insensitive**: "DRONZER" = "dronzer" = "Dronzer"

- **Preview**: Shows top 5 results before dropdown**Status**: ✅ Production Ready - CoinsEngine Compatible


### 📄 Pagination
- **25 players per page**: Optimized for Discord's dropdown limit
- **Previous/Next buttons**: Easy navigation
- **Page counter**: Shows "Page 3/10"
- **Dynamic**: Buttons appear only when needed

### 💰 Currency Management
- **Decimal support**: Add/remove fractional amounts (e.g., 12.75 gems)
- **Balance validation**: Can't remove more than player has
- **Confirmation required**: Double-check before transactions
- **Real-time updates**: Refresh button fetches latest data

### 📊 Discord Logging
Optional logging channel records:
```
✅ DronzerTB added 100.00 gems to Player123
Performed by: @Admin#1234
```

---

## 📁 Project Structure

```
economy-manager-v1/
├── bot/
│   ├── main.py                 # Bot entry point
│   ├── __init__.py             # Version info
│   ├── cogs/
│   │   └── economy.py          # /manage command & callbacks
│   ├── database/
│   │   └── db_manager.py       # MySQL connection & queries
│   ├── ui/
│   │   └── views.py            # Discord UI components
│   └── utils/
│       ├── config.py           # .env loader
│       └── logger.py           # Logging setup
├── logs/
│   └── bot.log                 # Runtime logs
├── .env                        # Configuration (created by setup)
├── .env.example                # Template
├── requirements.txt            # Python dependencies
├── setup-interactive.sh        # Interactive setup wizard
├── CHANGELOG.md                # Version history
├── VERSION                     # Current version (0.4.0)
└── README.md                   # This file
```

---

## 🔒 Security Features

- ✅ **SQL Injection Prevention**: Parameterized queries with `buffered=True` cursors
- ✅ **Role-Based Access**: Only specified role can use `/manage` command
- ✅ **Credential Protection**: `.env` file not committed to git
- ✅ **Input Validation**: Amount checks, positive values only
- ✅ **Audit Trail**: All transactions logged with username & timestamp
- ✅ **Ephemeral Messages**: Bot responses only visible to command user

---

## 🐛 Troubleshooting

### Bot Won't Start
```bash
# Check Python version (needs 3.8+)
python3 --version

# Verify dependencies installed
pip3 install -r requirements.txt

# Check .env file exists
ls -la .env

# View error logs
tail -f logs/bot.log
```

### Commands Not Appearing
- ✅ Enable **Server Members Intent** and **Message Content Intent** in Discord Developer Portal
- ✅ Wait 10 seconds after bot starts (guild sync takes time)
- ✅ Check bot has **Use Slash Commands** permission

### Database Connection Failed
- ✅ Verify MySQL/MariaDB is running
- ✅ Check credentials in `.env` file
- ✅ Ensure user has SELECT, UPDATE permissions
- ✅ Test connection: `mysql -u user -p -h host database`

### Player Not Found Error
- ✅ Use UUID-based search (more reliable than names)
- ✅ Check player exists in `coinsengine_users` table
- ✅ Verify table name in `.env` matches actual table

---

## 📊 Version History

### v0.4.0 (Current) - 2025-11-10 🚀
- ✨ **Pagination**: Previous/Next buttons for unlimited players
- ✨ **Fuzzy Search**: Smart search with typo tolerance
- ✨ **Relevance Ranking**: Search results sorted by match quality
- 🎨 **Page Counter**: Shows current page position
- 📝 **Search Preview**: Top 5 results display

### v0.3.0 - 2025-11-10
- ✅ Refresh button fixed (UUID-based lookup)
- ✅ All currency operations working
- ✅ Production ready status

### v0.2.x - 2025-11-10
- 🔧 Bug fixes: UUID lookups, cursor buffering, duplicate names
- 🛠️ Database query optimizations

### v0.1.0
- 🎉 Initial release
- 💎 Basic currency management
- 🔘 Button interface

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🤝 Contributing

Contributions welcome! This project follows strict protocols:

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Follow** coding standards in `prompts.txt`
4. **Update** CHANGELOG.md with changes
5. **Increment** VERSION file (semantic versioning)
6. **Test** thoroughly before committing
7. **Submit** pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Credits

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Compatible with [CoinsEngine](https://www.spigotmc.org/resources/coinsengine.84121/) plugin
- Developed following MCP (Model Context Protocol) standards

---

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/dronzer-tb/economy-manager-v1/issues)
- 📖 **Docs**: See `docs/PRD.md` for detailed requirements
- 💬 **Discord**: (Add your support server invite here)

---

**Current Version**: `0.4.0` | **Status**: ✅ Production Ready

Made with ❤️ for Minecraft server administrators
