# Product Requirements Document

**Version**: 0.1.0
**Last Updated**: 2025-11-10T07:36:34.541Z
**Status**: Active

## 1. Executive Summary

**Product Name:** Economy Manager V1

**Platform:** Discord Bot

**Purpose:** Provide server administrators with an intuitive interface to manage player economies (gems and coins) in Minecraft servers by querying and updating a MySQL database through a Discord bot with button-based interactions.

**Key Vision:** Streamlined, user-friendly economy management without requiring command syntax knowledge—all interactions driven by interactive buttons and dropdowns.

---

## 2. Target Users

- Minecraft server administrators
- Economy managers
- Server staff with permission to manage player currencies

---

## 3. Features & Requirements

### 3.1 Player Selection - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Dropdown menu system to select players from the MySQL database

**Acceptance Criteria**:
- [ ] Display all active players from MySQL database in a searchable dropdown
- [ ] Allow users to search/filter player names within the dropdown
- [ ] Real-time population from database on bot startup and periodic refreshes

**Technical Notes**:
- Use discord.ui.Select component
- Implement database query to fetch all players
- Cache player list with periodic refresh mechanism

**Change History**:
- [0.1.0] - Feature planned

---

### 3.2 View Player Economy - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Display selected player's current gems and coins balance

**Acceptance Criteria**:
- [ ] Show player's current gems balance
- [ ] Show player's current coins balance
- [ ] Clean, formatted display of currency values
- [ ] Include player identifier (name/UUID) for confirmation

**Technical Notes**:
- Query database for player-specific economy data
- Format display using Discord embeds
- MCP servers involved: context7 (for discord.py embed best practices)

**Change History**:
- [0.1.0] - Feature planned

---

### 3.3 Add Currency - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Buttons to increase player's gem and coin balances

**Acceptance Criteria**:
- [ ] "Add Gems" button functional
- [ ] "Add Coins" button functional
- [ ] Modal/form input for specifying amount
- [ ] Confirmation before transaction applied
- [ ] Database successfully updated with new values

**Technical Notes**:
- Use discord.ui.Button components
- Use discord.ui.Modal for amount input
- Implement confirmation step
- Use parameterized SQL UPDATE queries

**Change History**:
- [0.1.0] - Feature planned

---

### 3.4 Remove Currency - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Buttons to decrease player's gem and coin balances

**Acceptance Criteria**:
- [ ] "Remove Gems" button functional
- [ ] "Remove Coins" button functional
- [ ] Modal/form input for specifying amount
- [ ] Validation to prevent negative balances
- [ ] Confirmation before transaction applied
- [ ] Database successfully updated with new values

**Technical Notes**:
- Use discord.ui.Button components
- Use discord.ui.Modal for amount input
- Implement balance validation logic
- Handle edge cases (insufficient balance)

**Change History**:
- [0.1.0] - Feature planned

---

### 3.5 Button-Based Interface - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: All interactions via buttons (no slash commands required)

**Acceptance Criteria**:
- [ ] All actions accessible via buttons
- [ ] Intuitive button layout with clear labeling
- [ ] Session persistence during active management
- [ ] User can manage multiple transactions in one session

**Technical Notes**:
- Design button layout for optimal UX
- Implement view persistence
- Handle timeout scenarios

**Change History**:
- [0.1.0] - Feature planned

---

### 3.6 Installation Script - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: Medium
**Description**: Automated installation from GitHub repository

**Acceptance Criteria**:
- [ ] Script clones repository from GitHub
- [ ] Downloads all required dependencies
- [ ] Places files in appropriate directories
- [ ] Executable on Windows, Linux, and macOS

**Technical Notes**:
- Create shell script for Unix systems
- Create batch script for Windows
- Use pip for Python dependencies

**Change History**:
- [0.1.0] - Feature planned

---

### 3.7 Setup Script - Status: Planned
**Version Introduced**: 0.1.0
**Priority**: High
**Description**: Interactive configuration script for bot setup

**Acceptance Criteria**:
- [ ] Interactive prompts for MySQL credentials (host, port, user, password)
- [ ] Prompt for database name
- [ ] Prompt for Discord bot token
- [ ] Prompt for Server ID/Guild ID
- [ ] Validates database connection
- [ ] Creates .env file with credentials
- [ ] Confirms successful setup

**Technical Notes**:
- Use python-dotenv for environment variable management
- Implement connection testing
- Secure credential storage
- Provide clear error messages

**Change History**:
- [0.1.0] - Feature planned

---

## 4. Technical Architecture

### 4.1 Technology Stack
- **Language**: Python 3.8+
- **Discord Framework**: discord.py (v2.0+)
- **Database**: MySQL
- **Database Connector**: mysql-connector-python
- **Environment Management**: python-dotenv
- **Logging**: Python logging module

### 4.2 Database Schema Assumptions
- **Table name**: `players` (configurable)
- **Columns**: 
  - `player_name` or `uuid` (player identifier)
  - `gems` (integer)
  - `coins` (integer)

### 4.3 Bot Architecture
```
bot/
├── main.py              # Bot entry point
├── cogs/
│   ├── economy.py       # Economy management commands
│   └── admin.py         # Admin utilities
├── database/
│   ├── db_manager.py    # Database connection and queries
│   └── models.py        # Data models
├── ui/
│   ├── views.py         # Discord UI views
│   ├── modals.py        # Input modals
│   └── buttons.py       # Button components
└── utils/
    ├── config.py        # Configuration loader
    └── logger.py        # Logging setup
```

### 4.4 Security Measures
- Role-based access control
- SQL injection prevention (parameterized queries)
- Bot token stored in .env (never hardcoded)
- Transaction logging
- Input validation

### 4.5 Error Handling
- Graceful database connection error handling
- User-friendly error messages in Discord
- Comprehensive logging system
- Automatic reconnection logic
- Timeout handling

---

## 5. Testing Requirements

### 5.1 Unit Tests
- Database query functions
- Currency validation logic
- Permission checking

### 5.2 Integration Tests
- Discord bot command flow
- Database transactions
- UI component interactions

### 5.3 Performance Benchmarks
- Bot response time < 2 seconds
- Database query optimization
- Concurrent user handling

---

## 6. Deployment & Maintenance

### 6.1 Deployment Process
1. Clone repository
2. Run installation script
3. Run setup script (configure credentials)
4. Start bot with `python main.py`

### 6.2 Monitoring
- Transaction logging
- Error logging
- Uptime monitoring
- Database connection status

### 6.3 Rollback Procedures
- Version tags for stable releases
- Database backup before major updates
- Configuration backup

---

## 7. Version History
- [0.1.0] - 2025-11-10 - Initial project setup and planning phase
