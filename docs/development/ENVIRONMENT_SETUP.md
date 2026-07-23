# ENVIRONMENT_SETUP.md

## Platform-Specific Setup

### macOS (Apple Silicon)

```bash
# Homebrew (pre-installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Core tools
brew install git python@3.12 node@20 flutter docker postgresql@16 redis

# Shell configuration
echo 'export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Linux (Ubuntu/Debian)

```bash
# System packages
sudo apt update && sudo apt install -y git python3.12 python3.12-venv nodejs npm docker.io postgresql-16 redis-server

# Flutter (snap)
sudo snap install flutter --classic

# Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

### Windows (WSL2)

```bash
# Install WSL2
wsl --install

# Inside WSL2, follow Linux instructions above
```

## Version Requirements

| Tool | Minimum Version | Recommended |
|------|----------------|-------------|
| Python | 3.12 | 3.12.x |
| Node.js | 20.x LTS | 20.x |
| Flutter | 3.16 | 3.22+ |
| Docker | 24.x | 25.x+ |
| PostgreSQL | 16 | 16.x |
| Redis | 7.x | 7.2+ |

## Environment Variables

Required for local development:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/election_db

# Cache
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here

# Application
APP_ENV=development
DEBUG=true
```

## Dependency Installation

### Python
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Flutter
```bash
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### Node.js (if needed for tooling)
```bash
npm install -g pnpm
pnpm install
```