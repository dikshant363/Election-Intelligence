# LOCAL_AUTOMATION.md

## Local Automation

The repository includes a suite of development scripts located in the `scripts/` directory. Each script serves a distinct purpose in the local development workflow:

- `scripts/dev` - Unified command dispatcher for all development tasks
- `scripts/bootstrap` - Initializes development environment
- `scripts/setup` - Configures tooling dependencies
- `scripts/doctest` (if present) - Validates documentation examples
- `scripts/format` - Applies code formatting tools
- `scripts/lint` - Runs linters and style checkers
- `scripts/typecheck` - Executes static type checking
- `scripts/test` - Runs the test suite
- `scripts/clean` - Removes generated artifacts
- `scripts/doctor` - Diagnoses environment health
- `scripts/verify` - Runs complete repository verification

All scripts are executable and accept no arguments. The unified `scripts/dev` wrapper command accepts natural language commands such as `./scripts/dev format` or `./scripts/dev verify`.

The scripts are designed to be called directly from the repository root and operate within the project's configured environment. No implementation-specific code is included; scripts contain only documentation, placeholder logic, or command delegation.