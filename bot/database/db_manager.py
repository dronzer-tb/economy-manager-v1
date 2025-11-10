"""
Database Manager for Economy Manager Bot
Version: 0.1.0
Handles MySQL database connections and queries
"""

import mysql.connector
from mysql.connector import Error, pooling
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger('economy_bot')

class DatabaseManager:
    """Manages MySQL database connections and operations."""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str, 
                 pool_name: str = "economy_pool", pool_size: int = 5):
        """
        Initialize database manager with connection pooling.
        
        Args:
            host: Database host
            port: Database port
            user: Database user
            password: Database password
            database: Database name
            pool_name: Connection pool name
            pool_size: Number of connections in pool
        """
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'pool_name': pool_name,
            'pool_size': pool_size
        }
        self.pool = None
        
    async def connect(self) -> bool:
        """
        Establish database connection pool.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.pool = mysql.connector.pooling.MySQLConnectionPool(**self.config)
            logger.info(f"Database connection pool created: {self.config['pool_name']}")
            
            # Test connection
            connection = self.pool.get_connection()
            if connection.is_connected():
                logger.info("Database connection test successful")
                connection.close()
                return True
        except Error as e:
            logger.error(f"Database connection error: {e}")
            return False
            
    async def close(self):
        """Close all database connections."""
        # MySQL connector pool doesn't have explicit close, connections auto-close
        logger.info("Database connections will auto-close")
        
    def _get_connection(self):
        """Get connection from pool."""
        if not self.pool:
            raise Exception("Database pool not initialized")
        return self.pool.get_connection()
        
    async def get_all_players(self, table_name: str = 'coinsengine_users') -> List[Dict[str, any]]:
        """
        Retrieve all players from database.
        
        Args:
            table_name: Name of the players table
            
        Returns:
            List of player dictionaries
        """
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = f"SELECT id, uuid, name, gems, coins, last_online FROM {table_name} ORDER BY name"
            cursor.execute(query)
            players = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            logger.debug(f"Retrieved {len(players)} players from database")
            return players
            
        except Error as e:
            logger.error(f"Error fetching players: {e}")
            return []
            
    async def get_player_balance(self, player_name: str, table_name: str = 'coinsengine_users') -> Optional[Dict[str, any]]:
        """
        Get a specific player's balance.
        
        Args:
            player_name: Player's name or UUID
            table_name: Name of the players table
            
        Returns:
            Dictionary with player data or None
        """
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            
            # Using parameterized query to prevent SQL injection
            # Note: Column is 'name' not 'player_name' in coinsengine_users table
            query = f"SELECT id, uuid, name, gems, coins, last_online FROM {table_name} WHERE name = %s OR uuid = %s"
            cursor.execute(query, (player_name, player_name))
            player = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            return player
            
        except Error as e:
            logger.error(f"Error fetching player balance: {e}")
            return None
            
    async def update_currency(self, player_name: str, currency_type: str, 
                            amount: float, operation: str = 'add',
                            table_name: str = 'coinsengine_users') -> Tuple[bool, str]:
        """
        Update player's currency (gems or coins).
        
        Args:
            player_name: Player's name or UUID
            currency_type: 'gems' or 'coins'
            amount: Amount to add/remove (supports decimals)
            operation: 'add' or 'remove'
            table_name: Name of the players table
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if currency_type not in ['gems', 'coins']:
            return False, "Invalid currency type. Use 'gems' or 'coins'."
            
        if amount <= 0:
            return False, "Amount must be positive."
            
        try:
            connection = self._get_connection()
            cursor = connection.cursor(buffered=True)
            
            # First, get current balance to check for negative balance
            # Note: Column is 'name' not 'player_name' in coinsengine_users table
            cursor.execute(
                f"SELECT {currency_type} FROM {table_name} WHERE name = %s OR uuid = %s",
                (player_name, player_name)
            )
            result = cursor.fetchone()
            
            if not result:
                cursor.close()
                connection.close()
                return False, "Player not found."
                
            current_balance = float(result[0])
            
            # Calculate new balance
            if operation == 'add':
                new_balance = current_balance + amount
            elif operation == 'remove':
                new_balance = current_balance - amount
                if new_balance < 0:
                    cursor.close()
                    connection.close()
                    return False, f"Insufficient balance. Current: {current_balance:.2f}, Trying to remove: {amount:.2f}"
            else:
                cursor.close()
                connection.close()
                return False, "Invalid operation. Use 'add' or 'remove'."
                
            # Update database - use 'name' column instead of 'player_name'
            query = f"UPDATE {table_name} SET {currency_type} = %s WHERE name = %s OR uuid = %s"
            cursor.execute(query, (new_balance, player_name, player_name))
            connection.commit()
            
            affected_rows = cursor.rowcount
            cursor.close()
            connection.close()
            
            if affected_rows > 0:
                logger.info(f"Updated {player_name}: {operation} {amount} {currency_type}")
                return True, f"Successfully {operation}ed {amount:.2f} {currency_type}. New balance: {new_balance:.2f}"
            else:
                return False, "No rows updated."
                
        except Error as e:
            logger.error(f"Error updating currency: {e}")
            return False, f"Database error: {str(e)}"
