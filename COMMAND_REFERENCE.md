# COMMAND_REFERENCE.md

## Command Reference

All development commands are located in the `scripts/` directory and can be executed using the unified `scripts/dev` entrypoint.

### Available Commands

| Command | Description |
|--------|-----------|
| `bootstrap` | Initialize development environment and dependencies |
| `setup` | Configure tooling and environment settings |
| `doctor` | Diagnose environment health and integrity |
| `verify` | Run complete local verification suite |
| `format` | Apply code formatting standards |
| `lint` | Run static analysis and style checkers |
| `typecheck` | Perform static type checking |
| `test` | Execute test suite |
| `clean` | Remove generated artifacts and caches |

### Usage Examples
```bash
# Verify environment health
./scripts/dev doctor

# Run complete verification
./scripts/dev verify

# Format codebase
./scripts/dev format

# Run full quality check
./scripts/dev verify
```

All commands assume execution from repository root. The scripts directory provides both individual entrypoints and unified dispatcher.