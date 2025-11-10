# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.3.1] - 2025-11-10
### Added
- **Search Player** button to find players beyond the first 25
- Player search modal with partial name matching
- Shows total player count and how many are displayed
- Automatic selection for single search result
- Dropdown for multiple search results

### Fixed
- Fixed limitation showing only first 25 players (A-M)
- All players now accessible via search feature
- Better UX with clear instructions when >25 players exist

## [0.3.0] - 2025-11-10 - PRODUCTION READY 🎉
### Fixed
- Fixed refresh button to use UUID for player lookup
- EconomyManagementView now stores and uses player UUID
- Refresh button now correctly fetches updated player data

### Notes
- All core features working: player selection, currency management, logging
- All buttons functional: Add/Remove Gems/Coins, Refresh
- Ready for production deployment

## [0.2.9] - 2025-11-10
### Fixed
- Fixed "Unread result found" error in update_currency function
- Added buffered cursor to properly handle multiple queries
- All currency update operations now work correctly

## [0.2.8] - 2025-11-10
### Fixed
- Fixed player lookup using UUID instead of player name
- Database queries now use UUID as primary identifier
- Player name retrieved from database result for display
- Resolves "Player not found" error after dropdown selection

## [0.2.7] - 2025-11-10
### Fixed
- **CRITICAL**: Fixed "The specified option value is already used" error with duplicate player names
- Player dropdown now uses UUID as unique identifier instead of player name
- Handles databases with multiple players having the same name correctly

### Changed
- Player selection now uses UUID internally while still displaying player name
- Added player_map to track UUID to name mapping

## [0.2.6] - 2025-11-10
### Fixed
- **CRITICAL**: Fixed slash commands not appearing in Discord
- Commands now sync instantly to specific guild (when GUILD_ID is configured)
- Added proper guild-specific command syncing for immediate availability
- Global sync fallback for bots without GUILD_ID (note: takes up to 1 hour)

### Changed
- Improved command sync logging with guild information
- Better error handling for command sync failures

## [0.2.5] - 2025-11-10
### Fixed
- **CRITICAL**: Rewrote interactive setup to use bash `read` instead of Python `input()`
- Eliminated all EOFError issues by avoiding Python heredoc stdin conflicts
- Database connection testing now works correctly
- All prompts now display and accept input properly

### Changed
- Interactive configuration now uses native bash for all user input
- Python only used for database testing and .env file writing (no stdin required)
- Improved error handling and user feedback

## [0.2.4] - 2025-11-10
### Fixed
- Resolved `EOFError` during installer when run via `curl | bash` by reattaching to `/dev/tty`
- Added guard to `setup-interactive.sh` requiring an interactive terminal

### Changed
- Bootstrap installer now warns and provides manual instructions if `/dev/tty` unavailable
- README clarifies how the installer behaves in non-interactive environments

## [0.2.3] - 2025-11-10
### Added
- **Two-Step Installer**: New `install.sh` bootstrap script + `setup-interactive.sh` for proper interactive configuration
- **Discord Logging Channel**: Bot can now send action logs to a dedicated Discord channel
  * Configure via `LOG_CHANNEL_ID` in .env
  * Logs all economy transactions with admin info and timestamps
  * Logs bot startup/shutdown events
- **Python Path Fix**: Added sys.path modification to fix `ModuleNotFoundError` when running bot

### Changed
- **Installation Method**: Split installer into bootstrap (curl-friendly) and interactive setup
  * `install.sh`: Downloads files and launches interactive setup
  * `setup-interactive.sh`: Runs AFTER clone for full interactive configuration
- Updated bot/main.py to add project root to Python path automatically
- Enhanced .env.example with LOG_CHANNEL_ID field

### Fixed
- Fixed `ModuleNotFoundError: No module named 'bot'` when running `python3 bot/main.py`
- Interactive configuration now works properly (no EOFError)

## [0.2.2] - 2025-11-10
### Fixed
- Fixed setup.sh to handle non-interactive mode when piped from curl
- Added interactive terminal detection (`[ -t 0 ]` check)
- Non-interactive mode now creates .env from template instead of prompting
- Fixed directory existence check to work in both interactive and non-interactive modes
- Improved user feedback for both installation modes

## [0.2.1] - 2025-11-10
### Fixed
- Fixed install-bot.sh not changing directory after cloning repository
- Added error handling for directory change operation

## [0.2.0] - 2025-11-10
### Added
- One-line installer script (install-bot.sh) for automated deployment
- Support for CoinsEngine plugin database structure
- Decimal value support for gems and coins (DOUBLE type)
- UUID display in player management interface
- Automatic database schema validation during setup

### Changed
- **BREAKING**: Updated database schema to use CoinsEngine format
  * Table name: `coinsengine_users` (instead of `players`)
  * Column name: `name` (instead of `player_name`)
  * Database name: `coinsengine_shared` (default)
  * Currency types now use DOUBLE instead of INT
- Updated all database queries to use new column names
- Modified UI to display decimal values with 2 decimal places
- Enhanced setup script to validate table structure
- Updated default configuration values

### Fixed
- Database column name mismatch (player_name vs name)
- Integer-only currency values (now supports decimals)
- Table name configuration defaults

## [0.1.0] - 2025-11-10
### Added
- Initial project structure (docs/, logs/, bot/, scripts/)
- VERSION file tracking (0.1.0)
- Agent activity log system [Link to agent_log.md entry #1]
- CHANGELOG.md for version tracking
- PRD.md with complete product requirements
- README.md with comprehensive project overview
- Discord bot implementation using discord.py v2.0+
- MySQL database integration with connection pooling
- Button-based UI with discord.ui components:
  * Player selection dropdown (discord.ui.Select)
  * Economy management buttons (Add/Remove Gems/Coins)
  * Currency input modals (discord.ui.Modal)
  * Transaction confirmation system
- Database manager with parameterized queries (SQL injection prevention)
- Configuration management using python-dotenv
- Comprehensive logging system (file + console)
- Installation scripts for Linux/macOS (install.sh) and Windows (install.bat)
- Interactive setup script with database connection validation
- Environment variable template (.env.example)
- MIT LICENSE
- .gitignore for Python/Discord bot projects
- Complete documentation (PRD, README, CHANGELOG)

### Security
- Role-based access control (administrator permission required)
- SQL injection prevention via parameterized queries
- Secure credential storage in .env files
- Ephemeral messages for sensitive operations
- Transaction logging and audit trail
