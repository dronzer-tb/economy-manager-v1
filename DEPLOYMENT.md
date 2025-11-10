# GitHub Deployment Guide

This guide will help you deploy Economy Manager V1 to your GitHub repository.

## Prerequisites

- Git installed
- GitHub account
- Repository created: `economy-manager-v1`

## Step 1: Initialize Git (If Not Done)

```bash
cd "/home/kasniya/Economay manager"
git init
git branch -M main
```

## Step 2: Add Remote Repository

Replace `dronzer-tb` with your GitHub username if different:

```bash
git remote add origin https://github.com/dronzer-tb/economy-manager-v1.git
```

Or if already added:
```bash
git remote set-url origin https://github.com/dronzer-tb/economy-manager-v1.git
```

## Step 3: Stage All Files

```bash
git add .
```

## Step 4: Commit Changes

```bash
git commit -m "v0.2.0 - CoinsEngine compatibility + one-line installer

Major changes:
- Adapted to CoinsEngine database structure
- Added one-line installer script
- Support for decimal currency values
- Enhanced UI with UUID display
- Updated documentation

Breaking changes:
- Table name: players → coinsengine_users
- Column name: player_name → name
- Database name: minecraft_economy → coinsengine_shared
- Currency type: INT → DOUBLE
"
```

## Step 5: Push to GitHub

```bash
git push -u origin main
```

If you encounter authentication issues:
```bash
# Use personal access token
git push https://YOUR_USERNAME:YOUR_TOKEN@github.com/dronzer-tb/economy-manager-v1.git main
```

## Step 6: Create GitHub Release (Optional)

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v0.2.0`
4. Title: `Version 0.2.0 - CoinsEngine Compatible`
5. Description:
   ```markdown
   ## Economy Manager V1 - Version 0.2.0
   
   ### 🎉 What's New
   
   - ✅ **CoinsEngine Database Support**: Now compatible with CoinsEngine plugin
   - ✅ **One-Line Installer**: Easy installation with automated setup
   - ✅ **Decimal Currency**: Supports decimal values for gems and coins
   - ✅ **Enhanced UI**: Shows player UUIDs and formatted balances
   
   ### 📦 Quick Install
   
   ```bash
   curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash
   ```
   
   ### 🔄 Breaking Changes
   
   - Database table changed: `players` → `coinsengine_users`
   - Database name changed: `minecraft_economy` → `coinsengine_shared`
   - Column name changed: `player_name` → `name`
   - Currency type changed: INT → DOUBLE
   
   See [CHANGELOG.md](CHANGELOG.md) for full details.
   ```
6. Click "Publish release"

## Step 7: Update Repository Description

On GitHub repository page:
1. Click "About" settings (gear icon)
2. Description: `Discord bot for managing Minecraft server economies (gems & coins) - CoinsEngine compatible`
3. Topics: `discord-bot`, `minecraft`, `economy`, `python`, `coinsengine`
4. Save

## Step 8: Create README Badge (Optional)

Add these badges to top of README.md:

```markdown
[![GitHub release](https://img.shields.io/github/v/release/dronzer-tb/economy-manager-v1)](https://github.com/dronzer-tb/economy-manager-v1/releases)
[![GitHub issues](https://img.shields.io/github/issues/dronzer-tb/economy-manager-v1)](https://github.com/dronzer-tb/economy-manager-v1/issues)
[![GitHub stars](https://img.shields.io/github/stars/dronzer-tb/economy-manager-v1)](https://github.com/dronzer-tb/economy-manager-v1/stargazers)
```

## Step 9: Test One-Line Installer

From a clean directory:

```bash
cd /tmp
curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash
```

This verifies:
- ✅ Script is accessible
- ✅ Clone works
- ✅ Dependencies install
- ✅ Setup runs correctly

## Step 10: Update Repository Settings

### Branch Protection (Optional)
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable: "Require pull request reviews before merging"

### GitHub Pages (Optional)
If you want to host documentation:
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: `main`, folder: `/docs`
4. Save

## Common Git Commands

### Check Status
```bash
git status
```

### View Changes
```bash
git diff
```

### Pull Latest Changes
```bash
git pull origin main
```

### Create New Branch
```bash
git checkout -b feature/new-feature
```

### Switch Back to Main
```bash
git checkout main
```

### View Commit History
```bash
git log --oneline
```

### Undo Last Commit (Keep Changes)
```bash
git reset --soft HEAD~1
```

### Undo All Local Changes
```bash
git reset --hard origin/main
```

## Troubleshooting

### "Permission denied" error
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitHub Settings → SSH Keys

# Change remote to SSH
git remote set-url origin git@github.com:dronzer-tb/economy-manager-v1.git
```

### "Repository not found" error
```bash
# Verify remote URL
git remote -v

# Update URL
git remote set-url origin https://github.com/dronzer-tb/economy-manager-v1.git
```

### Large file warning
```bash
# Check file sizes
du -sh *

# Remove large files from git
git rm --cached large-file.log
echo "large-file.log" >> .gitignore
git commit -m "Remove large file"
```

### Merge conflicts
```bash
# Pull latest changes
git pull origin main

# Resolve conflicts in files
# Then:
git add .
git commit -m "Resolved merge conflicts"
git push origin main
```

## Post-Deployment Checklist

After pushing to GitHub:

- [ ] Repository is public/accessible
- [ ] README displays correctly
- [ ] install-bot.sh is accessible at raw URL
- [ ] One-line installer works
- [ ] All documentation files are present
- [ ] CHANGELOG is up to date
- [ ] Version tag created (v0.2.0)
- [ ] Issues tab enabled
- [ ] Discussions tab enabled (optional)
- [ ] License file present (MIT)

## Maintenance

### For Future Updates

1. Make changes locally
2. Update VERSION file
3. Update CHANGELOG.md
4. Update agent log
5. Commit:
   ```bash
   git add .
   git commit -m "vX.Y.Z - Description"
   git push origin main
   ```
6. Create new release on GitHub

### Versioning Rules

- **MAJOR (X.0.0)**: Breaking changes
- **MINOR (0.X.0)**: New features, backward compatible
- **PATCH (0.0.X)**: Bug fixes

---

## Your Repository URL

After deployment, users can install with:

```bash
curl -sSL https://raw.githubusercontent.com/dronzer-tb/economy-manager-v1/main/install-bot.sh | bash
```

**Repository:** https://github.com/dronzer-tb/economy-manager-v1

---

*Ready to deploy? Run the commands in Step 3-5 above!*
