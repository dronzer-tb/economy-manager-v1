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
