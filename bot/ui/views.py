"""
UI Components for Economy Manager Bot
Version: 0.1.0
Discord UI Views, Buttons, Modals, and Select Menus
"""

import discord
from discord import ui
from typing import List, Optional, Callable
import logging

logger = logging.getLogger('economy_bot')

class PlayerSelectView(ui.View):
    """View with dropdown to select a player."""
    
    def __init__(self, players: List[dict], callback: Callable):
        super().__init__(timeout=180)  # 3 minute timeout
        self.callback_func = callback
        
        # Add player select dropdown
        self.add_item(PlayerSelect(players, self.on_player_select))
        
    async def on_player_select(self, interaction: discord.Interaction, selected_player: str):
        """Handle player selection."""
        await self.callback_func(interaction, selected_player)


class PlayerSelect(ui.Select):
    """Dropdown menu for selecting players."""
    
    def __init__(self, players: List[dict], callback: Callable):
        self.callback_func = callback
        
        # Create options from players (max 25 options per Discord limitation)
        options = []
        for i, player in enumerate(players[:25]):
            # Use 'name' field from coinsengine_users table
            player_name = player.get('name', player.get('uuid', f'Player {i+1}'))
            gems = player.get('gems', 0)
            coins = player.get('coins', 0)
            
            options.append(
                discord.SelectOption(
                    label=player_name,
                    description=f"💎 {gems:.2f} gems | 🪙 {coins:.2f} coins",
                    value=player_name
                )
            )
            
        super().__init__(
            placeholder="Choose a player to manage...",
            min_values=1,
            max_values=1,
            options=options
        )
        
    async def callback(self, interaction: discord.Interaction):
        """Handle selection callback."""
        selected = self.values[0]
        await self.callback_func(interaction, selected)


class EconomyManagementView(ui.View):
    """View with buttons for managing player economy."""
    
    def __init__(self, player_name: str, player_data: dict, db_manager, bot=None):
        super().__init__(timeout=300)  # 5 minute timeout
        self.player_name = player_name
        self.player_data = player_data
        self.db_manager = db_manager
        self.bot = bot  # Bot instance for logging
        
    @ui.button(label="Add Gems", style=discord.ButtonStyle.success, emoji="💎")
    async def add_gems_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to add gems."""
        modal = CurrencyModal(
            title="Add Gems",
            player_name=self.player_name,
            currency_type="gems",
            operation="add",
            db_manager=self.db_manager,
            bot=self.bot
        )
        await interaction.response.send_modal(modal)
        
    @ui.button(label="Remove Gems", style=discord.ButtonStyle.danger, emoji="💎")
    async def remove_gems_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to remove gems."""
        modal = CurrencyModal(
            title="Remove Gems",
            player_name=self.player_name,
            currency_type="gems",
            operation="remove",
            db_manager=self.db_manager,
            bot=self.bot
        )
        await interaction.response.send_modal(modal)
        
    @ui.button(label="Add Coins", style=discord.ButtonStyle.success, emoji="🪙")
    async def add_coins_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to add coins."""
        modal = CurrencyModal(
            title="Add Coins",
            player_name=self.player_name,
            currency_type="coins",
            operation="add",
            db_manager=self.db_manager,
            bot=self.bot
        )
        await interaction.response.send_modal(modal)
        
    @ui.button(label="Remove Coins", style=discord.ButtonStyle.danger, emoji="🪙")
    async def remove_coins_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to remove coins."""
        modal = CurrencyModal(
            title="Remove Coins",
            player_name=self.player_name,
            currency_type="coins",
            operation="remove",
            db_manager=self.db_manager,
            bot=self.bot
        )
        await interaction.response.send_modal(modal)
        
    @ui.button(label="Refresh", style=discord.ButtonStyle.primary, emoji="🔄")
    async def refresh_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to refresh player data."""
        # Fetch updated player data
        player_data = await self.db_manager.get_player_balance(self.player_name)
        
        if player_data:
            embed = create_player_embed(self.player_name, player_data)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message(
                "❌ Error fetching player data.",
                ephemeral=True
            )


class CurrencyModal(ui.Modal):
    """Modal for inputting currency amount."""
    
    def __init__(self, title: str, player_name: str, currency_type: str, 
                 operation: str, db_manager, bot=None):
        super().__init__(title=title)
        self.player_name = player_name
        self.currency_type = currency_type
        self.operation = operation
        self.db_manager = db_manager
        self.bot = bot  # Bot instance for logging
        
        # Add input field
        self.amount_input = ui.TextInput(
            label="Amount",
            placeholder="Enter amount...",
            required=True,
            min_length=1,
            max_length=10
        )
        self.add_item(self.amount_input)
        
    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        try:
            # Support decimal values for gems/coins
            amount = float(self.amount_input.value)
            
            if amount <= 0:
                await interaction.response.send_message(
                    "❌ Amount must be positive!",
                    ephemeral=True
                )
                return
                
            # Show confirmation
            confirm_view = ConfirmationView(
                player_name=self.player_name,
                currency_type=self.currency_type,
                amount=amount,
                operation=self.operation,
                db_manager=self.db_manager,
                bot=self.bot
            )
            
            emoji = "💎" if self.currency_type == "gems" else "🪙"
            action = "Add" if self.operation == "add" else "Remove"
            
            await interaction.response.send_message(
                f"**Confirmation Required**\n"
                f"{action} **{amount:.2f}** {emoji} {self.currency_type} "
                f"{'to' if self.operation == 'add' else 'from'} **{self.player_name}**?",
                view=confirm_view,
                ephemeral=True
            )
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid amount! Please enter a number (decimals allowed).",
                ephemeral=True
            )


class ConfirmationView(ui.View):
    """View for confirming currency transactions."""
    
    def __init__(self, player_name: str, currency_type: str, amount: int,
                 operation: str, db_manager, bot=None):
        super().__init__(timeout=60)
        self.player_name = player_name
        self.currency_type = currency_type
        self.amount = amount
        self.operation = operation
        self.db_manager = db_manager
        self.bot = bot  # Bot instance for logging
        
    @ui.button(label="Confirm", style=discord.ButtonStyle.success, emoji="✅")
    async def confirm_button(self, interaction: discord.Interaction, button: ui.Button):
        """Confirm the transaction."""
        success, message = await self.db_manager.update_currency(
            player_name=self.player_name,
            currency_type=self.currency_type,
            amount=self.amount,
            operation=self.operation
        )
        
        if success:
            await interaction.response.edit_message(
                content=f"✅ {message}",
                view=None
            )
            
            # Send log to log channel
            if self.bot:
                emoji = "💎" if self.currency_type == "gems" else "🪙"
                action = "Added" if self.operation == "add" else "Removed"
                log_message = (
                    f"{emoji} **Economy Update**\n"
                    f"**Action:** {action} {self.amount:.2f} {self.currency_type}\n"
                    f"**Player:** {self.player_name}\n"
                    f"**Admin:** {interaction.user.mention}\n"
                    f"**Time:** <t:{int(interaction.created_at.timestamp())}:F>"
                )
                await self.bot.send_log(log_message)
        else:
            await interaction.response.edit_message(
                content=f"❌ {message}",
                view=None
            )
            
        # Disable all buttons
        for item in self.children:
            item.disabled = True
            
    @ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="❌")
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        """Cancel the transaction."""
        await interaction.response.edit_message(
            content="❌ Transaction cancelled.",
            view=None
        )


def create_player_embed(player_name: str, player_data: dict) -> discord.Embed:
    """
    Create an embed displaying player economy information.
    
    Args:
        player_name: Player's name
        player_data: Dictionary with player data
        
    Returns:
        Discord Embed object
    """
    gems = float(player_data.get('gems', 0))
    coins = float(player_data.get('coins', 0))
    uuid = player_data.get('uuid', 'N/A')
    
    embed = discord.Embed(
        title=f"💰 Economy Manager",
        description=f"**Player:** {player_name}\n**UUID:** `{uuid}`",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="💎 Gems",
        value=f"`{gems:,.2f}`",
        inline=True
    )
    
    embed.add_field(
        name="🪙 Coins",
        value=f"`{coins:,.2f}`",
        inline=True
    )
    
    embed.set_footer(text="Use the buttons below to manage this player's economy")
    
    return embed
