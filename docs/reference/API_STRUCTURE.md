# Public REST API Directory Structure

```
backend/
├── app/
│   └── api/
│       ├── __init__.py               # API package entrypoint
│       ├── router.py                 # Aggregated API router (health + v1)
│       └── v1/                       # Version 1 REST API
│           ├── __init__.py
│           ├── dependencies/         # FastAPI dependency injection
│           │   ├── __init__.py
│           │   └── dependencies.py   # get_uow, get_command_pipeline, etc.
│           ├── errors/               # RFC 7807 Error handling
│           │   ├── __init__.py
│           │   └── error_handlers.py # ProblemDetails & DomainError mapping
│           ├── openapi/              # OpenAPI schema metadata
│           ├── responses/            # API response wrappers
│           ├── routers/              # Entity REST routers
│           │   ├── __init__.py       # Aggregated v1 router
│           │   ├── candidates.py     # /api/v1/candidates
│           │   ├── constituencies.py # /api/v1/constituencies
│           │   ├── elections.py      # /api/v1/elections
│           │   ├── parties.py        # /api/v1/parties
│           │   ├── polling_booths.py # /api/v1/polling-booths
│           │   └── results.py        # /api/v1/results
│           └── schemas/              # Pydantic v2 request & response schemas
│               ├── __init__.py
│               ├── candidate_schemas.py
│               ├── constituency_schemas.py
│               ├── election_schemas.py
│               ├── pagination.py     # Generic PaginatedResponse[T]
│               ├── party_schemas.py
│               ├── polling_schemas.py
│               └── result_schemas.py
tests/
└── test_api.py                       # REST API integration test suite
API_GUIDE.md                          # REST API guide & documentation
API_STRUCTURE.md                      # REST API directory structure layout
API_VALIDATION.md                     # REST API verification report
```

## Architectural Isolation Guarantees
1. **Zero Direct Repository Invocations**: Routers delegate 100% of execution to `CommandPipeline` and `QueryHandlers`.
2. **Schema Separation**: Pydantic v2 API schemas validate incoming JSON payloads and format outgoing responses separately from Domain or ORM models.
3. **Uniform Error Format**: Every non-2xx response returns standard RFC 7807 JSON.
