# SETUP.md

## 1. Installed Software (Verified)
- **Homebrew**: Installed via `/opt/homebrew/bin/brew`
- **Core CLI Tools**: `git`, `node`, `python3`, `docker`, `postgresql@16`, `postgresql@18`, `redis`, `flutter`, `uv`, `uvwasi`, `webp`, `pipx`, `ripgrep`, `starship`, `antigravity-cli`, `claude-code`, `git-lfs`, `1password-cli`, `android-studio`
- **CLI/Tools**: `claude` (Claude Code CLI) v2.1.204 installed
- **Verification**: 
  - `python3 --version` → `/opt/homebrew/bin/python3`
  - `node --version` → `/opt/homebrew/bin/node`
  - `docker --version` → `/usr/local/bin/docker`
  - `git --version` → `git version 2.45.0`
  - `git lfs version` → `git-lfs/3.7.1`
  - `flutter --version` → `Flutter 3.22.0`
  - `claude --version` → `2.1.204 (Claude Code)`

## 2. Missing Software (Required)
| Category | Missing Tools |
|----------|---------------|
| **Android** | `adb` |
| **IDE** | `code` (VS Code), `cursor` |
| **CLI** | `yarn`, `gemini-cli`, `playwright`, `fastapi` |
| **Python Packages** | `pytest`, `jest`, `black`, `ruff`, `flake8`, `eslint`, `prettier`, `stylua`, `fzf`, `htop`, `tmux` |
| **Security** | `ssh-audit`, `gitleaks` |
| **Project Tools** | `pnpm` (global), `yarn` (global) |

## 3. Installation Commands

### 3.1 Homebrew Packages
```bash
# Install missing formula packages
brew install adb yarn gemini-cli playwright fastapi fzf htop tmux ssh-audit

# Install GUI apps via Homebrew Cask
brew install --cask visual-studio-code   # Provides `code` command after enabling "Shell Command: Install 'code' command in PATH" from VS Code UI
```

### 3.2 npm Global Packages
```bash
# Install pnpm globally
npm install -g pnpm

# Install Playwright browsers
npm install -g playwright
```

### 3.3 Python Environment
```bash
# Ensure Python 3.12 is default
brew install python@3.12
echo 'export PATH="/opt/homebrew/opt/python@3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Optional: pyenv for version management
brew install pyenv
echo -e '\n# pyenv\nexport PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"\neval "$(pyenv init --path)"\neval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

### 3.4 Node.js (via nvm)
```bash
# Install nvm
brew install nvm
echo -e '\n# nvm\nexport NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")\n\.(\(nvm\) -s "$NVM_DIR/nvm.sh" > /dev/null 2>&1 || \. "$NVM_DIR/nvm.sh")\n' >> ~/.zshrc
source ~/.zshrc
nvm install --lts   # installs latest LTS (e.g., 20.x)
nvm use --lts
```

### 3.5 Ruby & Gems (if needed)
```bash
gem install bundler
gem install gemini-cli   # installs gemini CLI globally
```

### 3.5 Flutter Setup
```bash
# Flutter already installed via Homebrew
brew install flutter

# Run flutter doctor to verify Android/iOS toolchain
flutter doctor

# Install Android SDK components (if using Android emulator)
flutter doctor Android-sdk
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$PATH
```

### 3.6 Android Platform Tools
```bash
# Install platform-tools (if not already)
brew install android-platform-tools

# Verify ADB
adb version
adb devices
```

### 3.7 iOS Setup
```bash
# Ensure Xcode Command Line Tools are installed
xcode-select --install

# Verify Xcode
xcodebuild -version

# List simulators
xcrun simctl list devices
```

### 3.8 Docker & Compose
```bash
# Start Docker daemon
brew services start docker

# Verify Docker
docker --version
docker run hello-world

# Install Docker Compose (if needed)
brew install docker-compose
```

### 3.8 PostgreSQL
```bash
# Start PostgreSQL service
brew services start postgresql@16   # adjust version as installed

# Create database and user
createdb my_election_db
psql -U postgres -c "CREATE USER election_user WITH PASSWORD 'secure_password';"
psql -U election_user -d my_election_db -c "GRANT ALL PRIVILEGES ON DATABASE my_election_db TO election_user;"

# Verify connection
psql -U election_user -d my_election_db -c "SELECT version();"
```

### 3.9 Redis
```bash
# Start Redis service
brew services start redis

# Verify Redis
redis-cli ping   # Expected output: PONG
```

### 3.10 Git Setup
```bash
# Configure Git identity
git config --global user.name "Dikshant Aggarwal"
git config --global user.email "dikshant@example.com"

# Enable SSH key usage (see GitHub SSH setup)
ssh-keygen -t ed25519 -C "dikshant@example.com" -f ~/.ssh/id_ed25519
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Verify SSH connection
ssh -T git@github.com
```

### 3.11 GitHub CLI
```bash
# Install GitHub CLI (if not installed)
brew install gh

# Authenticate to GitHub
gh auth login   # follow prompts

# Verify authentication
gh auth status
```

### 3.12 Python Development
```bash
# Create virtual environment (example)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dev tools
pip install pytest hypothesis
```

### 3.13 Node.js Development
```bash
# Verify Node version
node --version   # should be v20.x (or latest LTS)

# Install npm packages globally
npm install -g pnpm
pnpm config set store-dir "$HOME/.pnpm-store"
```

### 3.14 pnpm Setup
```bash
# Verify pnpm
pnpm --version   # should be >9.x

# Install project dependencies
pnpm install
```

### 3.15 Claude Code Setup
```bash
# Verify installation
claude --version   # should show 2.1.204

# Configure status line (optional)
echo '{"statusline": {"enabled": true, "format": "Claude: {version}"}}' > ~/.claude/settings.json

# Initialize project directory
cd /Users/dikshantagarwal/Desktop/CivicLens India/Election-Intelligence
claude init   # creates .claude/ folder if needed
```

### 3.16 Gemini CLI Setup
```bash
# Install globally (if not done earlier)
pip3 install gemini-cli

# Verify
gemini --version

# Configure API key
mkdir -p ~/.gemini
echo 'api_key: YOUR_GEMINI_API_KEY' > ~/.gemini/config.yaml
```

### 3.17 Playwright Setup
```bash
# Install browsers
playwright install

# Verify installation
playwright --version
playwright show-browsers   # lists installed browsers

# Create test script
cat > test_playwright.js <<'EOF'
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  console.log('Title:', await page.title());
  await browser.close();
})();
EOF
node test_playwright.js
```

### 3.18 FastAPI Setup
```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Create sample app (main.py)
cat > main.py <<'EOF'
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
EOF

# Run server
uvicorn main:app --reload

# Test endpoint
curl http://127.0.0.1:8000
```

### 3.18 Project Dependencies
- Create `requirements.txt` (Python) or `package.json` (Node) / `pubspec.yaml` (Flutter) with exact versions.
- Example `requirements.txt`:
  ```
  fastapi==0.110.0
  uvicorn[standard]==0.25.0
  sqlalchemy==2.0.30
  psycopg2-binary==2.9.9
  redis==5.0.3
  ```
- Example `package.json` snippet:
  ```json
  {
    "name": "election-intelligence",
    "version": "0.1.0",
    "private": true,
    "scripts": {
      "start": "node index.js"
    },
    "dependencies": {
      "fastify": "^4.28.0"
    }
  }
  ```

### 3.19 Recommended Terminal Utilities
- **fzf**: `brew install fzf && $(brew --prefix)/opt/fzf/install`
- **exa**: `brew install exa`
- **bat**: `brew install bat`
- **ripgrep**: `brew install ripgrep` (already installed)
- **starship**: `brew install starship`
- **zsh-syntax-highlighting**: `brew install zsh-syntax-highlighting`
- **zsh-autosuggestions**: `brew install zsh-autosuggestions`
- Add to `~/.zshrc`:
  ```bash
  eval "$(fzf --zsh)"
  eval "$(zsh-autosuggestions)"
  eval "$(starship init zsh)"
  ```
- Reload shell: `source ~/.zshrc`

### 3.20 Security Tools
- **1Password CLI**: `brew install 1password-cli`
- **ssh-audit**: `brew install ssh-audit`
- **gitleaks**: `brew install gitleaks`
- **truffleHog**: `pip install truffleHog`
- **lynis** (system audit): `brew install lynis`

### 3.21 Testing Tools
- **pytest**: `pip install pytest`
- **jest**: `npm install -g jest`
- **coverage**: `pip install coverage`
- **pytest-cov**: `pip install pytest-cov`
- **snyk**: `npm install -g snyk`
- **OWASP ZAP**: `brew install zaproxy` (or use Docker image)

### 3.22 Linting Tools
- **flake8** (Python): `pip install flake8`
- **black** (Python formatter): `pip install black`
- **ruff** (Python linter): `pip install ruff`
- **eslint** (JS/TS): `npm install -g eslint`
- **prettier** (JS/TS formatter): `npm install -g prettier`
- **stylua** (Lua): `brew install stylua`
- **check-js**: `npm install -g check-js`

### 3.23 Formatting Tools
- **prettier** (already listed)
- **stylua** (already listed)
- **clang-format** (C/C++/Obj-C): `brew install clang-format`
- **black** (Python): `pip install black`
- **isort** (Python imports): `pip install isort`

### 3.24 Everything Required Before Writing a Single Line of Code
- [ ] All software in sections 1‑21 installed and verified.
- [ ] `~/.zshrc` updated with environment variables from section 4.
- [ ] Shell reloaded (`source ~/.zshrc`).
- [ ] Project dependencies initialized (virtual env, pnpm install, etc.).
- [ ] Git repository initialized (`git init`) and `.gitignore` created.
- [ ] Pre‑commit hooks installed (e.g., `pre-commit install`) if using them.
- [ ] IDE extensions installed and configured (VS Code Antigravity, GitLens, Prettier, etc.).
- [ ] Security baseline (SSH keys, 1Password, API secrets) stored securely.
- [ ] CI/CD pipeline (GitHub Actions / GitLab CI) skeleton defined.
- [ ] Monitoring / logging (e.g., `loguru` for Python) ready.
- [ ] Backup strategy (Git remote, cloud sync) configured.
- [ ] Documentation scaffold (`README.md`, `CONTRIBUTING.md`) created.
- [ ] License file added (`LICENSE`).
- [ ] Project management board (GitHub Projects / Jira) set up with initial issues.

---

**Verification commands** (run sequentially):
```bash
# Homebrew
brew list --versions

# Python
python3 -V; pip -V

# Node
node -v; npm -v

# Docker
docker info

# PostgreSQL
psql -V

# Redis
redis-cli ping

# Flutter
flutter doctor -v

# Android
adb version

# iOS
xcodebuild -version

# GitHub
gh auth status

# VS Code
code --version   # after installing

# Playwright
playwright install && playwright test --help

# FastAPI
uvicorn --version
```

After reviewing, **please approve** so we can proceed with initializing the workspace or making further adjustments.