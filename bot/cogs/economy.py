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
            
            await interaction.followup.send(
                "**Economy Manager**\nSelect a player to manage:",
                view=view,
                ephemeral=True
            )
            
        except Exception as e:
            logger.error(f"Error in manage_economy command: {e}", exc_info=True)
            await interaction.followup.send(
                f"❌ An error occurred: {str(e)}",
                ephemeral=True
            )
            
    async def on_player_selected(self, interaction: discord.Interaction, player_name: str):
        """
        Callback when a player is selected from dropdown.
        
        Args:
            interaction: Discord interaction
            player_name: Selected player's name
        """
        await interaction.response.defer()
        
        try:
            # Fetch player data
            player_data = await self.bot.db_manager.get_player_balance(player_name)
            
            if not player_data:
                await interaction.followup.send(
                    f"❌ Player '{player_name}' not found.",
                    ephemeral=True
                )
                return
                
            # Create embed with player info
            embed = create_player_embed(player_name, player_data)
            
            # Create management view with buttons (pass bot instance for logging)
            view = EconomyManagementView(player_name, player_data, self.bot.db_manager, self.bot)
            
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
            synced = await self.bot.tree.sync()
            logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

async def setup(bot):
    """Setup function to add cog to bot."""
    await bot.add_cog(Economy(bot))
