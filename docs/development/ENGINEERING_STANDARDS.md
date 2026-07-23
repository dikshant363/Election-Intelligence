# ENGINEERING_STANDARDS.md

## Codebase Standards

### Python
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants
- Type hints on all public function parameters
- Docstrings for all public functions (Google style)
- Maximum line length: 100 characters
- One import per line
- Group imports: stdlib, third-party, local

### Flutter
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

### TypeScript
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

### SQL
- Use snake_case for table/column names
- Always use explicit column names in SELECT
- Use proper data types with length specifications
- Add constraints (NOT NULL, UNIQUE, CHECK)
- Add indexes for frequently queried columns
- Use migrations for schema changes
- Name conventions: `idx_` for indexes, `fk_` for foreign keys, `pk_` for primary keys

### Markdown
- Use `#` for main headers, `##` for subsections
- Keep lines under 80 characters
- Use code blocks with language specification
- Use tables for structured data
- Use ordered lists for processes
- Use unordered lists for feature lists
- Always include examples for code snippets
- Use relative links for internal references
- Use explicit links for external sources

### YAML
- Use 2-space indentation
- Use double quotes for strings with special characters
- Use single quotes for simple strings
- Align colons in mappings
- Use computed values with `&` for reuse
- Validate with schema when possible
- Keep files under 256 lines per component

### JSON
- Use 2-space indentation
- Use double quotes for keys and string values
- No trailing commas
- Alphabetize object keys
- Group related properties
- Validate against schema

### Shell
- Use `#!/bin/bash` shebang
- Use `set -euo pipefail` for error handling
- Use descriptive variable names
- Avoid complex one-liners; use functions
- Quote variables with double quotes
- Use `set -x` for debugging
- Use `echo` for user-facing messages
- Use `read` for input validation