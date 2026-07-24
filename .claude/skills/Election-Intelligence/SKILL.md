```markdown
# Election-Intelligence Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the Election-Intelligence Python codebase. You'll learn how to structure files, write imports and exports, follow commit message styles, and understand the project's approach to testing. This guide is designed to help contributors maintain consistency and quality throughout the repository.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example: `data_processor.py`, `vote_counter.py`

### Import Style
- Use **relative imports** within the package.
  - Example:
    ```python
    from .utils import parse_results
    from .models import ElectionResult
    ```

### Export Style
- Use **named exports** (explicitly listing what is exported from a module).
  - Example:
    ```python
    __all__ = ['ElectionResult', 'parse_results']
    ```

### Commit Messages
- Messages are **freeform** (no strict prefix), with an average length of 60 characters.
  - Example:  
    ```
    Add initial data processing script for election results
    ```

## Workflows

### Adding a New Feature
**Trigger:** When implementing a new capability or module  
**Command:** `/add-feature`

1. Create a new Python file using snake_case (e.g., `new_feature.py`).
2. Implement your feature, using relative imports for dependencies.
3. Explicitly list exports with `__all__` if the module is intended for import elsewhere.
4. Write or update corresponding test files (see Testing Patterns).
5. Commit your changes with a clear, descriptive message.

### Fixing a Bug
**Trigger:** When correcting an error or flaw in the codebase  
**Command:** `/fix-bug`

1. Locate the problematic code and make the necessary corrections.
2. Update or add tests to cover the bug fix.
3. Use relative imports if importing from other modules.
4. Commit with a message describing the bug and the fix.

### Running Tests
**Trigger:** To verify code correctness after changes  
**Command:** `/run-tests`

1. Identify test files (pattern: `*.test.*`).
2. Use the project's preferred test runner (framework not specified; check project docs or use `pytest` as a default).
3. Run all tests and ensure they pass before merging.

## Testing Patterns

- Test files follow the pattern `*.test.*` (e.g., `data_processor.test.py`).
- Testing framework is **unknown**; check for test runners in the project or use `pytest` if unsure.
- Place tests alongside or near the modules they test.
- Example test file:
  ```python
  # data_processor.test.py
  from .data_processor import process_votes

  def test_process_votes():
      result = process_votes([1, 2, 3])
      assert result == 6
  ```

## Commands
| Command      | Purpose                                    |
|--------------|--------------------------------------------|
| /add-feature | Start the workflow for adding a new feature|
| /fix-bug     | Start the workflow for fixing a bug        |
| /run-tests   | Run all tests in the repository            |
```