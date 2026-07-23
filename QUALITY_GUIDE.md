# QUALITY_GUIDE.md

## Quality Workflow

### Single Quality Entrypoint
All quality checks are accessible through the unified `scripts/quality` command.

### Quality Check Categories

- **Environment Health**: `scripts/quality doctor`
- **Code Quality**: `scripts/quality lint`, `scripts/quality format`, `scripts/quality typecheck`
- **Testing**: `scripts/quality test`
- **Cleanup**: `scripts/quality clean`

### Quality Check Flow
1. Run `./scripts/quality` for complete quality verification
2. Review individual script outputs for detailed results
3. Address any issues before proceeding

### Quality Documentation
- `QUALITY_GUIDE.md` - Workflow documentation (this file)
- `QUALITY_REFERENCE.md` - Command reference and expectations

### Quality Principles
- Local execution only
- No remote services
- No CI/CD configuration
- All checks must be executable locally
- Scripts must remain as wrappers only