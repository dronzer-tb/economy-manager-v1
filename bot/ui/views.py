"""
UI Components for Economy Manager Bot
Version: 0.1.0
Discord UI Views, Buttons, Modals, and Select Menus
"""

import discord
from discord import ui
from typing import List, Optional, Callable
import logging
from difflib import SequenceMatcher

logger = logging.getLogger('economy_bot')

class PlayerSelectView(ui.View):
    """View for selecting a player from dropdown with pagination and search."""
    
    def __init__(self, players: List[dict], callback: Callable, page: int = 0):
        super().__init__(timeout=300)
        self.callback_func = callback
        self.all_players = players  # Store all players
        self.page = page
        self.page_size = 25
        
        # Calculate pagination
        total_pages = (len(players) - 1) // self.page_size + 1 if players else 0
        start_idx = page * self.page_size
        end_idx = start_idx + self.page_size
        current_players = players[start_idx:end_idx]
        
        # Add player select dropdown
        self.add_item(PlayerSelect(current_players, self.on_player_select))
        
        # Add Previous button if not on first page
        if page > 0:
            prev_button = ui.Button(label="Previous", style=discord.ButtonStyle.secondary, emoji="⬅️")
            prev_button.callback = self.previous_page
            self.add_item(prev_button)
        
        # Add Next button if there are more pages
        if end_idx < len(players):
            next_button = ui.Button(label="Next", style=discord.ButtonStyle.secondary, emoji="➡️")
            next_button.callback = self.next_page
            self.add_item(next_button)
        
        # Page info (disabled button as label)
        page_info = ui.Button(
            label=f"Page {page + 1}/{total_pages}",
            style=discord.ButtonStyle.secondary,
            disabled=True
        )
        self.add_item(page_info)
        
    async def on_player_select(self, interaction: discord.Interaction, selected_player: str):
        """Handle player selection."""
        await self.callback_func(interaction, selected_player)
    
    async def previous_page(self, interaction: discord.Interaction):
        """Go to previous page."""
        new_view = PlayerSelectView(self.all_players, self.callback_func, self.page - 1)
        
        total_players = len(self.all_players)
        start_idx = (self.page - 1) * self.page_size + 1
        end_idx = min(self.page * self.page_size, total_players)
        
        await interaction.response.edit_message(
            content=f"**Economy Manager**\n📊 Total Players: {total_players}\n📋 Showing: {start_idx}-{end_idx}",
            view=new_view
        )
    
    async def next_page(self, interaction: discord.Interaction):
        """Go to next page."""
        new_view = PlayerSelectView(self.all_players, self.callback_func, self.page + 1)
        
        total_players = len(self.all_players)
        start_idx = (self.page + 1) * self.page_size + 1
        end_idx = min((self.page + 2) * self.page_size, total_players)
        
        await interaction.response.edit_message(
            content=f"**Economy Manager**\n📊 Total Players: {total_players}\n📋 Showing: {start_idx}-{end_idx}",
            view=new_view
        )
    
    @ui.button(label="Search Player", style=discord.ButtonStyle.primary, emoji="🔍", row=4)
    async def search_button(self, interaction: discord.Interaction, button: ui.Button):
        """Button to search for a player by name."""
        modal = PlayerSearchModal(self.all_players, self.callback_func)
        await interaction.response.send_modal(modal)


class PlayerSelect(ui.Select):
    """Dropdown menu for selecting players."""
    
    def __init__(self, players: List[dict], callback: Callable):
        self.callback_func = callback
        self.player_map = {}  # Map UUID to player data
        
        # Create options from players (max 25 options per Discord limitation)
        options = []
        for i, player in enumerate(players[:25]):
            # Use 'name' field from coinsengine_users table
            player_name = player.get('name', player.get('uuid', f'Player {i+1}'))
            uuid = player.get('uuid', f'unknown_{i}')
            gems = player.get('gems', 0)
            coins = player.get('coins', 0)
            
            # Store player data mapped by UUID
            self.player_map[uuid] = player_name
            
            options.append(
                discord.SelectOption(
                    label=player_name,
                    description=f"💎 {gems:.2f} gems | 🪙 {coins:.2f} coins",
                    value=uuid  # Use UUID as value to ensure uniqueness
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
        selected_uuid = self.values[0]
        # Pass UUID to callback - it will be used for database lookup
        await self.callback_func(interaction, selected_uuid)


class EconomyManagementView(ui.View):
    """View with buttons for managing player economy."""
    
    def __init__(self, player_name: str, player_data: dict, db_manager, bot=None, player_uuid: str = None):
        super().__init__(timeout=300)  # 5 minute timeout
        self.player_name = player_name
        self.player_uuid = player_uuid or player_data.get('uuid', player_name)  # Fallback to name if no UUID
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
        # Fetch updated player data using UUID
        player_data = await self.db_manager.get_player_balance(self.player_uuid)
        
        if player_data:
            # Update player name in case it changed
            self.player_name = player_data.get('name', self.player_name)
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


class PlayerSearchModal(ui.Modal):
    """Modal for searching players by name with fuzzy matching."""
    
    def __init__(self, all_players: List[dict], callback: Callable):
        super().__init__(title="Search Player")
        self.all_players = all_players
        self.callback_func = callback
        
        # Add search input field
        self.search_input = ui.TextInput(
            label="Player Name",
            placeholder="Enter player name (fuzzy search enabled)...",
            required=True,
            min_length=1,
            max_length=50
        )
        self.add_item(self.search_input)
    
    def fuzzy_match_score(self, search_term: str, player_name: str) -> float:
        """
        Calculate fuzzy match score between search term and player name.
        Returns a score between 0 and 1, where 1 is perfect match.
        """
        search_lower = search_term.lower()
        name_lower = player_name.lower()
        
        # Exact match gets highest score
        if search_lower == name_lower:
            return 1.0
        
        # Contains gets high score
        if search_lower in name_lower:
            return 0.9
        
        # Use SequenceMatcher for fuzzy matching
        return SequenceMatcher(None, search_lower, name_lower).ratio()
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle search submission with fuzzy matching."""
        await interaction.response.defer()
        
        search_term = self.search_input.value.strip()
        
        # Calculate fuzzy match scores for all players
        scored_players = []
        for player in self.all_players:
            player_name = player.get('name', '')
            score = self.fuzzy_match_score(search_term, player_name)
            
            # Only include players with score > 0.4 (40% similarity)
            if score > 0.4:
                scored_players.append((score, player))
        
        # Sort by score (highest first)
        scored_players.sort(key=lambda x: x[0], reverse=True)
        matches = [player for score, player in scored_players]
        
        if not matches:
            await interaction.followup.send(
                f"❌ No players found matching '{self.search_input.value}'\nTry a different search term or use pagination.",
                ephemeral=True
            )
            return
        
        if len(matches) == 1:
            # Only one match, directly select it
            player_uuid = matches[0].get('uuid')
            await self.callback_func(interaction, player_uuid)
        else:
            # Multiple matches, show dropdown with results (sorted by relevance)
            view = PlayerSelectView(matches, self.callback_func)
            
            # Show top 5 match names as preview
            preview_names = [m.get('name', 'Unknown') for m in matches[:5]]
            preview_text = "\n".join([f"• {name}" for name in preview_names])
            if len(matches) > 5:
                preview_text += f"\n• ... and {len(matches) - 5} more"
            
            await interaction.followup.send(
                f"**Search Results** ({len(matches)} players found)\n"
                f"Results sorted by relevance:\n{preview_text}\n\n"
                f"Select a player from the dropdown:",
                view=view,
                ephemeral=True
            )


def create_player_embed(player_name: str, player_data: dict) -> discord.Embed:
    """
    Create an embed displaying player economy information.
    
    Args:
        player_name: Player name
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
