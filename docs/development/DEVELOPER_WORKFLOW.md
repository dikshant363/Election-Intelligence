# Developer Workflow & Git Standards

This document outlines the standard Git workflow, commit conventions, and review processes for the Election Intelligence Platform.

## 1. Branch Strategy

We use a feature-branch workflow. All branches must branch from and merge back into `main` (or a specific release branch).

**Naming Convention:**
- `feature/sprint-X.Y-short-name`: For new features.
  - Example: `feature/sprint-1.2-candidate-profile`
- `hotfix/short-name`: For urgent production fixes.
  - Example: `hotfix/fix-auth-token-expiry`
- `release/vX.Y.Z`: For staging releases.
  - Example: `release/v1.0.0`
- `chore/short-name`: For maintenance tasks (dependency updates, refactoring).

## 2. Conventional Commits

We follow [Conventional Commits](https://www.conventionalcommits.org/). This standardizes our history and allows automated changelog generation.

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools
- `refactor:` A code change that neither fixes a bug nor adds a feature

**Examples:**
- `feat(api): add district boundary endpoint`
- `fix(auth): resolve JWT token race condition`
- `test(domain): add voter aggregate unit tests`
- `chore(deps): update fastapi to 0.109.0`

## 3. Pre-commit Checklist

Before pushing any code or opening a PR, ensure you have:
1. Ran the linter: `ruff check backend` and `flutter analyze`
2. Formatted code: `ruff format backend`
3. Compiled Python code: `python -m compileall backend`
4. Ran backend tests: `pytest` (Must pass all 287+ tests)
5. Ran frontend tests: `flutter test`

## 4. Pull Request Template

When creating a PR, use the default template:

```markdown
## Description
Provide a brief overview of the changes. Link to JIRA/Linear ticket if applicable.

## Type of change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)

## Checklist:
- [ ] I have performed a self-review of my code
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing tests pass locally with my changes
- [ ] My code follows the style guidelines of this project
```

## 5. Code Review Standards

Reviewers must evaluate the PR for:
- **Architecture:** Does this violate Layered Architecture? Are domain models isolated?
- **Security:** Are inputs validated? Are queries safe from SQL injection?
- **Performance:** Are database queries optimized (e.g., resolving N+1 issues)?
- **Tests:** Are edge cases covered? Are mocks used appropriately?
- **Naming:** Are variables and functions explicitly named?

## 6. Merge Policy

- PRs require at least **1 approval** from a core team member.
- CI/CD pipelines must pass (Build, Test, Lint).
- All discussions must be resolved.
- Squash and merge is preferred to keep the `main` history clean.

## 7. Release Workflow

1. Cut a release branch: `git checkout -b release/v1.1.0`
2. Bump versions in `pyproject.toml` and `pubspec.yaml`.
3. Generate Changelog based on commits.
4. Merge `release` into `main`.
5. Tag the merge commit: `git tag -a v1.1.0 -m "Release v1.1.0"`
6. Push tags: `git push origin --tags`
7. CI/CD will automatically build Docker images and push to the registry.

## 8. Hotfix Workflow

1. Branch off `main` (or the specific tagged release): `git checkout -b hotfix/issue-name`
2. Apply the fix and write a regression test.
3. Open a PR against `main`.
4. Merge and tag a patch release (e.g., `v1.1.1`).

## 9. AI Agent Collaboration Rules

For AI agents (Claude, Gemini, Codex) contributing to this repository:
- **Commits:** Agents must strictly use the conventional commit format.
- **Branches:** Agents must use the designated branch naming convention.
- **Self-Correction:** Agents should run quality gates (`ruff`, `pytest`, `flutter analyze`) and fix issues before summarizing their turn.
- **Documentation:** Agents must update corresponding docstrings and markdown files when altering system behavior.
- **No force-pushing** to shared branches.
