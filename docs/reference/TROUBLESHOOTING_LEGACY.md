# TROUBLESHOOTING.md

## Common Issues and Solutions

### 1. Missing Dependencies
**Error**: "command not found: git"
**Solution**: Install git via package manager
macOS: `brew install git`
Linux: `sudo apt install git`
Windows: Download from git-scm.com

### 2. Python Environment Issues
**Error**: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Node.js Installation
**Error**: "nvm: command not found"
**Solution**: Install Node Version Manager
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
```
Source ~/.bashrc: `source ~/.bashrc`
nvm install --lts
```

### 4. Flutter SDK Not Found
**Error**: "flutter: command not found"
**Solution**: Install Flutter via Homebrew
```bash
brew install --cask flutter
```
Flutter automatically adds to PATH.

### 5. Missing IDE Extensions
**Issue**: VS Code missing essential extensions
**Solution**: Open Command Palette (Ctrl+Shift+P), select "Extensions: Install Extensions"
Required: "Python", "Dart", "GitLens", "ESlint"

### 6. Git Configuration
**Issue**: Git user identity not set
**Solution**: Set global user configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 7. Docker Commands
**Error**: "docker command not found"
**Solution**: Install Docker
macOS: `brew install --cask docker`
Linux: `sudo apt install docker.io`
Start service: `sudo systemctl start docker`

### 8. PostgreSQL Connection
**Error**: "could not connect to server"
**Solution**: Start PostgreSQL service and configure pg_hba.conf
```bash
brew services start postgresql@16
createdb election_db
```

### 9. Redis Connection
**Error**: "Connection refused"
**Solution**: Start Redis service
macOS: `brew services start redis`
Linux: `sudo systemctl start redis`

### 10. Python Package Installation
**Error**: "Cannot install package 'fastapi'"
**Solution**: Update pip and install with --break-system-packages
```bash
pip install --break-system-packages fastapi
```

### 11. Node Package Manager
**Error**: "pnpm: command not found"
**Solution**: Install pnpm globally
```bash
npm install -g pnpm
```

### 12. Flutter Doctor Issues
**Error**: "Flutter doctor shows warnings"
**Solution**: Run `flutter doctor -v` and follow the prompts to install missing components.
For Android: Install Android Studio and create a virtual device.
For iOS: Install Xcode via the Mac App Store.

### 13. Git Authentication
**Error**: "Permission denied (publickey)"
**Solution**: Generate SSH key and add to ssh-agent
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```
Add the public key to your GitHub account settings.

### 14. Environment Variables
**Error**: "Missing required environment variable"
**Solution**: Copy .env.example to .env and configure
```bash
cp .env.example .env
```
Edit .env with your configuration values.

### 15. Python Version Mismatch
**Error**: "Python version not supported"
**Solution**: Install Python 3.12 via pyenv
```bash
pyenv install 3.12.x
pyenv global 3.12.x
```
Verify: `python3 --version`

### 16. Node.js Version Mismatch
**Error**: "Node.js version not supported"
**Solution**: Install Node.js 20.x via nvm
```bash
nvm install 20
nvm use 20
```
Verify: `node --version`

### 17. Docker Compose Issues
**Error**: "docker-compose command not found"
**Solution**: Install Docker Compose separately
```bash
brew install docker-compose
```
Or use Docker Desktop which includes Compose.

### 18. VS Code Settings Not Applied
**Issue**: VS Code settings not loading
**Solution**: Ensure you opened the folder as workspace
```bash
code .
```
Check .vscode/settings.json for correct configuration.

### 19. Git Large File Storage
**Error**: "git-lfs: command not found"
**Solution**: Install Git LFS
```bash
brew install git-lfs
git lfs install
```

### 20. Python Poetry Not Found
**Error**: "poetry: command not found"
**Solution**: Install Poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Add to PATH: `export PATH="$HOME/.local/bin:$PATH"`