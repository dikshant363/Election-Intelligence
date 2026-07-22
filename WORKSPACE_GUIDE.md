# WORKSPACE_GUIDE.md

## VS Code Workspace

### Recommended Settings
- Enable format on save
- Use recommended extensions
- Configure Python interpreter to use virtual environment

### Dev Container
- Use the provided devcontainer.json for consistent development
- Forwarded ports: 8000 (API), optional Flutter dev server ports
- Post-create command runs setup script

### Local Development
- Use scripts/bootstrap and scripts/setup for initial setup
- Use individual scripts for specific tasks (format, lint, etc.)
- Use VS Code tasks for IDE integration