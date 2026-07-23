# Dependency Rules

This document outlines the strict dependency management rules for the Election Intelligence Platform, adhering to Clean Architecture principles.

## 1. Architectural Dependency Diagram

```text
+-----------------------------------------------------+
|                  PRESENTATION                       |
|  (api, routers, schemas, dependencies)              |
+--------------------------+--------------------------+
                           |
                           v
+--------------------------+--------------------------+
|                  APPLICATION                        |
|  (commands, queries, handlers, DTOs, interfaces)    |
+--------------------------+--------------------------+
                           |
                           v
+--------------------------+--------------------------+
|                     DOMAIN                          |
|  (aggregates, entities, value_objects, exceptions)  |
+-----------------------------------------------------+

+-----------------------------------------------------+
|                 INFRASTRUCTURE                      |
| (persistence, database, security, ai, search, etc)  |
+--------------------------+--------------------------+
                           |
                           v
          [Depends on Application & Domain]
```

*Rule: Dependencies point strictly INWARD toward the Domain.*

## 2. Package Dependency Table

| Package | Can Import | Cannot Import |
|---------|------------|---------------|
| `api` | `application`, `domain`, `core` | `infrastructure`, `persistence`, `database` |
| `application` | `domain`, `core` | `api`, `infrastructure`, `persistence`, `database` |
| `domain` | `core` | `api`, `application`, `infrastructure`, `persistence`, `database`, `security` |
| `persistence` | `domain`, `application`, `database`, `core` | `api` |
| `database` | `core` | `api`, `application`, `domain` (except generic types) |
| `security` | `application`, `domain`, `core` | `api` |
| `identity` | `application`, `domain`, `core` | `api` |
| `etl` | `application`, `domain`, `infrastructure`, `core` | `api` |
| `search` | `application`, `domain`, `core` | `api` |
| `ai` | `application`, `domain`, `core` | `api` |
| `realtime` | `application`, `domain`, `core` | `api` |
| `observability` | `core` | Business logic packages |
| `performance` | `core` | Business logic packages |
| `production` | `core` | Business logic packages |
| `core` | None (Standard Library only) | All other packages |
| `config` | `core` | All other packages |

## 3. Forbidden Patterns

### ❌ WRONG: Domain importing Infrastructure
```python
# domain/aggregates/election.py
from infrastructure.database.models import ElectionModel # ILLEGAL

class Election:
    pass
```

### ✅ RIGHT: Infrastructure imports Domain
```python
# infrastructure/persistence/repositories/election_repo.py
from domain.aggregates.election import Election
from infrastructure.database.models import ElectionModel

class ElectionRepository:
    def to_domain(self, model: ElectionModel) -> Election:
        ...
```

### ❌ WRONG: Application logic using HTTP requests directly
```python
# application/commands/create_election.py
from fastapi import Request # ILLEGAL

def handle(request: Request):
    pass
```

### ✅ RIGHT: Application uses DTOs/Commands
```python
# application/commands/create_election.py
from pydantic import BaseModel

class CreateElectionCommand(BaseModel):
    name: str

def handle(command: CreateElectionCommand):
    pass
```

## 4. Checking Violations

Use `pytest-archon` or similar architectural testing tools, or run greps:

```bash
# Check if domain imports application or infrastructure
grep -r "from application " backend/app/domain/
grep -r "from infrastructure " backend/app/domain/
```

We enforce these rules automatically in CI using custom Ruff rules and standard architectural tests.

## 5. Architectural Reasoning

- **Domain Isolation**: Core business logic must be testable without databases, APIs, or external services.
- **Replaceability**: Infrastructure details (Postgres, Redis) can be swapped without rewriting Application or Domain logic.
- **Separation of Concerns**: Presentation handles HTTP/JSON; Application handles use cases; Domain handles business rules.

## 6. Exceptions

Exceptions to these rules are extremely rare. They require:
1. Written justification via PR comment.
2. Approval from a Staff Engineer or Architect.
3. Explicit `# noqa: dependency-rule` comment explaining the temporary hack and link to tech-debt ticket.
