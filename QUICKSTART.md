# Quick Start Guide - Economy Manager V1

## One-Line Installation (Recommended)

The easiest way to install and set up the bot:

```bash
curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash
```

This automated installer will:
1. ✅ Check for Python 3, Git, and pip
2. ✅ Clone the repository
3. ✅ Install all dependencies
4. ✅ Run the interactive setup wizard
5. ✅ Start the bot automatically

**That's it!** The bot will be running after the setup completes.

---

## Manual Installation

### Prerequisites
- Python 3.8 or higher
- MySQL/MariaDB database with CoinsEngine data
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Discord Server with admin permissions

### Step-by-Step Setup

### 1. Install Dependencies

**Linux/macOS:**
```bash
cd "/home/kasniya/Economay manager"
./scripts/install.sh
```

**Windows:**
```cmd
cd "C:\path\to\Economay manager"
scripts\install.bat
```

Or manually:
```bash
pip install -r requirements.txt
```

### 2. Configure the Bot

Create your `.env` file:
```bash
cp .env.example .env
```

Then edit `.env` with your details:
```env
# Database Configuration
DB_HOST=172.18.0.1
DB_PORT=3306
DB_USER=coinsengine
DB_PASSWORD=your_password
DB_NAME=coinsengine_shared

# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_server_id

# Optional
TABLE_NAME=coinsengine_users
ADMIN_ROLE_ID=your_admin_role_id
```

**Or use the interactive setup:**
```bash
python scripts/setup.py
```

### 3. Prepare Your Database

The bot works with the **CoinsEngine** plugin database structure. Your database should have the `coinsengine_users` table:

```sql
-- Table should already exist if you're using CoinsEngine
-- Example structure:
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

**Required columns:**
- `name` - Player username
- `uuid` - Player UUID
- `gems` - Gem balance (DOUBLE)
- `coins` - Coin balance (DOUBLE)

If you're using CoinsEngine, this table already exists!

### 4. Setup Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token to your `.env` file
5. Enable these Privileged Gateway Intents:
   - Server Members Intent
   - Message Content Intent
6. Go to "OAuth2" > "URL Generator"
7. Select scopes: `bot`, `applications.commands`
8. Select permissions: `Administrator` (or at minimum: Send Messages, Use Slash Commands, Read Messages/View Channels)
9. Copy the generated URL and invite the bot to your server

### 5. Start the Bot

```bash
python bot/main.py
```

You should see:
```
INFO: Logged in as YourBotName (ID: 123456789)
INFO: Bot is ready! Connected to 1 guild(s)
```

### 6. Use the Bot

In your Discord server:
1. Type `/manage` to start managing player economies
2. Select a player from the dropdown
3. View their balance
4. Use buttons to add/remove gems or coins
5. Confirm transactions

## Troubleshooting

### Bot won't start
- Check your `.env` file has correct values
- Verify database connection with `python scripts/setup.py`
- Check bot token is valid

### Can't see slash commands
- Make sure bot has `applications.commands` scope
- Wait a few minutes for Discord to sync
- Try kicking and re-inviting the bot

### Database errors
- Verify MySQL/MariaDB is running
- Check credentials in `.env`
- Ensure `coinsengine_users` table exists
- Verify table has required columns (name, uuid, gems, coins)
- Check table name matches `TABLE_NAME` in `.env`

### Permission errors in Discord
- Bot needs Administrator permission or specific permissions
- Check role hierarchy (bot role must be above managed roles)
- Verify bot is in the correct server

## Need Help?

- Check the [README.md](README.md) for full documentation
- Review [PRD.md](docs/PRD.md) for feature details
- Check logs in `logs/bot.log` for errors
- Open an issue on GitHub

## Next Steps

- Test all features (add/remove gems/coins)
- Set up a specific admin role (update `ADMIN_ROLE_ID`)
- Monitor logs for any issues
- Consider setting up automated backups of your database

---

**Version**: 0.2.0  
**Status**: Production Ready - CoinsEngine Compatible
