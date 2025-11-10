# Quick Start Guide - Economy Manager V1

## Prerequisites
- Python 3.8 or higher
- MySQL database (with player data)
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Discord Server with admin permissions

## Step-by-Step Setup

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
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=minecraft_economy

# Discord Configuration
DISCORD_TOKEN=your_discord_bot_token
GUILD_ID=your_server_id

# Optional
TABLE_NAME=players
ADMIN_ROLE_ID=your_admin_role_id
```

**Or use the interactive setup:**
```bash
python scripts/setup.py
```

### 3. Prepare Your Database

Make sure your MySQL database has a `players` table:

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

Add some test data:
```sql
INSERT INTO players (player_name, uuid, gems, coins) VALUES
('Steve', '069a79f4-44e9-4726-a5be-fca90e38aaf5', 100, 500),
('Alex', '0e6c3f48-0c6a-4c6e-9b5a-5f5c3f3f3f3f', 250, 1000);
```

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
- Verify MySQL is running
- Check credentials in `.env`
- Ensure `players` table exists
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

**Version**: 0.1.0  
**Status**: Ready for testing
