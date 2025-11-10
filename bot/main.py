"""
Economy Manager V1 - Main Bot Entry Point
Version: 0.1.0
"""

import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from bot.utils.config import Config
from bot.utils.logger import setup_logger
from bot.database.db_manager import DatabaseManager

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()

class EconomyBot(commands.Bot):
    """Main bot class for Economy Manager."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',  # Fallback prefix, mainly using buttons
            intents=intents,
            help_command=None
        )
        
        self.config = Config()
        self.db_manager = None
        
    async def setup_hook(self):
        """Setup hook called before bot starts."""
        logger.info("Setting up bot...")
        
        # Initialize database connection
        self.db_manager = DatabaseManager(
            host=self.config.DB_HOST,
            port=self.config.DB_PORT,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            database=self.config.DB_NAME
        )
        
        await self.db_manager.connect()
        logger.info("Database connection established")
        
        # Load cogs
        await self.load_extension('bot.cogs.economy')
        logger.info("Loaded economy cog")
        
    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f'Logged in as {self.user.name} (ID: {self.user.id})')
        logger.info(f'Bot is ready! Connected to {len(self.guilds)} guild(s)')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="player economies 💎"
            )
        )
        
    async def on_error(self, event, *args, **kwargs):
        """Global error handler."""
        logger.error(f"Error in event {event}", exc_info=True)
        
    async def close(self):
        """Cleanup before shutdown."""
        logger.info("Shutting down bot...")
        if self.db_manager:
            await self.db_manager.close()
            logger.info("Database connection closed")
        await super().close()

def main():
    """Main entry point."""
    bot = EconomyBot()
    
    try:
        bot.run(bot.config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
