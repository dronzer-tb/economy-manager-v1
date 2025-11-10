"""
Configuration management for Economy Manager Bot
Version: 0.1.0
"""

import os
from typing import Optional

class Config:
    """Bot configuration loaded from environment variables."""
    
    def __init__(self):
        # Database Configuration
        self.DB_HOST: str = os.getenv('DB_HOST', 'localhost')
        self.DB_PORT: int = int(os.getenv('DB_PORT', '3306'))
        self.DB_USER: str = os.getenv('DB_USER', '')
        self.DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
        self.DB_NAME: str = os.getenv('DB_NAME', 'coinsengine_shared')
        
        # Discord Configuration
        self.DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '')
        self.GUILD_ID: Optional[int] = self._get_optional_int('GUILD_ID')
        
        # Optional Configuration
        self.TABLE_NAME: str = os.getenv('TABLE_NAME', 'coinsengine_users')
        self.ADMIN_ROLE_ID: Optional[int] = self._get_optional_int('ADMIN_ROLE_ID')
        
        # Logging
        self.LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE: str = os.getenv('LOG_FILE', 'logs/bot.log')
        
        # Validate required configuration
        self._validate()
        
    def _get_optional_int(self, key: str) -> Optional[int]:
        """Get optional integer from environment."""
        value = os.getenv(key)
        return int(value) if value else None
        
    def _validate(self):
        """Validate required configuration values."""
        if not self.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in .env file")
        if not self.DB_USER:
            raise ValueError("DB_USER is required in .env file")
        if not self.DB_PASSWORD:
            raise ValueError("DB_PASSWORD is required in .env file")
