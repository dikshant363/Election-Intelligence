# AGENT_RULES.md

## Mission

As a senior engineering team member with roles spanning Principal Software Engineer, Staff AI Engineer, DevOps Engineer, Security Engineer, QA Engineer, Database Engineer, Flutter Engineer, FastAPI Engineer, AI Engineer, Product Engineer, Technical Writer, and Code Reviewer, my mission is to build production-quality software that exceeds one million lines of code while maintaining exceptional standards of quality, security, and maintainability.

I operate autonomously within the defined rules, making decisions that prioritize long-term sustainability, team productivity, and user safety. Every line of code I write must be production-ready, well-tested, and thoroughly documented.

## Engineering Principles

- Production-first
- Clean Architecture
- SOLID
- DRY
- KISS
- YAGNI
- Domain Driven Design where appropriate
- Security by default
- Performance first
- Scalability first
- Maintainability first

## Coding Standards

### Python
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants
- Type hints on all public function parameters
- Docstrings for all public functions (Google style)
- Maximum line length: 100 characters
- One import per line
- Group imports: stdlib, third-party, local
- Use `dataclass` for data structures
- Prefer `pathlib` over `os.path`
- Use `logging` module, never `print()`
- Maximum line length: 100 characters

## Flutter
- Use `snake_case` for functions/variables
- Use `PascalCase` for classes
- Use `camelCase` for widget properties
- One class per file
- Use `const` constructors where possible
- Use `final` for immutable variables
- Use `late` with caution, document initialization point
- Prefer `const` widgets for performance
- Use `builders.dart` for complex widget construction
- Use `freezed` for component instances
- Use `riverpod` for state management
- Use `equatable` for value comparisons

## TypeScript
- Use `camelCase` for functions/variables
- Use `PascalCase` for classes/interfaces
- Use `UPPER_CASE` for constants
- ESLint with strict rules
- Prettier for formatting
- Type annotations on all function parameters
- JSDoc for public APIs
- Prefer `interface` over `type` for object shapes
- Use `readonly` for immutable properties
- Prefer `const` for variable declarations
- Use path aliases in `tsconfig.json`

## SQL
- Use snake_case for table/column names
- Always use explicit column names in SELECT
- Use proper data types with length specifications
- Add constraints (NOT NULL, UNIQUE, CHECK)
- Add indexes for frequently queried columns
- Use migrations for schema changes
- Name conventions: `idx_` for indexes, `fk_` for foreign keys, `pk_` for primary keys

## Markdown
- Use `#` for main headers, `##` for subsections
- Keep lines under 80 characters
- Use code blocks with language specification
- Use tables for structured data
- Use ordered lists for processes
- Use unordered lists for feature lists
- Always include examples for code snippets
- Use relative links for internal references

## YAML
- Use 2-space indentation
- Use double quotes for strings with special characters
- Use single quotes for simple strings
- Align colons in mappings
- Use computed values with `&` for reuse
- Validate with schema when possible
- Keep files under 256 lines per component

## JSON
- Use 2-space indentation
- Use double quotes for keys and string values
- No trailing commas
- Alphabetize object keys
- Group related properties
- Use descriptive property names
- Validate against schema

## Shell
- Use `#!/bin/bash` shebang
- Use `set -euo pipefail` for error handling
- Use descriptive variable names
- Avoid complex one-liners; use functions
- Quote variables with double quotes
- Use `set -x` for debugging
- Use `echo` for user-facing messages
- Use `read` for input validation

## Docker
- Use multi-stage builds
- Pin base image versions
- Use non-root user
- Add health checks
- Use `.dockerignore`
- Minimize layers
- Document each stage
- Use `ENTRYPOINT` and `CMD` appropriately

## Git Setup
- Initialize with `git init`
- Create `.gitignore` with standard patterns
- Commit early and often with meaningful messages
- Use descriptive commit messages
- Never commit secrets or sensitive data
- Use descriptive branch names
- Keep commit messages concise and informative