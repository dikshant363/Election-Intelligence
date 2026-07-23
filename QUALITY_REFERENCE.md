# QUALITY_REFERENCE.md

## Quality Command Reference

### scripts/quality

**Purpose**: Single local quality entrypoint that dispatches to existing validation scripts.

**Usage**: 
```
./scripts/quality
```

**What it does**:
- Runs environment health check (doctor)
- Runs linting checks (lint)
- Runs code formatting checks (format)
- Runs static type checking (typecheck)
- Runs test suite (test)

**Note**: This is a dispatcher only - no implementation logic. All quality checks are handled by individual scripts.

### scripts/dev

**Purpose**: Unified command dispatcher for development tasks.

**Commands**:
```
./scripts/dev doctor    # Environment health check
./scripts/dev format    # Code formatting
./scripts/dev lint      # Linting checks
./scripts/dev typecheck # Type checking
./scripts/dev test      # Test execution
./scripts/dev verify    # Summary verification
./scripts/dev quality   # Local quality checks (new)
./scripts/dev clean     # Clean build artifacts
```

## Quality Validation Process

1. All quality checks are local-only
2. No remote services or CI/CD integration
3. All scripts must be executable and non-empty
4. Configuration files must be syntactically valid
5. Documentation must remain under 200 lines per file
6. No implementation logic in quality scripts