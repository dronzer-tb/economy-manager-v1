"""
Economy Management Cog for Economy Manager Bot
Version: 0.1.0
Handles economy-related commands and interactions
"""

import discord
from discord.ext import commands
from discord import app_commands
import logging
from bot.ui.views import PlayerSelectView, EconomyManagementView, create_player_embed

logger = logging.getLogger('economy_bot')

class Economy(commands.Cog):
    """Cog for handling economy management."""
    
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="manage", description="Manage player economy")
    @app_commands.default_permissions(administrator=True)
    async def manage_economy(self, interaction: discord.Interaction):
        """
        Main command to start economy management.
        Shows dropdown to select a player.
        """
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Fetch all players from database
            players = await self.bot.db_manager.get_all_players()
            
            if not players:
                await interaction.followup.send(
                    "❌ No players found in the database.",
                    ephemeral=True
                )
                return
                
            # Create and send player selection view
            view = PlayerSelectView(players, self.on_player_selected)
            
            total_players = len(players)
            shown_players = min(25, total_players)
            
            message = f"**Economy Manager**\n"
            message += f"📊 Total Players: {total_players}\n"
            message += f"📋 Showing: 1-{shown_players}\n\n"
            message += f"🔍 **Search**: Fuzzy search enabled - type partial names\n"
            if total_players > 25:
                message += f"⬅️➡️ **Navigate**: Use Previous/Next buttons to browse all players"
            
            await interaction.followup.send(
                message,
                view=view,
                ephemeral=True
            )
            
        except Exception as e:
            logger.error(f"Error in manage_economy command: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )
            
    async def on_player_selected(self, interaction: discord.Interaction, player_uuid: str):
        """
        Callback when a player is selected from dropdown.
        
        Args:
            interaction: Discord interaction
            player_uuid: Selected player's UUID
        """
        await interaction.response.defer()
        
        try:
            # Fetch player data using UUID
            player_data = await self.bot.db_manager.get_player_balance(player_uuid)
            
            if not player_data:
                await interaction.followup.send(
                    f"❌ Player with UUID '{player_uuid}' not found.",
                    ephemeral=True
                )
                return
                
            # Get player name from database result
            player_name = player_data.get('name', 'Unknown')
            
            # Create embed with player info
            embed = create_player_embed(player_name, player_data)
            
            # Create management view with buttons (pass bot instance for logging and UUID for refresh)
            view = EconomyManagementView(player_name, player_data, self.bot.db_manager, self.bot, player_uuid)
            
            await interaction.followup.send(
                embed=embed,
                view=view,
                ephemeral=True
            )
            
            logger.info(f"User {interaction.user} is managing economy for {player_name}")
            
        except Exception as e:
            logger.error(f"Error in on_player_selected: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )
            
    @commands.Cog.listener()
    async def on_ready(self):
        """Sync slash commands when cog is ready."""
        try:
            # Sync to specific guild if configured for instant updates
            if self.bot.config.GUILD_ID:
                guild = discord.Object(id=self.bot.config.GUILD_ID)
                self.bot.tree.copy_global_to(guild=guild)
                synced = await self.bot.tree.sync(guild=guild)
                logger.info(f"Synced {len(synced)} command(s) to guild {self.bot.config.GUILD_ID}")
            else:
                # Global sync (takes up to 1 hour to propagate)
                synced = await self.bot.tree.sync()
                logger.info(f"Synced {len(synced)} command(s) globally (may take up to 1 hour)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}", exc_info=True)

async def setup(bot):
    """Setup function to add cog to bot."""
    await bot.add_cog(Economy(bot))
