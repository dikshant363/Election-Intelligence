# AI Agent Collaboration Governance

## 1. Agent Roles and Boundaries

- **Principal Architect Agent:** Responsible for system design, structural changes, and approving core library upgrades.
- **Feature Implementation Agent:** Writes backend endpoints and frontend widgets. Focuses on logic and integration.
- **Test Agent:** Solely responsible for writing and maintaining unit, integration, and E2E tests.
- **Documentation Agent:** Keeps documentation in sync with codebase changes.
- **Review Agent:** Reviews PRs for security, performance, and adherence to style guides.

## 2. Branch Ownership Rules

- Every agent session must operate on an isolated feature branch (e.g., `feature/[agent-id]/endpoint-name`).
- Agents must **never** commit directly to `main` or `master`.
- An agent session owns its branch; other agents should not push to a branch currently owned by an active session unless explicitly instructed.

## 3. Naming Conventions for Agent Commits

Commits must follow Conventional Commits and identify the agent:
```text
feat(auth): implement JWT refresh token logic [agent:FeatureImpl-XYZ]
fix(db): resolve asyncpg connection leak [agent:Architect-ABC]
docs(api): update swagger for elections endpoint [agent:DocGen]
```

## 4. Conflict Resolution Protocol

- If an agent encounters a merge conflict, it must attempt to rebase on `main`.
- If the conflict is purely textual and obvious, the agent may resolve it.
- **Architectural or logic conflicts MUST NOT be auto-resolved by agents.** The agent must halt, document the conflict in the PR, and request human intervention.

## 5. What Agents MAY Do

- Create and checkout feature branches.
- Write, modify, and run tests.
- Update documentation files in `/docs`.
- Add new API endpoints that strictly follow existing established patterns (e.g., routing, DI, models).
- Refactor code within a single bounded context or subsystem.

## 6. What Agents MUST NOT Do

- Modify database migration files (Alembic) without explicit human approval.
- Change authentication, authorization (RBAC), or JWT logic without human review.
- Add external dependencies (`pyproject.toml`, `pubspec.yaml`) without human approval.
- Modify CI/CD pipeline definitions (`.github/workflows/ci.yml`) without human review.
- Commit secrets, API keys, or sensitive configuration values.
- Merge their own Pull Requests.
- Delete or rename existing public API endpoints (breaking changes).
- Modify `ARCHITECTURE.md` or `THREAT_MODEL.md` without human approval.

## 7. Quality Gate Requirements

Before committing, agents MUST run and ensure the success of:
- `ruff check .` (Python linting)
- `pytest` (Backend tests - 287 currently)
- `flutter analyze` (Dart linting)
- `flutter test` (Frontend tests - 6 currently)

## 8. Documentation Requirements

Agents must update relevant documentation when changing code. If an agent adds an endpoint, it must ensure OpenAPI schemas (via FastAPI Pydantic models) are updated and any relevant markdown docs are amended.

## 9. Escalation Protocol

An agent must stop execution, drop context into a status file or PR comment, and request human input if:
- It repeatedly fails to fix a test failure after 3 attempts.
- It encounters an ambiguous requirement affecting security.
- It needs to modify core infrastructure (DB schema, Auth middleware).

## 10. Agent Session Tracking

Agent changes are tracked via the `[agent:<ID>]` tag in commit messages. Human reviewers can filter Git history by these tags to audit the behavior of specific agent configurations.

## 11. Multi-agent Coordination

To avoid concurrent modification conflicts:
- Agents must pull the latest changes frequently.
- Agents must lock specific files conceptually via PR drafts if making sweeping changes.
- Two agents should not be assigned to refactor the same module simultaneously.
