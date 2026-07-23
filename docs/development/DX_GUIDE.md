# DX_GUIDE.md

## Developer Experience Guide

### Workflow
- All commands accessed via `scripts/dev <command>`
- Scripts are wrappers only — no implementation logic
- See `COMMAND_REFERENCE.md` for command list

### Conventions
- Scripts directory contains only dispatcher wrappers
- No business logic in DX layer
- Validation scripts must be executable and non-empty
- Documentation must remain under 200 lines per file

### Troubleshooting
See `TROUBLESHOOTING.md` for common issues.